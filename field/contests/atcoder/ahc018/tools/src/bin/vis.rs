use tools::*;

fn main() {
    if std::env::args().len() != 3 {
        eprintln!(
            "Usage: {} <tester input> <tester output>",
            std::env::args().nth(0).unwrap()
        );
        return;
    }
    let in_file = std::env::args().nth(1).unwrap();
    let in_data = std::fs::read_to_string(&in_file).unwrap_or_else(|_| {
        eprintln!("no such file: {}", in_file);
        std::process::exit(1);
    });
    let out_file = std::env::args().nth(2).unwrap();
    let out_data = std::fs::read_to_string(&out_file).unwrap_or_else(|_| {
        eprintln!("no such file: {}", out_file);
        std::process::exit(1);
    });

    let vis_data = parse_visualize_data(&in_data, &out_data).unwrap();
    let sol_info = validate_sol(&vis_data);
    if let Some(err) = sol_info.error {
        eprintln!("{}", err);
    }
    eprintln!("Total Cost = {}", sol_info.total_cost);

    let (_, img) = vis(&vis_data, sol_info.max_turn);

    img.write_png("vis.png").unwrap();
}
