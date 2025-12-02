use crate::utils::read_input;

pub fn run() {
    let input = read_input(1);
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}

fn part1(input: &str) -> usize {
    let mut position: i32 = 50;
    let mut count = 0;
    
    for line in input.lines() {
        let line = line.trim();
        if line.is_empty() {
            continue;
        }
        
        let direction = line.chars().next().unwrap();
        let distance: i32 = line[1..].parse().unwrap();
        
        if direction == 'L' {
            position -= distance;
        } else {
            position += distance;
        }
        
        // Normalize to 0-99 range
        position = ((position % 100) + 100) % 100;
        
        if position == 0 {
            count += 1;
        }
    }
    
    count
}

fn part2(input: &str) -> usize {
    let mut position: i32 = 50;
    let mut count = 0;
    
    for line in input.lines() {
        let line = line.trim();
        if line.is_empty() {
            continue;
        }
        
        let direction = line.chars().next().unwrap();
        let distance: i32 = line[1..].parse().unwrap();
        
        if direction == 'L' {
            // Count how many times we pass through 0 when rotating left
            for _ in 0..distance {
                position -= 1;
                if position < 0 {
                    position += 100;
                }
                if position == 0 {
                    count += 1;
                }
            }
        } else {
            // Count how many times we pass through 0 when rotating right
            for _ in 0..distance {
                position += 1;
                if position >= 100 {
                    position -= 100;
                }
                if position == 0 {
                    count += 1;
                }
            }
        }
    }
    
    count
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn example_part1() {
        let example = read_test_input(1);
        assert_eq!(part1(&example), 3);
    }

    #[test]
    fn example_part2() {
        let example = read_test_input(1);
        assert_eq!(part2(&example), 6);
    }
}
