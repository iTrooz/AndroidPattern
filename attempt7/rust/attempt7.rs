const SIZE: isize = 4;
const MIN_LEN: usize = 4;
const MAX_LEN: usize = 7;

fn is_close_int(n: f64) -> bool {
    let n = n.abs() % 1.0;
    let eps = 0.0001;
    n < eps || (1.0 - n) < eps
}

#[test]
fn test_is_close_int() {
    assert!(is_close_int(5.00001));
    assert!(is_close_int(5.99999));
    assert!(is_close_int(-5.00001));
    assert!(is_close_int(-5.99999));
    assert!(!is_close_int(5.5));
}

fn to_number_0(p: &(isize, isize)) -> isize {
    6 - p.1 * 3 + p.0
}

fn get_inbetween_points(p1: &(isize, isize), p2: &(isize, isize)) -> Vec<(isize, isize)> {
    let xdiff = p2.0 - p1.0;

    if xdiff == 0 {
        let y_range = (p1.1.min(p2.1) + 1)..p1.1.max(p2.1);
        y_range.map(move |y| (p1.0, y)).collect()
    } else {
        let slope = (p2.1 - p1.1) as f64 / xdiff as f64;

        let init = p2.1 as f64 - slope * p2.0 as f64;

        let x_range = (p1.0.min(p2.0) + 1)..p1.0.max(p2.0);
        x_range
            .filter_map(move |x| {
                let y = slope * x as f64 + init;
                if is_close_int(y) {
                    Some((x, y.round() as isize))
                } else {
                    None
                }
            })
            .collect()
    }
}

#[test]
fn test_get_inbetween_points() {
    assert_eq!(get_inbetween_points(&(0, 0), &(3, 3)), vec![(1, 1), (2, 2)]);
    assert_eq!(get_inbetween_points(&(3, 3), &(0, 0)), vec![(1, 1), (2, 2)]);
    assert_eq!(get_inbetween_points(&(1, 1), &(3, 5)), vec![(2, 3)]);
    assert_eq!(get_inbetween_points(&(0, 0), &(0, 2)), vec![(0, 1)]);
    assert_eq!(get_inbetween_points(&(0, 0), &(2, 0)), vec![(1, 0)]);
}

fn gen_all_points() -> Vec<(isize, isize)> {
    (0..SIZE)
        .flat_map(move |x| (0..SIZE).map(move |y| (x, y)))
        .collect()
}

fn choose_next_point(used_points: &mut Vec<(isize, isize)>, last_point: (isize, isize)) -> isize {
    let mut found_possibilities = 0;

    if used_points.len() >= MIN_LEN {
        found_possibilities += 1;
        if used_points.len() == MAX_LEN {
            return found_possibilities;
        }
    }

    for p in gen_all_points() {
        if !used_points.contains(&p) {
            let mut valid = true;

            for between_p in get_inbetween_points(&last_point, &p) {
                if !used_points.contains(&between_p) {
                    valid = false;
                    break;
                }
            }

            if valid {
                // TODO maybe use stack push/pop instead of copy ??
                let mut used_points_copy = used_points.clone();
                used_points_copy.push(p);
                found_possibilities += choose_next_point(&mut used_points_copy, p);
            }
        }
    }

    found_possibilities
}

fn main() {
    let mut total = 0;

    for p in gen_all_points() {
        println!("Starting start point {:?} ({})", p, to_number_0(&p));
        let mut used_points = vec![p];
        total += choose_next_point(&mut used_points, p);
        println!("Finished start point {:?}", p);
    }

    println!("Sum: {}", total);
}
