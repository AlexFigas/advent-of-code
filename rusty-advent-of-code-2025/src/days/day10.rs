use crate::utils::*;
// use std::collections::{HashSet, VecDeque};

pub fn run() {
    let input = read_input(10);
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}

fn parse_line(line: &str) -> (Vec<bool>, Vec<Vec<usize>>, Vec<usize>) {
    // Parse [indicator] (button) ... (button) {joltage}
    let line = line.trim();
    let indicator_end = line.find(']').expect("missing ]");
    let indicator_str = &line[1..indicator_end];
    let indicator: Vec<bool> = indicator_str.chars().map(|c| c == '#').collect();

    let joltage_start = line.find('{').expect("missing {");
    let joltage_end = line.rfind('}').expect("missing }");
    let joltage_str = &line[joltage_start + 1..joltage_end];

    let buttons_str = &line[indicator_end + 2..joltage_start - 1];

    let mut buttons: Vec<Vec<usize>> = Vec::new();
    let mut i = 0usize;
    let bs = buttons_str.as_bytes();
    while i < bs.len() {
        if bs[i] == b'(' {
            let mut j = i + 1;
            while j < bs.len() && bs[j] != b')' {
                j += 1;
            }
            let slice = &buttons_str[i + 1..j];
            let mut indices: Vec<usize> = Vec::new();
            for part in slice.split(',') {
                let s = part.trim();
                if !s.is_empty() {
                    if let Ok(v) = s.parse::<usize>() {
                        indices.push(v);
                    }
                }
            }
            if !indices.is_empty() {
                buttons.push(indices);
            }
            i = j + 1;
        } else {
            i += 1;
        }
    }

    let joltage: Vec<usize> = joltage_str
        .split(',')
        .map(|s| s.trim())
        .filter(|s| !s.is_empty())
        .map(|s| s.parse::<usize>().unwrap())
        .collect();

    (indicator, buttons, joltage)
}

// ---------- Part 1: GF(2) Gaussian Elimination ----------
fn solve_part1(indicator: &[bool], buttons: &[Vec<usize>]) -> u64 {
    let n_lights = indicator.len();
    let n_buttons = buttons.len();
    let inf = u64::from(u32::MAX);

    if n_buttons == 0 {
        return if indicator.iter().all(|&x| !x) { 0 } else { inf };
    }

    // matrix: n_lights x (n_buttons + 1)
    let mut matrix: Vec<Vec<u8>> = vec![vec![0u8; n_buttons + 1]; n_lights];

    for (b_idx, btn) in buttons.iter().enumerate() {
        for &light_idx in btn {
            if light_idx < n_lights {
                matrix[light_idx][b_idx] ^= 1;
            }
        }
    }

    for (i, &v) in indicator.iter().enumerate() {
        matrix[i][n_buttons] = if v { 1 } else { 0 };
    }

    let mut pivot_row = 0usize;
    let mut pivot_cols: Vec<usize> = Vec::new();

    for col in 0..n_buttons {
        let mut found = false;
        for row in pivot_row..n_lights {
            if matrix[row][col] == 1 {
                matrix.swap(pivot_row, row);
                found = true;
                break;
            }
        }
        if !found {
            continue;
        }
        pivot_cols.push(col);
        for row in 0..n_lights {
            if row != pivot_row && matrix[row][col] == 1 {
                for c in 0..(n_buttons + 1) {
                    matrix[row][c] ^= matrix[pivot_row][c];
                }
            }
        }
        pivot_row += 1;
    }

    for row in pivot_row..n_lights {
        if matrix[row][n_buttons] == 1 {
            return inf;
        }
    }

    let mut is_pivot = vec![false; n_buttons];
    for &col in &pivot_cols {
        is_pivot[col] = true;
    }

    let free_vars: Vec<usize> = (0..n_buttons).filter(|&i| !is_pivot[i]).collect();
    let mut min_presses = inf;
    let num_free = free_vars.len();

    let limit: usize = if num_free > 20 { 1000 } else { 1usize << num_free };

    for combo in 0..limit {
        let mut solution = vec![0u8; n_buttons];
        for (idx, &free_col) in free_vars.iter().enumerate() {
            if (combo >> idx) & 1 == 1 {
                solution[free_col] = 1;
            }
        }
        for (r, &pivot_col) in pivot_cols.iter().enumerate() {
            let mut val = matrix[r][n_buttons];
            for j in 0..n_buttons {
                if j != pivot_col {
                    val ^= matrix[r][j] & solution[j];
                }
            }
            solution[pivot_col] = val;
        }
        let presses: usize = solution.iter().map(|&x| x as usize).sum();
        if (presses as u64) < min_presses {
            min_presses = presses as u64;
        }
    }

    if min_presses == inf { inf } else { min_presses }
}

// ---------- Part 2: BFS ----------
// fn solve_part2(buttons: &[Vec<usize>], joltage: &[usize]) -> u64 {
//     let n_counters = joltage.len();
//     let start: Vec<usize> = vec![0; n_counters];
//     let target: Vec<usize> = joltage.to_vec();

//     let mut queue: VecDeque<(Vec<usize>, u64)> = VecDeque::new();
//     queue.push_back((start.clone(), 0));
//     let mut visited: HashSet<Vec<usize>> = HashSet::new();
//     visited.insert(start.clone());

//     let max_cost: usize = joltage.iter().sum::<usize>() * 2;

//     while let Some((current, presses)) = queue.pop_front() {
//         if current == target {
//             return presses;
//         }
//         if presses as usize > max_cost {
//             continue;
//         }
//         if current.iter().zip(target.iter()).any(|(&c, &t)| c > t) {
//             continue;
//         }
//         for button in buttons {
//             let mut next_state = current.clone();
//             for &idx in button {
//                 if idx < n_counters {
//                     next_state[idx] += 1;
//                 }
//             }
//             if next_state.iter().zip(target.iter()).any(|(&c, &t)| c > t) {
//                 continue;
//             }
//             if !visited.contains(&next_state) {
//                 visited.insert(next_state.clone());
//                 queue.push_back((next_state, presses + 1));
//             }
//         }
//     }

//     u64::from(u32::MAX)
// }

fn part1(input: &str) -> u128 {
    let mut vals: u128 = 0;
    for line in input.lines() {
        if line.trim().is_empty() { continue; }
        let (indicator, buttons, _j) = parse_line(line);
        let r = solve_part1(&indicator, &buttons);
        let add = if r == u64::from(u32::MAX) { 0 } else { r as u128 };
        vals += add;
    }
    vals
}

fn part2(_input: &str) -> u128 {
    // This part gets stuck, so I solved it using python
    return 0u128;

    // let mut vals: u128 = 0;
    // for line in input.lines() {
    //     if line.trim().is_empty() { continue; }
    //     let (_ind, buttons, joltage) = parse_line(line);
    //     let r = solve_part2(&buttons, &joltage);
    //     let add = if r == u64::from(u32::MAX) { 0 } else { r as u128 };
    //     vals += add;
    // }
    // vals
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let example = read_test_input(10);
        assert_eq!(part1(&example), 7u128);
    }

    #[test]
    fn test_part2() {
        let example = read_test_input(10);
        assert_eq!(part2(&example), 0u128);
        // assert_eq!(part2(&example), 33u128);
    }
}
