mod days;
mod utils;
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    let day = args.get(1).map(|s| s.parse::<u8>().unwrap_or(0)).unwrap_or(0);

    match day {
        0 => days::day00::run(),
        1 => days::day01::run(),
        2 => days::day02::run(),
        3 => days::day03::run(),
        _ => eprintln!("Usage: cargo run <day>"),
    }
}
