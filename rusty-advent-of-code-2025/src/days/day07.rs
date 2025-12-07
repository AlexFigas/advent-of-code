use crate::utils::*;

pub fn run() {
    let input = read_input(7);
    let sum = part1(&input);
    println!("Part 1: {}", sum);
    println!("Part 2: {}", part2(&input));
}

fn part1(input: &str) -> u128 {
    use std::collections::HashMap;

    let grid: Vec<Vec<char>> = input.lines().map(|l| l.chars().collect()).collect();
    if grid.is_empty() {
        return 0u128;
    }
    let rows = grid.len();
    let cols = grid[0].len();

    // find S
    let mut start: Option<(usize, usize)> = None;
    for (r, row) in grid.iter().enumerate() {
        for (c, &ch) in row.iter().enumerate() {
            if ch == 'S' {
                start = Some((r, c));
                break;
            }
        }
        if start.is_some() {
            break;
        }
    }
    let (sr, sc) = match start {
        Some(p) => p,
        None => return 0u128,
    };

    // active beams at current row: column -> multiplicity
    let mut active: HashMap<usize, u128> = HashMap::new();
    active.insert(sc, 1u128);

    use std::collections::HashSet;
    let mut splits: u128 = 0;
    let mut seen_splitters: HashSet<(usize, usize)> = HashSet::new();

    // iterate rows from the row below S downwards
    for rr in (sr + 1)..rows {
        let mut next: HashMap<usize, u128> = HashMap::new();
        for (&c, &cnt) in active.iter() {
            // safety: c should be in bounds
            if c >= cols {
                continue;
            }
            match grid[rr][c] {
                '^' => {
                    // mark this splitter as hit (count once)
                    if !seen_splitters.contains(&(rr, c)) {
                        splits = splits.saturating_add(1);
                        seen_splitters.insert((rr, c));
                    }
                    if c > 0 {
                        *next.entry(c - 1).or_insert(0) += cnt;
                    }
                    if c + 1 < cols {
                        *next.entry(c + 1).or_insert(0) += cnt;
                    }
                }
                _ => {
                    *next.entry(c).or_insert(0) += cnt;
                }
            }
        }
        active = next;
        // if no active beams remain, we can stop early
        if active.is_empty() {
            break;
        }
    }

    splits
}

fn part2(input: &str) -> u128 {
    use std::collections::HashMap;

    let grid: Vec<Vec<char>> = input.lines().map(|l| l.chars().collect()).collect();
    if grid.is_empty() {
        return 0u128;
    }
    let rows = grid.len();
    let cols = grid[0].len();

    // find S
    let mut start: Option<(usize, usize)> = None;
    for (r, row) in grid.iter().enumerate() {
        for (c, &ch) in row.iter().enumerate() {
            if ch == 'S' {
                start = Some((r, c));
                break;
            }
        }
        if start.is_some() {
            break;
        }
    }
    let (sr, sc) = match start {
        Some(p) => p,
        None => return 0u128,
    };

    let mut memo: HashMap<(usize, usize), u128> = HashMap::new();

    fn dfs(
        grid: &Vec<Vec<char>>,
        rows: usize,
        cols: usize,
        r: usize,
        c: usize,
        memo: &mut HashMap<(usize, usize), u128>,
    ) -> u128 {
        if let Some(&v) = memo.get(&(r, c)) {
            return v;
        }
        let mut rr = r;
        while rr + 1 < rows {
            rr += 1;
            let ch = grid[rr][c];
            if ch == '^' {
                let mut total = 0u128;
                if c > 0 {
                    total = total.saturating_add(dfs(grid, rows, cols, rr, c - 1, memo));
                }
                if c + 1 < cols {
                    total = total.saturating_add(dfs(grid, rows, cols, rr, c + 1, memo));
                }
                memo.insert((r, c), total);
                return total;
            }
        }
        // reached bottom -> exited
        memo.insert((r, c), 1u128);
        1u128
    }

    dfs(&grid, rows, cols, sr, sc, &mut memo)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let example = read_test_input(7);
        assert_eq!(part1(&example), 21u128);
    }

    #[test]
    fn test_part2() {
        let example = read_test_input(7);
        assert_eq!(part2(&example), 40u128);
    }
}
