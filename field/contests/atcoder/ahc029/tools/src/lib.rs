use std::{
    fmt,
    io::{BufRead, BufReader, BufWriter, Read, Write},
    str,
};

use anyhow::{bail, Context, Error, Result};
use rand::{prelude::*, Rng};
use rand_chacha::{rand_core::SeedableRng, ChaCha20Rng};
use rand_distr::{Normal, WeightedIndex};
use std::collections::VecDeque;
use svg::node::element::SVG;

#[cfg(target_arch = "wasm32")]
use wasm_bindgen::prelude::*;

#[cfg(target_arch = "wasm32")]
use once_cell::sync::Lazy;

#[cfg(target_arch = "wasm32")]
use std::sync::Mutex;

mod lib_vis;
use lib_vis::SVGDrawer;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum CardType {
    WorkSingle,
    WorkAll,
    CancelSingle,
    CancelAll,
    Invest,
}

impl CardType {
    fn new(ty: usize) -> Self {
        match ty {
            0 => CardType::WorkSingle,
            1 => CardType::WorkAll,
            2 => CardType::CancelSingle,
            3 => CardType::CancelAll,
            4 => CardType::Invest,
            _ => panic!("Invalid type"),
        }
    }

    fn generate(rng: &mut ChaCha20Rng, x: &Vec<i64>) -> Self {
        let weighted_index = WeightedIndex::new(x).unwrap();
        let val = weighted_index.sample(rng);
        CardType::new(val)
    }
}

#[derive(Debug, Clone, Copy)]
pub struct Card {
    ty: CardType,
    w: i64,
    p: i64,
}

#[derive(Debug, Clone, Copy)]
pub struct Project {
    initial_h: i64,
    h: i64,
    v: i64,
}

#[derive(Debug, Clone)]
pub struct JudgeData {
    n: usize,
    m: usize,
    k: usize,
    t: usize,
    initial_projects: Vec<Project>,
    new_projects: Vec<Project>,
    initial_cards: Vec<Card>,
    new_cards: Vec<Vec<Card>>,
}

impl fmt::Display for JudgeData {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        writeln!(f, "{} {} {} {}", self.n, self.m, self.k, self.t)?;

        for project in self.initial_projects.iter() {
            writeln!(f, "{} {}", project.h, project.v)?;
        }

        for project in self.new_projects.iter() {
            writeln!(f, "{} {}", project.h, project.v)?;
        }

        for card in self.initial_cards.iter() {
            writeln!(f, "{} {}", card.ty as usize, card.w)?;
        }

        for cards in self.new_cards.iter() {
            for card in cards {
                writeln!(f, "{} {} {}", card.ty as usize, card.w, card.p)?;
            }
        }

        Ok(())
    }
}

impl str::FromStr for JudgeData {
    type Err = Error;

    fn from_str(s: &str) -> Result<Self> {
        let mut tokens = s.split_whitespace();

        let n: usize = read(tokens.next(), 2, 7).context("N")?;
        let m: usize = read(tokens.next(), 2, 8).context("M")?;
        let k: usize = read(tokens.next(), 2, 5).context("K")?;
        let t: usize = read(tokens.next(), 1000, 1000).context("T")?;

        let mut initial_projects: Vec<Project> = vec![];
        for i in 0..m {
            let h: i64 = read(tokens.next(), 1 << 2, 1 << 8)
                .context(format!("initial projects: h_init_{}", i))?;
            let v: i64 = read(tokens.next(), 1, 1 << 10)
                .context(format!("initial projects: v_init_{}", i))?;
            initial_projects.push(Project { initial_h: h, h, v });
        }

        let mut new_projects = Vec::new();
        for i in 0..m * t {
            let h: i64 =
                read(tokens.next(), 1 << 2, 1 << 8).context(format!("new projects: h_{}", i))?;
            let v: i64 =
                read(tokens.next(), 1, 1 << 10).context(format!("new projects: v_{}", i))?;
            new_projects.push(Project { initial_h: h, h, v });
        }

        let mut initial_cards = vec![];
        for i in 0..n {
            let ty: usize =
                read(tokens.next(), 0, 4).context(format!("initial cards: t_init_{}", i))?;
            let w: i64 =
                read(tokens.next(), 0, 50).context(format!("initial cards: w_init_{}", i))?;
            initial_cards.push(Card {
                ty: CardType::new(ty),
                w,
                p: 0,
            });
        }

        let mut new_cards = vec![];
        for i in 0..t {
            new_cards.push(vec![]);
            for j in 0..k {
                let ty: usize =
                    read(tokens.next(), 0, 4).context(format!("new cards: t_{}_{}", i, j))?;
                let w: i64 =
                    read(tokens.next(), 0, 50).context(format!("new cards: w_{}_{}", i, j))?;
                let p: i64 =
                    read(tokens.next(), 0, 10000).context(format!("new cards: p_{}_{}", i, j))?;
                new_cards[i].push(Card {
                    ty: CardType::new(ty),
                    w,
                    p,
                });
            }
        }

        Ok(JudgeData {
            n,
            m,
            k,
            t,
            initial_projects,
            new_projects,
            initial_cards,
            new_cards,
        })
    }
}

pub struct JudgeResult {
    pub score: i64,
}

#[derive(Clone)]
pub struct FieldData {
    projects: Vec<Project>,
    l: i64,
    money: i64,
}

#[derive(Clone)]
pub struct VisData {
    comments: Vec<String>,
    field_before_use: FieldData,
    field_after_use: FieldData,
    cards: Vec<Card>,
    candidates: Vec<Card>,
    selected_card: usize,
    selected_project: usize,
    selected_candidate: usize,
    finished_projects: Vec<bool>,
    canceled_projects: Vec<bool>,
}

impl VisData {
    pub fn draw_svg(&self, before_use: bool) -> SVG {
        let mut svg_drawer = SVGDrawer::new(&self, before_use);
        svg_drawer.draw_projects(self, before_use);
        svg_drawer.draw_hands(self, before_use);
        svg_drawer.draw_badges(self, before_use);
        svg_drawer.draw_money(self, before_use);
        svg_drawer.draw_candidates(self, before_use);
        svg_drawer.svg
    }
}

#[derive(Debug, Clone)]
struct State {
    n: usize,
    m: usize,
    k: usize,
    max_turn: usize,
    turn: usize,
    cards: Vec<Card>,
    projects: Vec<Project>,
    new_cards: Vec<Vec<Card>>,
    new_projects: VecDeque<Project>,
    l: i64,
    money: i64,
}

impl State {
    fn new(data: JudgeData) -> Self {
        State {
            n: data.n,
            m: data.m,
            k: data.k,
            max_turn: data.t,
            turn: 0,
            cards: data.initial_cards,
            projects: data.initial_projects,
            new_cards: data.new_cards,
            new_projects: data.new_projects.into_iter().collect(),
            l: 0,
            money: 0,
        }
    }

    fn update_project(&mut self, m: usize) {
        let project = self.new_projects.pop_front().unwrap();
        self.projects[m] = Project {
            initial_h: project.initial_h * (1 << self.l),
            h: project.h * (1 << self.l),
            v: project.v * (1 << self.l),
        };
    }

    fn get_card_candidate(&self) -> Vec<Card> {
        let mut cards = self.new_cards[self.turn].clone();
        for card in cards.iter_mut() {
            card.w *= 1 << self.l;
            card.p *= 1 << self.l;
        }
        cards
    }

    fn increment_l(&mut self) -> Result<()> {
        if self.l >= 20 {
            bail!("L must be less than or equal to 20");
        }
        self.l += 1;
        Ok(())
    }

    fn use_card(&mut self, card: Card, m: usize, vis_data: &mut VisData) -> Result<()> {
        match card.ty {
            CardType::WorkSingle => {
                let project = &mut self.projects[m];
                project.h -= card.w;
                if project.h <= 0 {
                    self.money += project.v;
                    self.update_project(m);
                    vis_data.finished_projects[m] = true;
                }
            }
            CardType::WorkAll => {
                for i in 0..self.m {
                    let project = &mut self.projects[i];
                    project.h -= card.w;
                    if project.h <= 0 {
                        self.money += project.v;
                        self.update_project(i);
                        vis_data.finished_projects[i] = true;
                    }
                }
            }
            CardType::CancelSingle => {
                self.update_project(m);
                vis_data.canceled_projects[m] = true;
            }
            CardType::CancelAll => {
                for i in 0..self.m {
                    self.update_project(i);
                    vis_data.canceled_projects[i] = true;
                }
            }
            CardType::Invest => self.increment_l()?,
        }
        Ok(())
    }

    fn play_turn<R: Read, W: Write>(
        &mut self,
        buf_reader: &mut BufReader<R>,
        buf_writer: &mut BufWriter<W>,
    ) -> Result<VisData> {
        let mut vis_data = VisData {
            comments: vec![],
            field_before_use: FieldData {
                projects: self.projects.clone(),
                l: self.l,
                money: self.money,
            },
            field_after_use: FieldData {
                projects: vec![],
                l: i64::MAX,
                money: i64::MAX,
            },
            cards: self.cards.clone(),
            candidates: vec![],
            selected_card: usize::MAX,
            selected_project: usize::MAX,
            selected_candidate: usize::MAX,
            finished_projects: vec![false; self.m],
            canceled_projects: vec![false; self.m],
        };
        // Use card
        let line = read_line_with_comments(buf_reader, &mut vis_data.comments)?;
        let mut tokens = line.split_whitespace();
        let c = read(tokens.next(), 0, self.n - 1).context("c")?;
        let m = read(tokens.next(), 0, self.m - 1).context("m")?;
        if let Some(_) = tokens.next() {
            bail!("use card: Too many tokens");
        }
        let card = self.cards[c];
        if card.ty != CardType::WorkSingle && card.ty != CardType::CancelSingle && m != 0 {
            bail!("m must be 0");
        }
        vis_data.selected_card = c;
        vis_data.selected_project = m;
        self.use_card(card, m, &mut vis_data)?;
        vis_data.field_after_use = FieldData {
            projects: self.projects.clone(),
            l: self.l,
            money: self.money,
        };

        // Output project info
        for project in self.projects.iter() {
            writeln!(buf_writer, "{} {}", project.h, project.v)?;
            buf_writer.flush()?;
        }

        // Output money
        writeln!(buf_writer, "{}", self.money)?;
        buf_writer.flush()?;

        // Output card candidate
        let cards = self.get_card_candidate();
        for card in cards.iter() {
            writeln!(buf_writer, "{} {} {}", card.ty as usize, card.w, card.p)?;
            buf_writer.flush()?;
        }
        vis_data.candidates = cards.clone();

        // Input drawing card
        let line = read_line_with_comments(buf_reader, &mut vis_data.comments)?;
        let mut tokens = line.split_whitespace();
        let r = read(tokens.next(), 0, self.k - 1).context("r")?;
        if let Some(_) = tokens.next() {
            bail!("draw card: Too many tokens");
        }
        vis_data.selected_candidate = r;

        // update card info
        let card = cards[r];
        if card.p > self.money {
            bail!("Not enough money");
        }
        self.money -= card.p;
        self.cards[c] = card;

        self.turn += 1;
        Ok(vis_data)
    }
}

pub fn judge(
    data: &JudgeData,
    reader: &mut impl Read,
    writer: &mut impl Write,
    vis_data_vec: &mut Vec<VisData>,
) -> Result<JudgeResult> {
    let mut buf_reader = BufReader::new(reader);
    let mut buf_writer = BufWriter::new(writer);

    writeln!(buf_writer, "{} {} {} {}", data.n, data.m, data.k, data.t)?;
    buf_writer.flush()?;

    for card in data.initial_cards.iter() {
        writeln!(buf_writer, "{} {}", card.ty as usize, card.w)?;
        buf_writer.flush()?;
    }

    for project in data.initial_projects.iter() {
        writeln!(buf_writer, "{} {}", project.h, project.v)?;
        buf_writer.flush()?;
    }

    let mut state = State::new(data.clone());
    while state.turn < state.max_turn {
        let vis_data = state
            .play_turn(&mut buf_reader, &mut buf_writer)
            .with_context(|| format!("turn {}", state.turn))?;
        vis_data_vec.push(vis_data);
    }

    Ok(JudgeResult { score: state.money })
}

fn read_line_with_comments(
    buf_reader: &mut BufReader<impl Read>,
    comments: &mut Vec<String>,
) -> Result<String> {
    loop {
        let mut line = String::new();
        buf_reader.read_line(&mut line)?;

        if line.starts_with("#") {
            line = line.strip_prefix("#").unwrap().trim().to_string();
            comments.push(line);
        } else {
            return Ok(line);
        }
    }
}

fn read<T: Copy + PartialOrd + std::fmt::Display + std::str::FromStr>(
    token: Option<&str>,
    lb: T,
    ub: T,
) -> Result<T> {
    if let Some(v) = token {
        if let Ok(v) = v.parse::<T>() {
            if v < lb || ub < v {
                bail!("Out of range: {}", v);
            } else {
                Ok(v)
            }
        } else {
            bail!("Parse error: {}", v);
        }
    } else {
        bail!("Unexpected EOF");
    }
}

fn generate_project(rng: &mut ChaCha20Rng) -> Project {
    let b = rng.gen_range(2.0f64..=8.0);
    let h = 2.0f64.powf(b).round() as i64;
    let normal_dist = Normal::<f64>::new(b, 0.5).unwrap();
    let v = 2.0f64
        .powf(normal_dist.sample(rng).clamp(0.0, 10.0))
        .round() as i64;
    Project { initial_h: h, h, v }
}

fn generate_card(rng: &mut ChaCha20Rng, m: usize, x: &Vec<i64>) -> Card {
    let ty = CardType::generate(rng, x);
    let mut w = 0;
    let mut p;
    match ty {
        CardType::WorkSingle => {
            w = rng.gen_range(1i64..=50);
            let mu = w as f64;
            let normal_dist = Normal::<f64>::new(mu, mu / 3.0).unwrap();
            p = normal_dist.sample(rng).round() as i64;
            p = p.clamp(1, 10000);
        }
        CardType::WorkAll => {
            w = rng.gen_range(1i64..=50);
            let mu = w as f64 * m as f64;
            let normal_dist = Normal::<f64>::new(mu, mu / 3.0).unwrap();
            p = normal_dist.sample(rng).round() as i64;
            p = p.clamp(1, 10000);
        }
        CardType::CancelSingle => p = rng.gen_range(0i64..=10),
        CardType::CancelAll => p = rng.gen_range(0i64..=10),
        CardType::Invest => p = rng.gen_range(200i64..=1000),
    }

    Card { ty, w, p }
}

pub fn gen(seed: u64, n: Option<usize>, m: Option<usize>, k: Option<usize>) -> JudgeData {
    let mut rng = ChaCha20Rng::seed_from_u64(seed ^ 94);

    // Don't pass usize or isize ranges to gen_range
    // This leads to non-reproducible results between 64-bit targets and 32-bit targets (e.g. Wasm)
    let n = n.unwrap_or(rng.gen_range(2..=7 as u64) as usize);
    let m = m.unwrap_or(rng.gen_range(2..=8 as u64) as usize);
    let k = k.unwrap_or(rng.gen_range(2..=5 as u64) as usize);
    let t = 1000;

    // Generate parameter
    let r: Vec<i64> = vec![20, 10, 10, 5, 3];
    let x: Vec<i64> = r.iter().map(|&r| rng.gen_range(1..=r)).collect();

    // initial project
    let mut initial_projects = vec![];
    for _ in 0..m {
        initial_projects.push(generate_project(&mut rng));
    }

    // M * T project's information (before capital increase)
    let mut new_projects = Vec::new();
    for _ in 0..m * t {
        new_projects.push(generate_project(&mut rng));
    }

    let mut initial_cards = vec![];
    for _ in 0..n {
        let mut card = generate_card(&mut rng, m, &x);
        // No need to draw initial cards
        card.p = 0;
        initial_cards.push(card);
    }

    // K * T card's information (before capital increase)
    let mut new_cards = vec![];
    for i in 0..t {
        new_cards.push(vec![]);
        new_cards[i].push(Card {
            ty: CardType::WorkSingle,
            w: 1,
            p: 0,
        });
        for _ in 1..k {
            new_cards[i].push(generate_card(&mut rng, m, &x));
        }
    }

    JudgeData {
        n,
        m,
        k,
        t,
        initial_projects,
        new_projects,
        initial_cards,
        new_cards,
    }
}

#[cfg(target_arch = "wasm32")]
#[wasm_bindgen]
pub fn generate(
    seed: u64,
    n: Option<usize>,
    m: Option<usize>,
    k: Option<usize>,
) -> Result<String, JsError> {
    let n = n.filter(|&n| n != 0);
    let m = m.filter(|&m| m != 0);
    let k = k.filter(|&k| k != 0);
    Ok(gen(seed, n, m, k).to_string())
}

#[cfg_attr(target_arch = "wasm32", wasm_bindgen(getter_with_clone))]
pub struct SolInfo {
    pub error: Option<String>,
    pub score: u64,
    pub max_turn: usize,
}

#[cfg(target_arch = "wasm32")]
#[derive(Clone)]
struct VisCache {
    error: Option<String>,
    vis_data_vec: Vec<VisData>,
}

#[cfg(target_arch = "wasm32")]
static VIS_CACHE: Lazy<Mutex<Option<VisCache>>> = Lazy::new(|| Mutex::new(None));

#[cfg(target_arch = "wasm32")]
#[wasm_bindgen]
pub fn get_sol_info(input: &str, output: &str) -> Result<SolInfo, JsError> {
    let judge_data = input
        .to_string()
        .parse()
        .map_err(|e| JsError::new(&format!("{:#}", e)))?;
    let output = output.to_string();
    let mut reader = std::io::Cursor::new(output.as_bytes());
    let mut writer = std::io::sink();
    let mut vis_data_vec = vec![];
    let res = judge(&judge_data, &mut reader, &mut writer, &mut vis_data_vec);

    match res {
        Ok(res) => {
            *VIS_CACHE.lock().unwrap() = Some(VisCache {
                error: None,
                vis_data_vec: vis_data_vec.clone(),
            });

            let sol_info = SolInfo {
                error: None,
                score: res.score as u64,
                max_turn: vis_data_vec.len(),
            };
            Ok(sol_info)
        }
        Err(err) => {
            *VIS_CACHE.lock().unwrap() = Some(VisCache {
                error: Some(format!("{:#}", err)),
                vis_data_vec: vis_data_vec.clone(),
            });

            let sol_info = SolInfo {
                error: Some(format!("{:#}", err)),
                score: 0,
                max_turn: vis_data_vec.len() + 1,
            };
            Ok(sol_info)
        }
    }
}

#[cfg_attr(target_arch = "wasm32", wasm_bindgen(getter_with_clone))]
pub struct VisResult {
    pub svg: String,
    pub comments: Vec<String>,
}

#[cfg(target_arch = "wasm32")]
#[wasm_bindgen]
pub fn visualize(
    _input: &str,
    _output: &str,
    before_use: bool,
    t: usize,
) -> Result<VisResult, JsError> {
    console_error_panic_hook::set_once();

    let VisCache {
        error,
        vis_data_vec,
    } = VIS_CACHE.lock().unwrap().clone().unwrap();

    if t <= vis_data_vec.len() {
        let vis_data = &vis_data_vec[t - 1];

        Ok(VisResult {
            svg: vis_data.draw_svg(before_use).to_string(),
            comments: vis_data.comments.clone(),
        })
    } else {
        Err(JsError::new(&format!("{:#}", error.unwrap())))
    }
}
