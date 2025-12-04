use crate::utils::*;

pub fn run() {
    let input = read_input(4);
    let sum = part1(&input);
    println!("Part 1: {}", sum);
    println!("Part 2: {}", part2(&input));
}

fn part1(input: &str) -> u128 {
    let grid: Vec<Vec<char>> = input
        .lines()
        .map(|l| l.trim_end().chars().collect())
        .filter(|r: &Vec<char>| !r.is_empty())
        .collect();

    let h = grid.len();
    if h == 0 { return 0; }
    let w = grid[0].len();

    let mut count: u128 = 0;

    for y in 0..h {
        for x in 0..w {
            if grid[y][x] != '@' { continue; }

            let mut neigh = 0;
            for dy in -1i32..=1 {
                for dx in -1i32..=1 {
                    if dy == 0 && dx == 0 { continue; }
                    let ny = y as i32 + dy;
                    let nx = x as i32 + dx;
                    if ny >= 0 && ny < h as i32 && nx >= 0 && nx < w as i32 {
                        if grid[ny as usize][nx as usize] == '@' {
                            neigh += 1;
                        }
                    }
                }
            }

            if neigh < 4 {
                count += 1;
            }
        }
    }

    count
}

fn part2(input: &str) -> u128 {
    let mut grid: Vec<Vec<char>> = input
        .lines()
        .map(|l| l.trim_end().chars().collect())
        .filter(|r: &Vec<char>| !r.is_empty())
        .collect();

    let h = grid.len();
    if h == 0 { return 0; }
    let w = grid[0].len();

    let mut removed: u128 = 0;

    loop {
        let mut to_remove = Vec::new();

        for y in 0..h {
            for x in 0..w {
                if grid[y][x] != '@' { continue; }

                let mut neigh = 0;
                for dy in -1i32..=1 {
                    for dx in -1i32..=1 {
                        if dy == 0 && dx == 0 { continue; }
                        let ny = y as i32 + dy;
                        let nx = x as i32 + dx;
                        if ny >= 0 && ny < h as i32 && nx >= 0 && nx < w as i32 {
                            if grid[ny as usize][nx as usize] == '@' {
                                neigh += 1;
                            }
                        }
                    }
                }

                if neigh < 4 {
                    to_remove.push((y, x));
                }
            }
        }

        if to_remove.is_empty() {
            break;
        }

        for (y, x) in to_remove.iter() {
            if grid[*y][*x] == '@' {
                grid[*y][*x] = '.';
                removed += 1;
            }
        }
    }

    removed
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let example = read_test_input(4);
        assert_eq!(part1(&example), 13u128);
    }

    #[test]
    fn test_part2() {
        let example = read_test_input(4);
        assert_eq!(part2(&example), 43u128);
    }
}
