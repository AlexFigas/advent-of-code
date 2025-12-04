use crate::utils::*;

pub fn run() {
    let input = read_input(0);
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}

fn part1(input: &str) -> &str {
    let words = input.split_whitespace();
    return words.into_iter().next().unwrap();
}

fn part2(input: &str) -> &str {
    let words = input.split_whitespace();
    return words.into_iter().last().unwrap();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let example = read_test_input(0);
        assert_eq!(part1(&example), "Rust");
    }

    #[test]
    fn test_part2() {
        let example = read_test_input(0);
        assert_eq!(part2(&example), "awesome");
    }
}
