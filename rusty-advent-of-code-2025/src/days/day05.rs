use crate::utils::*;

pub fn run() {
    let input = read_input(5);
    let sum = part1(&input);
    println!("Part 1: {}", sum);
    println!("Part 2: {}", part2(&input));
}

fn part1(input: &str) -> u128 {
    // Split into ranges and ids by the blank line
    let mut parts = input.splitn(2, "\n\n");
    let ranges_part = parts.next().unwrap_or("");
    let ids_part = parts.next().unwrap_or("");

    let mut ranges: Vec<(u128,u128)> = Vec::new();
    for line in ranges_part.lines() {
        let line = line.trim();
        if line.is_empty() { continue; }
        if let Some((a,b)) = line.split_once('-') {
            let lo: u128 = a.trim().parse().unwrap();
            let hi: u128 = b.trim().parse().unwrap();
            ranges.push((lo, hi));
        }
    }

    if ranges.is_empty() { return 0; }

    // Merge ranges
    ranges.sort_by_key(|r| r.0);
    let mut merged: Vec<(u128,u128)> = Vec::new();
    for (lo, hi) in ranges {
        if let Some(last) = merged.last_mut() {
            if lo <= last.1 + 1 {
                if hi > last.1 { last.1 = hi; }
                continue;
            }
        }
        merged.push((lo, hi));
    }

    // For each id, check membership via binary search on merged ranges
    let mut count: u128 = 0;
    for line in ids_part.lines() {
        let line = line.trim();
        if line.is_empty() { continue; }
        let id: u128 = line.parse().unwrap();

        // binary search for range with start <= id
        let mut lo = 0usize;
        let mut hi = merged.len();
        while lo < hi {
            let mid = (lo + hi) / 2;
            if merged[mid].0 <= id {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        if lo == 0 { continue; }
        let idx = lo - 1;
        if merged[idx].0 <= id && id <= merged[idx].1 {
            count += 1;
        }
    }

    count
}

fn part2(input: &str) -> u128 {
    // Only consider the ranges section and count total distinct IDs covered
    let mut parts = input.splitn(2, "\n\n");
    let ranges_part = parts.next().unwrap_or("");

    let mut ranges: Vec<(u128,u128)> = Vec::new();
    for line in ranges_part.lines() {
        let line = line.trim();
        if line.is_empty() { continue; }
        if let Some((a,b)) = line.split_once('-') {
            let lo: u128 = a.trim().parse().unwrap();
            let hi: u128 = b.trim().parse().unwrap();
            ranges.push((lo, hi));
        }
    }

    if ranges.is_empty() { return 0; }

    ranges.sort_by_key(|r| r.0);
    let mut merged: Vec<(u128,u128)> = Vec::new();
    for (lo, hi) in ranges {
        if let Some(last) = merged.last_mut() {
            if lo <= last.1 + 1 {
                if hi > last.1 { last.1 = hi; }
                continue;
            }
        }
        merged.push((lo, hi));
    }

    let mut total: u128 = 0;
    for (lo, hi) in merged {
        total += hi - lo + 1;
    }
    total
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let example = read_test_input(5);
        assert_eq!(part1(&example), 3u128);
    }

    #[test]
    fn test_part2() {
        let example = read_test_input(5);
        assert_eq!(part2(&example), 14u128);
    }
}
