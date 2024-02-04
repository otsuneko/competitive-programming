#![allow(non_snake_case)]

use clap::Parser;
use std::{io::prelude::*, path::PathBuf};
use tools::*;

#[derive(Parser, Debug)]
struct Cli {
    /// Path to seeds.txt
    seeds: String,
    /// Path to input directory
    #[clap(short = 'd', long = "dir", default_value = "in")]
    dir: PathBuf,
    #[clap(short, long)]
    /// Print input details in csv format
    verbose: bool,
}

fn main() {
    let cli = Cli::parse();
    if !std::path::Path::new(&cli.dir).exists() {
        std::fs::create_dir(&cli.dir).unwrap();
    }
    let f = std::fs::File::open(&cli.seeds).unwrap_or_else(|_| {
        eprintln!("no such file: {}", cli.seeds);
        std::process::exit(1)
    });
    let f = std::io::BufReader::new(f);
    let mut id = 0;
    if cli.verbose {
        println!("file,seed,N,wall,var_d");
    }
    for line in f.lines() {
        let line = line.unwrap();
        let line = line.trim();
        if line.len() == 0 {
            continue;
        }
        let seed = line.parse::<u64>().unwrap_or_else(|_| {
            eprintln!("parse failed: {}", line);
            std::process::exit(1)
        });
        let input = gen(seed);
        if cli.verbose {
            let wall = input
                .h
                .iter()
                .chain(&input.v)
                .map(|c| c.iter().filter(|&&c| c == '1').count())
                .sum::<usize>();
            let avg_d = input.d.iter().map(|d| d.iter().sum::<i64>()).sum::<i64>() as f64 / (input.N * input.N) as f64;
            let avg_d2 =
                input.d.iter().map(|d| d.iter().map(|d| d * d).sum::<i64>()).sum::<i64>() as f64 / (input.N * input.N) as f64;
            println!("{:04},{},{},{},{:.0}", id, seed, input.N, wall, avg_d2 - avg_d);
        }
        let mut w = std::io::BufWriter::new(std::fs::File::create(cli.dir.join(format!("{:04}.txt", id))).unwrap());
        write!(w, "{}", input).unwrap();
        id += 1;
    }
}
