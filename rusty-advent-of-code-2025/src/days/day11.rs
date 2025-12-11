use crate::utils::*;

pub fn run() {
    let input = read_input(11);
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}

fn part1(input: &str) -> u128 {
    count_paths(input, "you", "out")
}

fn part2(input: &str) -> u128 {
    // Count paths from `svr` to `out` that visit both `dac` and `fft`.
    count_paths_required(input, "svr", "out", &["dac", "fft"])
}

fn count_paths(input: &str, start: &str, goal: &str) -> u128 {
    use std::collections::{HashMap, HashSet};

    let mut graph: HashMap<&str, Vec<&str>> = HashMap::new();

    for line in input.lines() {
        let line = line.trim();
        if line.is_empty() {
            continue;
        }
        if let Some((node, rest)) = line.split_once(':') {
            let node = node.trim();
            let neighbors: Vec<&str> = rest
                .split_whitespace()
                .map(|s| s.trim())
                .filter(|s| !s.is_empty())
                .collect();
            graph.insert(node, neighbors);
        }
    }

    fn dfs<'a>(
        graph: &HashMap<&'a str, Vec<&'a str>>,
        node: &'a str,
        goal: &str,
        visited: &mut HashSet<&'a str>,
    ) -> u128 {
        if node == goal {
            return 1;
        }
        if !graph.contains_key(node) {
            return 0;
        }
        // prevent cycles: only visit node once per path
        if !visited.insert(node) {
            return 0;
        }
        let mut total = 0u128;
        if let Some(neighs) = graph.get(node) {
            for &n in neighs.iter() {
                total += dfs(graph, n, goal, visited);
            }
        }
        visited.remove(node);
        total
    }

    let mut visited: HashSet<&str> = HashSet::new();
    dfs(&graph, start, goal, &mut visited)
}

fn count_paths_required(input: &str, start: &str, goal: &str, required: &[&str]) -> u128 {
    use std::collections::HashMap;

    let mut graph: HashMap<&str, Vec<&str>> = HashMap::new();

    for line in input.lines() {
        let line = line.trim();
        if line.is_empty() {
            continue;
        }
        if let Some((node, rest)) = line.split_once(':') {
            let node = node.trim();
            let neighbors: Vec<&str> = rest
                .split_whitespace()
                .map(|s| s.trim())
                .filter(|s| !s.is_empty())
                .collect();
            graph.insert(node, neighbors);
        }
    }

    // Map required nodes to bits
    let mut req_index: HashMap<&str, u8> = HashMap::new();
    for (i, &r) in required.iter().enumerate() {
        req_index.insert(r, i as u8);
    }
    let all_mask: u8 = ((1u8) << required.len()) - 1u8;

    let mut memo: HashMap<(&str, u8), u128> = HashMap::new();

    // recursive with current mask param
    fn dfs_mask<'a>(
        graph: &HashMap<&'a str, Vec<&'a str>>,
        node: &'a str,
        goal: &str,
        req_index: &HashMap<&'a str, u8>,
        all_mask: u8,
        cur_mask: u8,
        memo: &mut HashMap<(&'a str, u8), u128>,
    ) -> u128 {
        let mut mask = cur_mask;
        if let Some(&i) = req_index.get(node) {
            mask |= 1u8 << i;
        }

        let key = (node, mask);
        if let Some(&v) = memo.get(&key) {
            return v;
        }

        if node == goal {
            let res = if mask == all_mask { 1u128 } else { 0u128 };
            memo.insert(key, res);
            return res;
        }
        if !graph.contains_key(node) {
            memo.insert(key, 0u128);
            return 0u128;
        }

        let mut total = 0u128;
        for &n in graph.get(node).unwrap().iter() {
            total += dfs_mask(graph, n, goal, req_index, all_mask, mask, memo);
        }
        memo.insert(key, total);
        total
    }

    dfs_mask(&graph, start, goal, &req_index, all_mask, 0u8, &mut memo)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let example = read_test_input_part(11, 1);
        assert_eq!(part1(&example), 5u128);
    }

    #[test]
    fn test_part2() {
        let example = read_test_input_part(11, 2);
        assert_eq!(part2(&example), 2u128);
    }
}
