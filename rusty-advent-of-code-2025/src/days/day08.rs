use crate::utils::*;

pub fn run() {
    let input = read_input(8);
    println!("Part 1: {}", part1(&input, 1000usize));
    println!("Part 2: {}", part2(&input));
}

fn part1(input: &str, k: usize) -> u128 {
    compute_product(input, k)
}

fn part2(input: &str) -> u128 {
    // Continue connecting closest pairs until all boxes are in one component.
    let pts: Vec<(i128, i128, i128)> = input
        .lines()
        .filter(|l| !l.trim().is_empty())
        .map(|l| {
            let parts: Vec<i128> = l.split(',').map(|p| p.trim().parse::<i128>().unwrap()).collect();
            (parts[0], parts[1], parts[2])
        })
        .collect();
    let n = pts.len();
    if n < 2 {
        return 0u128;
    }

    // build all pair distances (squared)
    let mut edges: Vec<(u128, usize, usize)> = Vec::new();
    edges.reserve(n * (n.saturating_sub(1)) / 2);
    for i in 0..n {
        for j in (i + 1)..n {
            let dx = pts[i].0 - pts[j].0;
            let dy = pts[i].1 - pts[j].1;
            let dz = pts[i].2 - pts[j].2;
            let dist2 = (dx * dx + dy * dy + dz * dz) as i128;
            edges.push((dist2 as u128, i, j));
        }
    }
    edges.sort_by_key(|e| e.0);

    // union-find
    let mut parent: Vec<usize> = (0..n).collect();
    let mut size: Vec<u128> = vec![1u128; n];
    fn find(parent: &mut [usize], x: usize) -> usize {
        let mut x0 = x;
        while parent[x0] != x0 {
            parent[x0] = parent[parent[x0]];
            x0 = parent[x0];
        }
        x0
    }

    let mut components = n;
    for &(_d, i, j) in edges.iter() {
        let ri = find(&mut parent, i);
        let rj = find(&mut parent, j);
        if ri != rj {
            // union by size
            if size[ri] < size[rj] {
                parent[ri] = rj;
                size[rj] += size[ri];
            } else {
                parent[rj] = ri;
                size[ri] += size[rj];
            }
            components -= 1;
            if components == 1 {
                // return product of X coordinates of the two junction boxes
                let xi = pts[i].0 as i128;
                let xj = pts[j].0 as i128;
                let prod = (xi * xj) as i128;
                return prod as u128;
            }
        }
    }

    0u128
}

fn compute_product(input: &str, k: usize) -> u128 {
    let pts: Vec<(i128, i128, i128)> = input
        .lines()
        .filter(|l| !l.trim().is_empty())
        .map(|l| {
            let parts: Vec<i128> = l.split(',').map(|p| p.trim().parse::<i128>().unwrap()).collect();
            (parts[0], parts[1], parts[2])
        })
        .collect();
    let n = pts.len();
    if n == 0 {
        return 0u128;
    }

    // build all pair distances (squared)
    let mut edges: Vec<(u128, usize, usize)> = Vec::new();
    edges.reserve(n * (n.saturating_sub(1)) / 2);
    for i in 0..n {
        for j in (i + 1)..n {
            let dx = pts[i].0 - pts[j].0;
            let dy = pts[i].1 - pts[j].1;
            let dz = pts[i].2 - pts[j].2;
            let dist2 = (dx * dx + dy * dy + dz * dz) as i128;
            edges.push((dist2 as u128, i, j));
        }
    }
    edges.sort_by_key(|e| e.0);

    // union-find
    let mut parent: Vec<usize> = (0..n).collect();
    let mut size: Vec<u128> = vec![1u128; n];
    fn find(parent: &mut [usize], x: usize) -> usize {
        let mut x0 = x;
        while parent[x0] != x0 {
            parent[x0] = parent[parent[x0]];
            x0 = parent[x0];
        }
        x0
    }

    let mut used = 0usize;
    for &( _d, i, j) in edges.iter() {
        if used >= k { break; }
        let ri = find(&mut parent, i);
        let rj = find(&mut parent, j);
        if ri != rj {
            // union by size
            if size[ri] < size[rj] {
                parent[ri] = rj;
                size[rj] += size[ri];
            } else {
                parent[rj] = ri;
                size[ri] += size[rj];
            }
        }
        used += 1;
    }

    // compute root sizes
    let mut comp: std::collections::HashMap<usize, u128> = std::collections::HashMap::new();
    for i in 0..n {
        let r = find(&mut parent, i);
        *comp.entry(r).or_insert(0) += 1u128;
    }

    let mut sizes: Vec<u128> = comp.values().copied().collect();
    sizes.sort_unstable_by(|a,b| b.cmp(a));
    let mut prod: u128 = 1;
    for i in 0..3.min(sizes.len()) {
        prod = prod.saturating_mul(sizes[i]);
    }
    prod
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let example = read_test_input(8);
        assert_eq!(part1(&example, 10usize), 40u128);
    }

    #[test]
    fn test_part2() {
        let example = read_test_input(8);
        assert_eq!(part2(&example), 25272u128);
    }
}
