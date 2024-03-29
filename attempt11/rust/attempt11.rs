use itertools::Either;
use mylib::make_all_points;

const SIZE: isize = 4;
const MIN_LEN: usize = 4;
const MAX_LEN: usize = 8;
make_all_points!(4); // create ALL_POINTS const. Pass SIZE as argument

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

fn get_inbetween_points(
    p1: &(isize, isize),
    p2: &(isize, isize),
) -> impl Iterator<Item = (isize, isize)> {
    let xdiff = p2.0 - p1.0;

    let mut either: Either<_, _>;

    if xdiff == 0 {
        let y_range = (p1.1.min(p2.1) + 1)..p1.1.max(p2.1);
        let p1x = p1.0;
        let fun = y_range.filter_map(move |y| Some((p1x, y)));
        either = Either::Left(fun);
    } else {
        let slope = (p2.1 - p1.1) as f64 / xdiff as f64;

        let init = p2.1 as f64 - slope * p2.0 as f64;

        let x_range = (p1.0.min(p2.0) + 1)..p1.0.max(p2.0);

        let fun = x_range.filter_map(move |x| {
            let y = slope * x as f64 + init;
            if is_close_int(y) {
                Some((x, y.round() as isize))
            } else {
                None
            }
        });
        either = Either::Right(fun);
    }

    std::iter::from_fn(move || match &mut either {
        Either::Left(ref mut left) => left.next(),
        Either::Right(ref mut right) => right.next(),
    })
}

#[test]
fn test_get_inbetween_points() {
    assert_eq!(
        get_inbetween_points(&(0, 0), &(3, 3)).collect::<Vec<_>>(),
        vec![(1, 1), (2, 2)]
    );
    assert_eq!(
        get_inbetween_points(&(3, 3), &(0, 0)).collect::<Vec<_>>(),
        vec![(1, 1), (2, 2)]
    );
    assert_eq!(
        get_inbetween_points(&(1, 1), &(3, 5)).collect::<Vec<_>>(),
        vec![(2, 3)]
    );
    assert_eq!(
        get_inbetween_points(&(0, 0), &(0, 2)).collect::<Vec<_>>(),
        vec![(0, 1)]
    );
    assert_eq!(
        get_inbetween_points(&(0, 0), &(2, 0)).collect::<Vec<_>>(),
        vec![(1, 0)]
    );
}

fn choose_next_point(used_points: &mut Vec<(isize, isize)>, last_point: (isize, isize)) -> isize {
    let mut found_possibilities = 0;

    if used_points.len() >= MIN_LEN {
        found_possibilities += 1;
        if used_points.len() >= MAX_LEN {
            return found_possibilities;
        }
    }

    for p in ALL_POINTS {
        if !used_points.contains(&p) {
            let mut valid = true;

            for between_p in get_inbetween_points(&last_point, &p) {
                if !used_points.contains(&between_p) {
                    valid = false;
                    break;
                }
            }

            if valid {
                used_points.push(p);
                found_possibilities += choose_next_point(used_points, p);
                used_points.pop();
            }
        }
    }

    found_possibilities
}

fn main() {
    let mut total = 0;

    for p in ALL_POINTS {
        println!("Starting start point {:?}", p);
        let mut used_points = vec![p];
        total += choose_next_point(&mut used_points, p);
        println!("Finished start point {:?}", p);
    }

    println!("Sum: {}", total);
}
