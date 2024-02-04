use std::{
    io::{self, Read, Write},
    process::Stdio,
};
use tools::*;

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

    let judge_data = {
        let mut judge_data_s = String::new();
        io::stdin().read_to_string(&mut judge_data_s).unwrap();

        judge_data_s.parse().unwrap_or_else(|e| {
            eprintln!("Failed to parse judge input: {:#}", e);
            std::process::exit(1)
        })
    };
    let mut reader = TeeReader {
        reader: p.stdout.as_mut().unwrap(),
        writer: io::stdout(),
    };
    let mut writer = p.stdin.as_mut().unwrap();
    let mut vis_data_vec = vec![];

    match judge(&judge_data, &mut reader, &mut writer, &mut vis_data_vec) {
        Ok(judge_result) => {
            eprintln!("Score = {}", judge_result.score);
        }
        Err(err) => {
            if let Ok(Some(status)) = p.try_wait() {
                if !status.success() {
                    eprintln!("Solver exited with error: {}", status);
                    std::process::exit(1);
                }
            }
            let _ = p.kill();

            eprintln!("{:#}", err);
            eprintln!("Score = 0");
        }
    }
}

struct TeeReader<R: Read, W: Write> {
    reader: R,
    writer: W,
}

impl<R: Read, W: Write> Read for TeeReader<R, W> {
    fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
        let n = self.reader.read(buf)?;
        self.writer.write_all(&buf[..n])?;
        Ok(n)
    }
}
