use crate::utils::read_input;

pub fn run() {
    let input = read_input(3);
    let sum = part1(&input);
    println!("Part 1: {}", sum);
    println!("Part 2: {}", part2(&input));
}

fn part1(input: &str) -> u128 {
    let mut total = 0u128;

    for line in input.lines() {
        let line = line.trim();
        if line.is_empty() {
            continue;
        }

        let digits: Vec<u8> = line
            .chars()
            .filter_map(|ch| ch.to_digit(10).map(|d| d as u8))
            .collect();

        let mut max_joltage = 0u128;

        // Try all pairs of positions
        for i in 0..digits.len() {
            for j in (i + 1)..digits.len() {
                let joltage = (digits[i] as u128) * 10 + (digits[j] as u128);
                max_joltage = max_joltage.max(joltage);
            }
        }

        total += max_joltage;
    }

    total
}

fn part2(input: &str) -> u128 {
    let mut total = 0u128;

    for line in input.lines() {
        let line = line.trim();
        if line.is_empty() {
            continue;
        }

        let digits: Vec<u8> = line
            .chars()
            .filter_map(|ch| ch.to_digit(10).map(|d| d as u8))
            .collect();

        if digits.len() < 12 {
            continue;
        }

        // Greedy approach: select 12 digits to maximize the resulting number
        // We need to select 12 positions such that the resulting 12-digit number is maximized
        let mut selected = Vec::new();
        let mut pos = 0; // next position to search from

        for step in 0..12 {
            // We need (12 - step) more digits including this one
            let remaining_needed = 12 - step;
            // Latest position we can start searching from
            let max_start = digits.len() - remaining_needed;

            // Find the position of the maximum digit in [pos, max_start]
            let mut best_digit = 0u8;
            let mut best_pos = pos;

            for i in pos..=max_start {
                if digits[i] > best_digit {
                    best_digit = digits[i];
                    best_pos = i;
                }
            }

            selected.push(best_digit);
            pos = best_pos + 1;
        }

        // Convert selected digits to a u128 number
        let mut joltage = 0u128;
        for digit in selected {
            joltage = joltage * 10 + (digit as u128);
        }

        total += joltage;
    }

    total
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let example = read_test_input(3);
        assert_eq!(part1(example), 357u128);
    }

    #[test]
    fn test_part2() {
        let example = read_test_input(3);
        assert_eq!(part2(example), 3121910778619u128);
    }
}
