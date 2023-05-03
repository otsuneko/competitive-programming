use std::io::{prelude::*, BufReader, BufWriter};
use std::process::{ChildStdout, Stdio};
use tools::*;

fn read(stdout: &mut BufReader<ChildStdout>) -> Result<DigOp, String> {
    loop {
        let mut out = String::new();
        match stdout.read_line(&mut out) {
            Ok(0) | Err(_) => {
                return Err(format!("Your program has terminated unexpectedly"));
            }
            _ => (),
        }
        if out.trim().len() == 0 {
            continue;
        }
        print!("{}", out);
        if out.starts_with("#") {
            continue;
        }
        return out.parse::<DigOp>();
    }
}

fn exec(p: &mut std::process::Child) -> Result<Outcome, String> {
    let mut input = String::new();
    std::io::stdin().read_to_string(&mut input).unwrap();
    let input = input.parse::<TesterInput>()?;
    let mut stdin = BufWriter::new(p.stdin.take().unwrap());
    let mut stdout = BufReader::new(p.stdout.take().unwrap());

    let n = input.h.len();
    let w = input.sources.len();
    let k = input.sinks.len();
    writeln!(stdin, "{} {} {} {}", n, w, k, input.base_cost).map_err(|e| e.to_string())?;
    for (r, c) in input.sources.iter() {
        writeln!(stdin, "{} {}", r, c).map_err(|e| e.to_string())?;
    }
    for (r, c) in input.sinks.iter() {
        writeln!(stdin, "{} {}", r, c).map_err(|e| e.to_string())?;
    }
    stdin.flush().map_err(|e| e.to_string())?;

    let mut sim = Sim::new(&input);
    loop {
        let op = read(&mut stdout)?;
        let dig_res = sim.dig(&op);
        if let Ok(res) = dig_res {
            writeln!(stdin, "{}", res as usize).map_err(|e| e.to_string())?;
        } else {
            writeln!(stdin, "-1").map_err(|e| e.to_string())?;
        }
        stdin.flush().map_err(|e| e.to_string())?;
        if dig_res? == DigResult::ConditionsSatisfied {
            break;
        }
    }

    let (outcome, err) = sim.compute_score();
    if let Some(err) = err {
        Err(err)
    } else {
        Ok(outcome)
    }
}

fn main() {
    if std::env::args().len() < 2 {
        eprintln!(
            "Usage: {} <command> [<args>...]",
            std::env::args().nth(0).unwrap()
        );
        return;
    }
    let (command, args) = (
        std::env::args().nth(1).unwrap(),
        std::env::args().skip(2).collect::<Vec<_>>(),
    );

    let mut p = std::process::Command::new(command)
        .args(args)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .unwrap_or_else(|e| {
            eprintln!("failed to execute the command");
            eprintln!("{}", e);
            std::process::exit(1)
        });

    match exec(&mut p) {
        Ok(outcome) => {
            eprintln!("Total Cost = {}", outcome.total_cost);
        }
        Err(err) => {
            eprintln!("{}", err);
            p.kill().unwrap();
        }
    }
}
