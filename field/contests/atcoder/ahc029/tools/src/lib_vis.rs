use svg::node::element::Text as TextElement;
use svg::node::element::SVG;
use svg::node::element::{Group, Path, Rectangle};
use svg::node::{Comment, Text};

use crate::{Card, CardType, Project, VisData};

const W: f64 = 800.0;
const H: f64 = 600.0;
const PADDING: f64 = 20.0;
const STR_H: f64 = 40.0;
const CANVAS_FONT_SIZE: f64 = 20.0;

const LEGEND_FONT_SIZE: f64 = 12.0;
const LEGEND_ICON_SIZE: f64 = 20.0;

const HAND_X: f64 = 0.0;
const HAND_Y: f64 = STR_H;
const HAND_W: f64 = (W - PADDING * 2.0) / 3.0;
const HAND_H: f64 = H - STR_H;
const HAND_FONT_SIZE: f64 = 12.0;
const HAND_ICON_SIZE: f64 = 25.0;
const HAND_EMPHASIZE_STROKE: f64 = 5.0;

const PROJECT_X: f64 = HAND_X + HAND_W + PADDING;
const PROJECT_Y: f64 = HAND_Y;
const PROJECT_W: f64 = HAND_W;
const PROJECT_H: f64 = H - STR_H;
const PROJECT_FONT_SIZE: f64 = 10.0;

const CANDIDATE_X: f64 = PROJECT_X + PROJECT_W + PADDING;
const CANDIDATE_Y: f64 = HAND_Y;
const CANDIDATE_W: f64 = HAND_W;
const CANDIDATE_H: f64 = HAND_H * 3.0 / 4.0;
const CANDIDATE_FONT_SIZE: f64 = 10.0;
const CANDIDATE_ICON_SIZE: f64 = 20.0;
const CANDIDATE_EMPHASIZE_STROKE: f64 = 4.0;

const BADGE_X: f64 = CANDIDATE_X;
const BADGE_Y: f64 = CANDIDATE_Y + CANDIDATE_H + PADDING / 2.0 + STR_H;

const MONEY_X: f64 = CANDIDATE_X;
const MONEY_Y: f64 = BADGE_Y + PADDING / 2.0;

pub struct SVGDrawer {
    pub svg: SVG,
}

impl SVGDrawer {
    pub fn new(vis_data: &VisData, before_use: bool) -> SVGDrawer {
        let mut doc = svg::Document::new()
            .set("id", "vis")
            .set(
                "viewBox",
                (-PADDING, -PADDING, W + 2.0 * PADDING, H + 2.0 * PADDING),
            )
            .set("width", W + 2.0 * PADDING)
            .set("height", H + 2.0 * PADDING);

        // draw base canvas
        doc = doc.add(
            Rectangle::new()
                .set("x", -PADDING)
                .set("y", -PADDING)
                .set("width", W + 2.0 * PADDING)
                .set("height", H + 2.0 * PADDING)
                .set("fill", "white")
                .set("stroke-width", "0.0"),
        );

        let mut res = SVGDrawer { svg: doc };

        // Draw canvas for project
        res.svg = res.svg.add(Self::rect(
            PROJECT_X, PROJECT_Y, PROJECT_W, PROJECT_H, None, None,
        ));
        res.add_text(
            "projects",
            PROJECT_X,
            PROJECT_Y - STR_H + PADDING / 2.0,
            CANVAS_FONT_SIZE,
            None,
            None,
            None,
        );

        // Draw canvas for hand
        res.svg = res
            .svg
            .add(Self::rect(HAND_X, HAND_Y, HAND_W, HAND_H, None, None));
        res.add_text(
            "hands",
            HAND_X,
            HAND_Y - STR_H + PADDING / 2.0,
            CANVAS_FONT_SIZE,
            None,
            None,
            None,
        );

        // Draw canvas for candidate
        res.svg = res.svg.add(Self::rect(
            CANDIDATE_X,
            CANDIDATE_Y,
            CANDIDATE_W,
            CANDIDATE_H,
            None,
            None,
        ));
        res.add_text(
            "candidates",
            CANDIDATE_X,
            CANDIDATE_Y - STR_H + PADDING / 2.0,
            CANVAS_FONT_SIZE,
            None,
            None,
            None,
        );

        // Draw badge
        res.draw_badges(vis_data, before_use);

        res
    }

    fn get_color(val: i64, lb: i64, ub: i64) -> String {
        // white: #FFFFFF
        const START_RED: u8 = 0xFF;
        const START_GREEN: u8 = 0xFF;
        const START_BLUE: u8 = 0xFF;
        // orange: #FFA500
        const END_RED: u8 = 0xFF;
        const END_GREEN: u8 = 0xA5;
        const END_BLUE: u8 = 0x00;

        let rate = if lb == ub || val < lb {
            0.0
        } else if val > ub {
            1.0
        } else {
            let tmp = (val - lb) as f64 / (ub - lb) as f64;
            0.2 + 0.8 * tmp
        };
        let r = (START_RED as f64 - (START_RED - END_RED) as f64 * rate).round() as u8;
        let g = (START_GREEN as f64 - (START_GREEN - END_GREEN) as f64 * rate).round() as u8;
        let b = (START_BLUE as f64 - (START_BLUE - END_BLUE) as f64 * rate).round() as u8;

        let buf = [r, g, b];
        let str = buf.iter().map(|x| format!("{:02X}", x)).collect::<String>();
        "#".to_string() + &str
    }

    fn draw_project(&mut self, x: f64, y: f64, w: f64, h: f64, l: i64, project: &Project) {
        let max_w = 2.0f64.powf(8.0 + l as f64);
        let initial_cost = project.initial_h as f64;
        let cost = project.h as f64;
        let project_w = initial_cost / max_w * w;

        let max_v = 1i64 << (10 + l);
        let color = Self::get_color(project.v, 0, max_v);

        // Draw remaining cost
        self.svg = self.svg.clone().add(
            Rectangle::new()
                .set("x", x)
                .set("y", y)
                .set("width", cost / max_w * w)
                .set("height", h)
                .set("fill", color)
                .set("stroke", "whitesmoke"),
        );

        // Draw initial cost
        self.svg = self.svg.clone().add(
            Rectangle::new()
                .set("x", x)
                .set("y", y)
                .set("width", project_w)
                .set("height", h)
                .set("fill", "none")
                .set("stroke", "gray"),
        );

        let text_x = if (project.initial_h as f64) < max_w / 2.0 {
            x + project_w + PADDING
        } else {
            x + PADDING
        };

        // draw h as text
        self.add_text(
            format!(
                "h: {}/{}",
                Self::separate_by_comma(project.h),
                Self::separate_by_comma(project.initial_h),
            )
            .as_str(),
            text_x,
            y + h / 3.0,
            PROJECT_FONT_SIZE,
            None,
            Some("middle"),
            None,
        );

        // draw v as text
        self.add_text(
            format!("v: {}", Self::separate_by_comma(project.v)).as_str(),
            text_x,
            y + h * 2.0 / 3.0,
            PROJECT_FONT_SIZE,
            None,
            Some("middle"),
            None,
        );
    }

    // emphasize selected project
    fn emphasize_project(
        &mut self,
        x: f64,
        y: f64,
        w: f64,
        h: f64,
        l: i64,
        project: &Project,
        stroke: &str,
    ) {
        let max_w = 2.0f64.powf(8.0 + l as f64);
        let initial_cost = project.initial_h as f64;
        let project_w = initial_cost / max_w * w;
        self.svg = self.svg.clone().add(
            Rectangle::new()
                .set("x", x)
                .set("y", y)
                .set("width", project_w)
                .set("height", h)
                .set("fill", "none")
                .set("stroke", stroke)
                .set("stroke-width", "3"),
        );
    }

    pub fn draw_projects(&mut self, vis_data: &VisData, before_use: bool) {
        let project_elm_w = Self::get_width_per_element(PROJECT_W, 1, PADDING);
        let project_elm_h = Self::get_width_per_element(PROJECT_H, 8, PADDING);

        let m = if before_use {
            vis_data.field_before_use.projects.len()
        } else {
            vis_data.field_after_use.projects.len()
        };

        let l = if before_use {
            vis_data.field_before_use.l
        } else {
            vis_data.field_after_use.l
        };

        // Draw each projects in field_before_use
        let projects = if before_use {
            vis_data.field_before_use.projects.clone()
        } else {
            vis_data.field_after_use.projects.clone()
        };

        for i in 0..m {
            let x = PROJECT_X + PADDING;
            let y = PROJECT_Y + PADDING + i as f64 * (project_elm_h + PADDING);
            self.draw_project(x, y, project_elm_w, project_elm_h, l, &projects[i]);
        }

        // Emphasize selected project(s)
        if before_use {
            let selected_card = vis_data.cards[vis_data.selected_card];
            let color = match selected_card.ty {
                CardType::CancelSingle | CardType::CancelAll => "red",
                _ => "lime",
            };
            match selected_card.ty {
                CardType::WorkSingle | CardType::CancelSingle => {
                    let selected_project = vis_data.selected_project;
                    let x = PROJECT_X + PADDING;
                    let y =
                        PROJECT_Y + PADDING + selected_project as f64 * (project_elm_h + PADDING);
                    self.emphasize_project(
                        x,
                        y,
                        project_elm_w,
                        project_elm_h,
                        l,
                        &projects[selected_project],
                        color,
                    );
                }
                CardType::WorkAll | CardType::CancelAll => {
                    for i in 0..m {
                        let x = PROJECT_X + PADDING;
                        let y = PROJECT_Y + PADDING + i as f64 * (project_elm_h + PADDING);
                        self.emphasize_project(
                            x,
                            y,
                            project_elm_w,
                            project_elm_h,
                            l,
                            &projects[i],
                            color,
                        );
                    }
                }
                _ => (),
            }
        }
    }

    fn add_icon(&mut self, x: f64, y: f64, sz: f64, card_ty: &CardType) {
        // Using Matrial Icons created by Google (under Apache License 2.0: https://github.com/google/material-design-icons/blob/master/LICENSE)
        let path = match card_ty {
            CardType::WorkSingle => Path::new().set("d", "M480-480q-66 0-113-47t-47-113q0-66 47-113t113-47q66 0 113 47t47 113q0 66-47 113t-113 47ZM160-160v-112q0-34 17.5-62.5T224-378q62-31 126-46.5T480-440q66 0 130 15.5T736-378q29 15 46.5 43.5T800-272v112H160Z"),
            CardType::WorkAll => Path::new().set("d", "M0-240v-63q0-43 44-70t116-27q13 0 25 .5t23 2.5q-14 21-21 44t-7 48v65H0Zm240 0v-65q0-32 17.5-58.5T307-410q32-20 76.5-30t96.5-10q53 0 97.5 10t76.5 30q32 20 49 46.5t17 58.5v65H240Zm540 0v-65q0-26-6.5-49T754-397q11-2 22.5-2.5t23.5-.5q72 0 116 26.5t44 70.5v63H780ZM160-440q-33 0-56.5-23.5T80-520q0-34 23.5-57t56.5-23q34 0 57 23t23 57q0 33-23 56.5T160-440Zm640 0q-33 0-56.5-23.5T720-520q0-34 23.5-57t56.5-23q34 0 57 23t23 57q0 33-23 56.5T800-440Zm-320-40q-50 0-85-35t-35-85q0-51 35-85.5t85-34.5q51 0 85.5 34.5T600-600q0 50-34.5 85T480-480Z"),
            CardType::CancelSingle => Path::new().set("d","M160-400q0-105 50-187t110-138q60-56 110-85.5l50-29.5v132q0 37 25 58.5t56 21.5q17 0 32.5-7t28.5-23l18-22q72 42 116 116.5T800-400q0 88-43 160.5T644-125q17-24 26.5-52.5T680-238q0-40-15-75.5T622-377L480-516 339-377q-29 29-44 64t-15 75q0 32 9.5 60.5T316-125q-70-42-113-114.5T160-400Zm320-4 85 83q17 17 26 38t9 45q0 49-35 83.5T480-120q-50 0-85-34.5T360-238q0-23 9-44.5t26-38.5l85-83Z"),
            CardType::CancelAll  => Path::new().set("d","M346-48q-125 0-212.5-88.5T46-350q0-125 86.5-211.5T344-648h13l27-47q12-22 36-28.5t46 6.5l30 17 5-8q23-43 72-56t92 12l35 20-40 69-35-20q-14-8-30.5-3.5T570-668l-5 8 40 23q21 12 27.5 36t-5.5 45l-27 48q23 36 34.5 76.5T646-348q0 125-87.5 212.5T346-48Zm454-560v-80h120v80H800ZM580-828v-120h80v120h-80Zm195 81-56-56 85-85 56 56-85 85Z" ),
            CardType::Invest => Path::new().set("d", "M440-160v-487L216-423l-56-57 320-320 320 320-56 57-224-224v487h-80Z"),
        };
        let ratio = 960.0 / sz;
        self.svg = self.svg.clone().add(
            Group::new()
                .add(Comment::new("Using Matrial Icons created by Google (under Apache License 2.0: https://github.com/google/material-design-icons/blob/master/LICENSE)"))
                .add(path)
                .set(
                    "transform",
                    format!(
                        "scale({}) translate({}, {})",
                        1.0 / ratio,
                        (x - sz / 2.0) * ratio,
                        (y + sz / 2.0) * ratio,
                    ),
                )
                .set("fill", "black")
                .set("stroke", "black")
                .set("stroke-width", "1.0"),
        );
    }

    fn draw_card(
        &mut self,
        x: f64,
        y: f64,
        w: f64,
        h: f64,
        card: &Card,
        icon_size: f64,
        font_size: f64,
        color: Option<&str>,
    ) {
        // Outer frame
        // fill by color according to card type
        let card_color = Self::card_type_to_color(card.ty);
        let card_color = color.unwrap_or(card_color.as_str());
        self.svg = self
            .svg
            .clone()
            .add(Self::rect(x, y, w, h, Some(card_color), Some("gray")).set("rx", w * 0.1));

        let text_x = x + w / 2.0;
        // Draw weight
        if card.w != 0 {
            self.add_text(
                format!("w:{}", Self::separate_by_comma(card.w)).as_str(),
                text_x,
                y + h * 3.0 / 4.0,
                font_size,
                None,
                Some("middle"),
                Some("middle"),
            );
        }
        // Draw price
        self.add_text(
            format!("p:{}", Self::separate_by_comma(card.p)).as_str(),
            text_x,
            y + h * 3.0 / 5.0,
            font_size,
            None,
            Some("middle"),
            Some("middle"),
        );

        self.add_icon(text_x, y + h / 4.0, icon_size, &card.ty);
    }

    fn gray_out_candidate(&mut self, x: f64, y: f64, w: f64, h: f64) {
        self.svg = self
            .svg
            .clone()
            .add(Self::rect(x, y, w, h, Some("gray"), Some("gray")).set("rx", w * 0.1));
    }

    fn emphasize_card(&mut self, x: f64, y: f64, w: f64, h: f64, stroke: &str, stroke_width: f64) {
        self.svg = self.svg.clone().add(
            Rectangle::new()
                .set("x", x)
                .set("y", y)
                .set("rx", w * 0.1)
                .set("width", w)
                .set("height", h)
                .set("fill", "none")
                .set("stroke", stroke)
                .set("stroke-width", stroke_width),
        );
        self.svg = self.svg.clone().add(
            Rectangle::new()
                .set("x", x + stroke_width / 2.0)
                .set("y", y + stroke_width / 2.0)
                .set("rx", (w - stroke_width) * 0.1)
                .set("width", w - stroke_width)
                .set("height", h - stroke_width)
                .set("fill", "none")
                .set("stroke", "gray")
                .set("stroke-width", stroke_width / 3.0),
        );
    }

    fn add_legend(&mut self, x: f64, y: f64, card_ty: CardType) {
        let color = Self::card_type_to_color(card_ty);
        let card_color = color.as_str();

        let sz = LEGEND_ICON_SIZE * 1.2;
        let icon_pos = sz / 2.0;
        self.svg = self
            .svg
            .clone()
            .add(Self::rect(x, y, sz, sz, Some(card_color), Some("gray")));

        self.add_icon(x + icon_pos, y + sz / 2.0, LEGEND_ICON_SIZE, &card_ty);
    }

    pub fn draw_hands(&mut self, vis_data: &VisData, before_use: bool) {
        let hand_elm_w = Self::get_width_per_element(HAND_W, 2, PADDING);
        let hand_elm_h = hand_elm_w * 1.3;
        let hand_padding_h = (HAND_H - 4.0 * hand_elm_h) / 5.0;

        let n = vis_data.cards.len();
        let c = vis_data.selected_card;

        // Draw each cards
        for i in 0..n {
            let card_pos = ((i / 2) as f64, (i % 2) as f64);
            let x = HAND_X + card_pos.1 * (hand_elm_w + PADDING) + PADDING;
            let y = HAND_Y + card_pos.0 * (hand_elm_h + hand_padding_h) + hand_padding_h;
            let color = if i == c && !before_use {
                Some("gray")
            } else {
                None
            };
            self.draw_card(
                x,
                y,
                hand_elm_w,
                hand_elm_h,
                &vis_data.cards[i],
                HAND_ICON_SIZE,
                HAND_FONT_SIZE,
                color,
            );
        }

        if before_use {
            // Emphasize selected card
            let card_pos = ((c / 2) as f64, (c % 2) as f64);
            let x = HAND_X + card_pos.1 * (hand_elm_w + PADDING) + PADDING;
            let y = HAND_Y + card_pos.0 * (hand_elm_h + hand_padding_h) + hand_padding_h;
            let color = "lime";
            self.emphasize_card(x, y, hand_elm_w, hand_elm_h, color, HAND_EMPHASIZE_STROKE);
        }

        // Add legends
        let card_ty_vec = vec![
            CardType::WorkSingle,
            CardType::WorkAll,
            CardType::CancelSingle,
            CardType::CancelAll,
            CardType::Invest,
        ];
        let pos = (3.0, 1.0);
        let x = HAND_X + pos.1 * (hand_elm_w + PADDING) + PADDING;
        let y = HAND_Y + pos.0 * (hand_elm_h + hand_padding_h) + hand_padding_h;
        self.add_text(
            "Card type",
            x + hand_elm_w / 2.0,
            y + 10.0,
            LEGEND_FONT_SIZE,
            None,
            None,
            Some("middle"),
        );
        for i in 0..card_ty_vec.len() {
            let legend_pos = ((i / 2) as f64, (i % 2) as f64);
            let legend_x = x + hand_elm_w / 2.0 - 50.0 + legend_pos.1 * 50.0;
            let legend_y = y + 30.0 + hand_elm_h / card_ty_vec.len() as f64 * legend_pos.0 * 1.2;
            self.add_text(
                format!("{} :", card_ty_vec[i] as usize).as_str(),
                legend_x + 5.0,
                legend_y + LEGEND_ICON_SIZE * 1.2 / 2.0,
                LEGEND_FONT_SIZE,
                None,
                Some("middle"),
                None,
            );
            self.add_legend(legend_x + 2.0 * LEGEND_FONT_SIZE, legend_y, card_ty_vec[i])
        }
    }

    pub fn draw_candidates(&mut self, vis_data: &VisData, before_use: bool) {
        let hand_elm_w = Self::get_width_per_element(HAND_W, 2, PADDING);
        let hand_elm_h = hand_elm_w * 1.3;
        let hand_padding_h = (HAND_H - 4.0 * hand_elm_h) / 5.0;
        let candidate_elm_w = hand_elm_w;
        let candidate_elm_h = hand_elm_h;
        let candidate_padding_h = hand_padding_h;
        let candidate_padding_w = (CANDIDATE_W - 2.0 * candidate_elm_w) / 3.0;

        let k = vis_data.candidates.len();

        if before_use {
            for i in 0..k {
                let card_pos = ((i / 2) as f64, (i % 2) as f64);
                let x = CANDIDATE_X
                    + card_pos.1 * (candidate_elm_w + candidate_padding_w)
                    + candidate_padding_w;
                let y = CANDIDATE_Y
                    + card_pos.0 * (candidate_elm_h + candidate_padding_h)
                    + candidate_padding_h;
                self.gray_out_candidate(x, y, candidate_elm_w, candidate_elm_h);
            }
        } else {
            // Draw each candidates
            for i in 0..k {
                let card_pos = ((i / 2) as f64, (i % 2) as f64);
                let x = CANDIDATE_X
                    + card_pos.1 * (candidate_elm_w + candidate_padding_w)
                    + candidate_padding_w;
                let y = CANDIDATE_Y
                    + card_pos.0 * (candidate_elm_h + candidate_padding_h)
                    + candidate_padding_h;
                self.draw_card(
                    x,
                    y,
                    candidate_elm_w,
                    candidate_elm_h,
                    &vis_data.candidates[i],
                    CANDIDATE_ICON_SIZE,
                    CANDIDATE_FONT_SIZE,
                    None,
                );
            }

            // Emphasize selected candidate
            let r = vis_data.selected_candidate;
            let card_pos = ((r / 2) as f64, (r % 2) as f64);
            let x = CANDIDATE_X
                + card_pos.1 * (candidate_elm_w + candidate_padding_w)
                + candidate_padding_w;
            let y = CANDIDATE_Y
                + card_pos.0 * (candidate_elm_h + candidate_padding_h)
                + candidate_padding_h;
            let color = "lime";
            self.emphasize_card(
                x,
                y,
                candidate_elm_w,
                candidate_elm_h,
                color,
                CANDIDATE_EMPHASIZE_STROKE,
            );
        }
    }

    pub fn draw_badges(&mut self, vis_data: &VisData, before_use: bool) {
        let y = BADGE_Y - STR_H + PADDING / 2.0;
        self.add_text(
            format!("invests :").as_str(),
            BADGE_X,
            y + CANVAS_FONT_SIZE / 2.0,
            CANVAS_FONT_SIZE,
            None,
            Some("middle"),
            None,
        );

        let l = if before_use {
            vis_data.field_before_use.l
        } else {
            vis_data.field_after_use.l
        };

        self.add_legend(BADGE_X + 90.0, y - 3.0, CardType::Invest);

        self.add_text(
            format!("× {}", l).as_str(),
            BADGE_X + 125.0,
            y + CANVAS_FONT_SIZE / 2.0,
            CANVAS_FONT_SIZE,
            None,
            Some("middle"),
            None,
        );
    }

    pub fn draw_money(&mut self, vis_data: &VisData, before_use: bool) {
        let money = if before_use {
            vis_data.field_before_use.money
        } else {
            vis_data.field_after_use.money
        };
        let str = format!("MONEY : {}", Self::separate_by_comma(money));
        self.add_text(&str, MONEY_X, MONEY_Y, CANVAS_FONT_SIZE, None, None, None);
    }

    fn get_width_per_element(w: f64, n: usize, padding: f64) -> f64 {
        (w - (n as f64 + 1.0) * padding) / n as f64
    }

    fn rect(x: f64, y: f64, w: f64, h: f64, fill: Option<&str>, stroke: Option<&str>) -> Rectangle {
        let fill = fill.unwrap_or("white");
        let stroke = stroke.unwrap_or("black");
        Rectangle::new()
            .set("x", x)
            .set("y", y)
            .set("width", w)
            .set("height", h)
            .set("fill", fill)
            .set("stroke", stroke)
    }

    fn add_text(
        &mut self,
        str: &str,
        x: f64,
        y: f64,
        font_size: f64,
        fill: Option<&str>,
        dominant_baseline: Option<&str>,
        text_anchor: Option<&str>,
    ) {
        let fill = fill.unwrap_or("black");
        let dominant_baseline = dominant_baseline.unwrap_or("hanging");
        let text_anchor = text_anchor.unwrap_or("start");
        // draw text
        self.svg = self.svg.clone().add(
            TextElement::new()
                .add(Text::new(format!("{}", str)))
                .set("x", x)
                .set("y", y)
                .set("font-size", font_size)
                .set("font-family", "sans-serif")
                .set("fill", fill)
                .set("dominant-baseline", dominant_baseline)
                .set("text-anchor", text_anchor),
        );
    }

    fn separate_by_comma(num: i64) -> String {
        num.to_string()
            .chars()
            .rev()
            .collect::<Vec<_>>()
            .chunks(3)
            .map(|x| x.iter().collect::<String>())
            .collect::<Vec<_>>()
            .join(",")
            .chars()
            .rev()
            .collect::<String>()
    }

    fn card_type_to_color(card_type: CardType) -> String {
        match card_type {
            CardType::WorkSingle => "lightcyan".to_string(),
            CardType::WorkAll => "deepskyblue".to_string(),
            CardType::CancelSingle => "tomato".to_string(),
            CardType::CancelAll => "violet".to_string(),
            CardType::Invest => "gold".to_string(),
        }
    }
}
