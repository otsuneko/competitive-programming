use std::io::{self, Cursor};

use tools::judge;

fn main() {
    if std::env::args().len() != 3 {
        eprintln!(
            "Usage: {} <input> <output>",
            std::env::args().nth(0).unwrap()
        );
        return;
    }
    let in_file = std::env::args().nth(1).unwrap();
    let out_file = std::env::args().nth(2).unwrap();
    let input = std::fs::read_to_string(&in_file).unwrap_or_else(|_| {
        eprintln!("no such file: {}", in_file);
        std::process::exit(1)
    });
    let output = std::fs::read_to_string(&out_file).unwrap_or_else(|_| {
        eprintln!("no such file: {}", out_file);
        std::process::exit(1)
    });

    let judge_data = input.parse().unwrap_or_else(|e| {
        eprintln!("Failed to parse judge input: {:#}", e);
        std::process::exit(1)
    });
    let mut reader = Cursor::new(output.as_bytes());
    let mut writer = io::sink();
    let mut vis_data_vec = vec![];

    let svg = match judge(&judge_data, &mut reader, &mut writer, &mut vis_data_vec) {
        Ok(judge_result) => {
            eprintln!("Score = {}", judge_result.score);

            let vis_data = vis_data_vec.last().unwrap();
            vis_data.draw_svg(false).to_string()
        }
        Err(err) => {
            eprintln!("{:#}", err);
            eprintln!("Score = 0");

            String::new()
        }
    };

    let vis = format!("<html><body>{}</body></html>", svg);
    std::fs::write("vis.html", &vis).unwrap();
}
