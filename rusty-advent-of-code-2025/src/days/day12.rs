use crate::utils::*;

pub fn run() {
    let input = read_input(12);
    println!("Part 1: {}", part1(&input));
}

fn part1(input: &str) -> u128 {
    let (presents, trees) = parse(input);

    let mut count = 0u128;
    for tree in trees.iter() {
        let mut total = 0usize;
        for (p, c) in presents.iter().zip(tree.counts.iter()) {
            total += p * (*c as usize);
        }
        let area = tree.size.0 * tree.size.1;
        if total <= area { count += 1; }
    }
    count
}

#[derive(Debug)]
struct Tree {
    size: (usize, usize),
    counts: Vec<usize>,
}

fn parse(input: &str) -> (Vec<usize>, Vec<Tree>) {
    // split into presents (shape blocks) and trees (region lines)
    let (presents_raw, trees_raw) = input.rsplit_once("\n\n").unwrap();

    let mut presents: Vec<usize> = Vec::new();
    for present in presents_raw.split("\n\n") {
        // skip leading line like '0:' and then grid rows
        if let Some(idx) = present.find('\n') {
            let raw = present[idx..].trim();
            let cnt = raw.chars().filter(|&ch| ch == '#').count();
            presents.push(cnt);
        }
    }

    let mut trees: Vec<Tree> = Vec::new();
    for line in trees_raw.lines() {
        let line = line.trim();
        if line.is_empty() { continue; }
        if let Some((size, rest)) = line.split_once(':') {
            if let Some((w, h)) = size.split_once('x') {
                let w = w.trim().parse::<usize>().unwrap();
                let h = h.trim().parse::<usize>().unwrap();
                let counts = rest
                    .split_whitespace()
                    .map(|s| s.trim().parse::<usize>().unwrap_or(0usize))
                    .collect::<Vec<usize>>();
                trees.push(Tree { size: (w, h), counts });
            }
        }
    }
    (presents, trees)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let example = read_test_input(12);
        assert_eq!(part1(&example), 2u128);
    }

}
