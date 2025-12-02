use crate::utils::read_input;
use std::collections::HashSet;

pub fn run() {
    let input = read_input(2);
    let sum = part1(&input);
    println!("Part 1: {}", sum);
    println!("Part 2: {}", part2(&input));
}

fn ceil_div(a: u128, b: u128) -> u128 {
    if a == 0 {
        0
    } else {
        (a + b - 1) / b
    }
}

fn part1(input: &str) -> u128 {
    let mut total: u128 = 0;

    // Input is a single line containing comma-separated ranges
    for token in input.split(',') {
        let t = token.trim();
        if t.is_empty() {
            continue;
        }

        let parts: Vec<&str> = t.split('-').collect();
        if parts.len() != 2 {
            continue;
        }

        let a: u128 = parts[0].parse().unwrap();
        let b: u128 = parts[1].parse().unwrap();
        if a > b { continue; }

        // max digits length for numbers in this range
        let max_digits = ((b as f64).log10().floor() as usize) + 1;

        // For each possible half-length k (so total length 2k)
        for k in 1..=(max_digits / 2) {
            let ten_k: u128 = 10u128.pow(k as u32);
            let mult = ten_k + 1; // n = S * (10^k + 1)

            // S must be within [10^{k-1}, 10^{k}-1]
            let s_lo_bound = 10u128.pow((k - 1) as u32);
            let s_hi_bound = ten_k - 1;

            // S must also satisfy a <= S*mult <= b
            let s_min = ceil_div(a, mult);
            let s_max = b / mult;

            let s_low = std::cmp::max(s_lo_bound, s_min);
            let s_high = std::cmp::min(s_hi_bound, s_max);

            if s_low <= s_high {
                let count = s_high - s_low + 1;
                // sum_{S=s_low..s_high} S = (s_low + s_high) * count / 2
                let sum_s = (s_low + s_high) * count / 2;
                total += sum_s * mult;
            }
        }
    }

    total
}

fn part2(input: &str) -> u128 {
    let mut ids: HashSet<u128> = HashSet::new();

    for token in input.split(',') {
        let t = token.trim();
        if t.is_empty() { continue; }
        let parts: Vec<&str> = t.split('-').collect();
        if parts.len() != 2 { continue; }
        let a: u128 = parts[0].parse().unwrap();
        let b: u128 = parts[1].parse().unwrap();
        if a > b { continue; }

        let max_digits = ((b as f64).log10().floor() as usize) + 1;

        for k in 1..=max_digits {
            // r is repetition count, need r>=2 and k*r <= max_digits
            let max_r = max_digits / k;
            if max_r < 2 { continue; }

            let ten_k: u128 = 10u128.pow(k as u32);
            let s_lo_bound = if k == 1 { 1u128 } else { 10u128.pow((k - 1) as u32) };
            let s_hi_bound = ten_k - 1;

            for r in 2..=max_r {
                // compute multiplier M = sum_{i=0..r-1} 10^{k*i}
                let mut m: u128 = 0;
                let mut factor: u128 = 1;
                for _ in 0..r {
                    m += factor;
                    factor = factor.saturating_mul(ten_k);
                }

                if m == 0 { continue; }

                let s_min = ceil_div(a, m);
                let s_max = b / m;
                let s_low = std::cmp::max(s_lo_bound, s_min);
                let s_high = std::cmp::min(s_hi_bound, s_max);
                if s_low > s_high { continue; }

                for s in s_low..=s_high {
                    ids.insert(s * m);
                }
            }
        }
    }

    ids.into_iter().sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn example_part1() {
        let example = read_test_input(2);
        assert_eq!(part1(&example), 1227775554u128);
    }

    #[test]
    fn example_part2() {
        let example = read_test_input(2);
        assert_eq!(part2(&example), 4174379265u128);
    }
}
