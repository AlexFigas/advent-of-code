use crate::utils::*;

pub fn run() {
    let input = read_input(9);
    let sum = part1(&input);
    println!("Part 1: {}", sum);
    println!("Part 2: {}", part2(&input));
}

fn part1(input: &str) -> u128 {
    let pts: Vec<(i128, i128)> = input
        .lines()
        .filter(|l| !l.trim().is_empty())
        .map(|l| {
            let parts: Vec<i128> = l.split(',').map(|p| p.trim().parse::<i128>().unwrap()).collect();
            (parts[0], parts[1])
        })
        .collect();

    let n = pts.len();
    let mut best: u128 = 0u128;
    for i in 0..n {
        for j in (i + 1)..n {
            let (xi, yi) = pts[i];
            let (xj, yj) = pts[j];
            if xi == xj || yi == yj {
                continue;
            }
            let dx = (xi - xj).abs() as u128 + 1u128;
            let dy = (yi - yj).abs() as u128 + 1u128;
            let area = dx.saturating_mul(dy);
            if area > best {
                best = area;
            }
        }
    }
    best
}

fn part2(input: &str) -> u128 {
    let pts: Vec<(i128, i128)> = input
        .lines()
        .filter(|l| !l.trim().is_empty())
        .map(|l| {
            let parts: Vec<i128> = l.split(',').map(|p| p.trim().parse::<i128>().unwrap()).collect();
            (parts[0], parts[1])
        })
        .collect();
    let n = pts.len();
    if n == 0 {
        return 0u128;
    }

    let min_x = pts.iter().map(|(x,_)| *x).min().unwrap();
    let max_x = pts.iter().map(|(x,_)| *x).max().unwrap();
    let min_y = pts.iter().map(|(_,y)| *y).min().unwrap();
    let max_y = pts.iter().map(|(_,y)| *y).max().unwrap();

    let w = (max_x - min_x + 1) as usize;
    let h = (max_y - min_y + 1) as usize;

    // If the full bounding box is small, use the simpler grid+flood-fill approach (works for tests and small inputs).
    let area_check = (w as u128).saturating_mul(h as u128);
    if area_check <= 5_000_000u128 {
        // grid: 0 = empty, 1 = red, 2 = green
        let mut grid: Vec<Vec<u8>> = vec![vec![0u8; w]; h];
        // mark red
        for (x,y) in pts.iter() {
            let xi = (x - min_x) as usize;
            let yi = (y - min_y) as usize;
            grid[yi][xi] = 1;
        }

        // draw connecting lines (inclusive) between consecutive red tiles
        for i in 0..n {
            let (x1,y1) = pts[i];
            let (x2,y2) = pts[(i+1) % n];
            if x1 == x2 {
                let xi = (x1 - min_x) as usize;
                let y0 = (y1.min(y2) - min_y) as usize;
                let y1i = (y1.max(y2) - min_y) as usize;
                for yy in y0..=y1i {
                    if grid[yy][xi] == 0 { grid[yy][xi] = 2; }
                }
            } else if y1 == y2 {
                let yi = (y1 - min_y) as usize;
                let x0 = (x1.min(x2) - min_x) as usize;
                let x1i = (x1.max(x2) - min_x) as usize;
                for xx in x0..=x1i {
                    if grid[yi][xx] == 0 { grid[yi][xx] = 2; }
                }
            }
        }

        // flood fill from borders through empty cells to mark outside
        let mut outside = vec![vec![false; w]; h];
        let mut q: Vec<(usize,usize)> = Vec::new();
        for x in 0..w {
            if grid[0][x] == 0 { outside[0][x] = true; q.push((x,0)); }
            if grid[h-1][x] == 0 && h>1 { outside[h-1][x] = true; q.push((x,h-1)); }
        }
        for y in 0..h {
            if grid[y][0] == 0 { outside[y][0] = true; q.push((0,y)); }
            if grid[y][w-1] == 0 && w>1 { outside[y][w-1] = true; q.push((w-1,y)); }
        }
        while let Some((x,y)) = q.pop() {
            let neigh = [(-1isize,0),(1,0),(0,-1),(0,1)];
            for (dx,dy) in neigh.iter() {
                let nx = x as isize + dx;
                let ny = y as isize + dy;
                if nx>=0 && nx<(w as isize) && ny>=0 && ny<(h as isize) {
                    let ux = nx as usize; let uy = ny as usize;
                    if !outside[uy][ux] && grid[uy][ux]==0 {
                        outside[uy][ux]=true;
                        q.push((ux,uy));
                    }
                }
            }
        }

        // any cell that is '.' (0) and not outside is interior -> mark green (2)
        for y in 0..h {
            for x in 0..w {
                if grid[y][x]==0 && !outside[y][x] {
                    grid[y][x]=2;
                }
            }
        }

        // Now allowed cells are grid==1 or grid==2
        // Build prefix sum of allowed
        let mut pref = vec![vec![0u32; w+1]; h+1];
        for y in 0..h {
            for x in 0..w {
                let val = if grid[y][x] >= 1 { 1u32 } else { 0u32 };
                pref[y+1][x+1] = pref[y+1][x] + pref[y][x+1] - pref[y][x] + val;
            }
        }

        // collect red coordinates indices
        let mut reds: Vec<(usize,usize)> = Vec::new();
        for (x,y) in pts.iter() {
            reds.push(((x-min_x) as usize, (y-min_y) as usize));
        }

        let mut best: u128 = 0;
        let m = reds.len();
        for i in 0..m {
            for j in (i+1)..m {
                let (xi, yi) = reds[i];
                let (xj, yj) = reds[j];
                if xi==xj || yi==yj { continue; }
                let x0 = xi.min(xj);
                let x1i = xi.max(xj);
                let y0 = yi.min(yj);
                let y1i = yi.max(yj);
                let area = ((x1i - x0 + 1) * (y1i - y0 + 1)) as u32;
                let sum_allowed = pref[y1i+1][x1i+1] as i64 - pref[y0][x1i+1] as i64 - pref[y1i+1][x0] as i64 + pref[y0][x0] as i64;
                if sum_allowed as u32 == area {
                    if (area as u128) > best { best = area as u128; }
                }
            }
        }
        return best;
    }

    // Otherwise use scanline filling (no full grid) to compute interior "green" tiles for large spans.
    // build edges
    let mut edges: Vec<(i128,i128,i128,i128)> = Vec::new();
    for i in 0..n {
        let (x1,y1) = pts[i];
        let (x2,y2) = pts[(i+1)%n];
        edges.push((x1,y1,x2,y2));
    }

    let hspan = (max_y - min_y + 1) as usize;
    // intervals_per_row[y - min_y] -> Vec of inclusive (xl, xr) integer x indices that are inside polygon
    let mut intervals_per_row: Vec<Vec<(i128,i128)>> = vec![Vec::new(); hspan];
    for yi in min_y..=max_y {
        let y_sample = yi as f64 + 0.5f64;
        let mut xs: Vec<f64> = Vec::new();
        for &(x1,y1,x2,y2) in edges.iter() {
            if y1 == y2 { continue; }
            let ymin = (y1 as f64).min(y2 as f64);
            let ymax = (y1 as f64).max(y2 as f64);
            // include when y_sample > ymin && y_sample <= ymax to avoid double counting
            if y_sample > ymin && y_sample <= ymax {
                let xint = x1 as f64 + (y_sample - y1 as f64) * (x2 as f64 - x1 as f64) / (y2 as f64 - y1 as f64);
                xs.push(xint);
            }
        }
        xs.sort_by(|a,b| a.partial_cmp(b).unwrap());
        let mut k = 0;
        while k+1 < xs.len() {
            let xl = xs[k];
            let xr = xs[k+1];
            // integer x included satisfy: x+0.5 in (xl, xr) => x in (xl-0.5, xr-0.5)
            let left = ( (xl - 0.5f64).ceil() as i128 ).max(min_x);
            let right = ( (xr - 0.5f64).floor() as i128 ).min(max_x);
            if left <= right {
                intervals_per_row[(yi - min_y) as usize].push((left, right));
            }
            k += 2;
        }
    }

    // collect red coordinates indices (original integer coordinates)
    let mut reds: Vec<(i128,i128)> = Vec::new();
    for (x,y) in pts.iter() { reds.push((*x,*y)); }

    let mut best: u128 = 0;
    for i in 0..n {
        for j in (i+1)..n {
            let (xi, yi) = reds[i];
            let (xj, yj) = reds[j];
            if xi==xj || yi==yj { continue; }
            let x0 = xi.min(xj);
            let x1i = xi.max(xj);
            let y0 = yi.min(yj);
            let y1i = yi.max(yj);
            let mut ok = true;
            for yy in y0..=y1i {
                let row = &intervals_per_row[(yy - min_y) as usize];
                // check if [x0,x1i] is fully covered by union of intervals in row
                let mut covered = false;
                for &(l,r) in row.iter() {
                    if l <= x0 && r >= x1i { covered = true; break; }
                }
                if !covered { ok = false; break; }
            }
            if ok {
                let area = ((x1i - x0 + 1) * (y1i - y0 + 1)) as u128;
                if area > best { best = area; }
            }
        }
    }

    best
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let example = read_test_input(9);
        assert_eq!(part1(&example), 50u128);
    }

    #[test]
    fn test_part2() {
        let example = read_test_input(9);
        assert_eq!(part2(&example), 24u128);
    }
}
