use proc_macro::TokenStream;

#[proc_macro]
pub fn make_all_points(input: TokenStream) -> TokenStream {
    let size: u16 = input.to_string().parse().unwrap();

    let mut s: String = "".to_owned();
    for x in 0..size {
        for y in 0..size {
            s.push_str(&format!("({},{}),", x, y));
        }
    }
    s.pop();
    
    format!("const ALL_POINTS: [(isize, isize); {}] = [{}];", size*size, s).parse().unwrap()
}
