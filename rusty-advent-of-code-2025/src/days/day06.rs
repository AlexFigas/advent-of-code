use crate::utils::*;

pub fn run() {
    let input = read_input(6);
    let sum = part1(&input);
    println!("Part 1: {}", sum);
    println!("Part 2: {}", part2(&input));
}

fn part1(input: &str) -> u128 {
    let lines: Vec<&str> = input.lines().collect();
    if lines.is_empty() { return 0; }

    // Build a rectangular grid of chars, pad with spaces
    let maxw = lines.iter().map(|l| l.len()).max().unwrap_or(0);
    let mut grid: Vec<Vec<char>> = Vec::new();
    for &l in &lines {
        let mut row: Vec<char> = l.chars().collect();
        while row.len() < maxw {
            row.push(' ');
        }
        grid.push(row);
    }

    let h = grid.len();
    if h == 0 { return 0; }
    let w = maxw;

    // Identify separator columns: a column that is all spaces
    let mut sep = vec![false; w];
    for x in 0..w {
        let mut all_space = true;
        for y in 0..h {
            if grid[y][x] != ' ' {
                all_space = false;
                break;
            }
        }
        sep[x] = all_space;
    }

    // Group contiguous non-separator columns as problems
    let mut problems: Vec<(usize,usize)> = Vec::new();
    let mut x = 0usize;
    while x < w {
        // skip separators
        while x < w && sep[x] { x += 1; }
        if x >= w { break; }
        let start = x;
        while x < w && !sep[x] { x += 1; }
        let end = x; // exclusive
        problems.push((start, end));
    }

    let mut grand: u128 = 0;
    for (sx, ex) in problems {
        // last row contains operator
        let op_row = h - 1;
        let mut op_char = '+';
        for x in sx..ex {
            let c = grid[op_row][x];
            if c != ' ' {
                op_char = c;
                break;
            }
        }

        let mut nums: Vec<u128> = Vec::new();
        for y in 0..(h-1) {
            // collect characters in this problem columns
            let s: String = grid[y][sx..ex].iter().collect();
            let s = s.trim();
            if s.is_empty() { continue; }
            // s may contain spaces between numbers, but per problem each row corresponds to one number vertically
            // so after trim the remaining should be digits
            if let Ok(v) = s.parse::<u128>() {
                nums.push(v);
            }
        }

        if nums.is_empty() { continue; }
        let mut res: u128 = if op_char == '+' { 0 } else { 1 };
        for &n in &nums {
            if op_char == '+' { res += n; } else { res *= n; }
        }
        grand += res;
    }

    grand
}

fn part2(input: &str) -> u128 {
    let lines: Vec<&str> = input.lines().collect();
    if lines.is_empty() { return 0; }

    let maxw = lines.iter().map(|l| l.len()).max().unwrap_or(0);
    let mut grid: Vec<Vec<char>> = Vec::new();
    for &l in &lines {
        let mut row: Vec<char> = l.chars().collect();
        while row.len() < maxw { row.push(' '); }
        grid.push(row);
    }

    let h = grid.len();
    if h == 0 { return 0; }
    let w = maxw;

    // Identify separator columns
    let mut sep = vec![false; w];
    for x in 0..w {
        let mut all_space = true;
        for y in 0..h {
            if grid[y][x] != ' ' { all_space = false; break; }
        }
        sep[x] = all_space;
    }

    // Group contiguous non-separator columns as problems
    let mut problems: Vec<(usize,usize)> = Vec::new();
    let mut x = 0usize;
    while x < w {
        while x < w && sep[x] { x += 1; }
        if x >= w { break; }
        let start = x;
        while x < w && !sep[x] { x += 1; }
        let end = x;
        problems.push((start, end));
    }

    let mut grand: u128 = 0;
    for (sx, ex) in problems {
        // operator at bottom row
        let op_row = h - 1;
        let mut op_char = '+';
        for cx in sx..ex {
            let c = grid[op_row][cx];
            if c != ' ' { op_char = c; break; }
        }

        // For part2, numbers are columns, most significant digit at top.
        // Numbers are read right-to-left (columns from ex-1 down to sx).
        let mut nums: Vec<u128> = Vec::new();
        for cx in (sx..ex).rev() {
            // gather chars from top to h-2 (exclude operator row)
            let s: String = grid[0..(h-1)].iter().map(|row| row[cx]).collect();
            let s = s.trim();
            if s.is_empty() { continue; }
            if let Ok(v) = s.parse::<u128>() { nums.push(v); }
        }

        if nums.is_empty() { continue; }
        let mut res: u128 = if op_char == '+' { 0 } else { 1 };
        for &n in &nums {
            if op_char == '+' { res += n; } else { res *= n; }
        }
        grand += res;
    }

    grand
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let example = read_test_input(6);
        assert_eq!(part1(&example), 4277556u128);
    }

    #[test]
    fn test_part2() {
        let example = read_test_input(6);
        assert_eq!(part2(&example), 3263827u128);
    }
}
