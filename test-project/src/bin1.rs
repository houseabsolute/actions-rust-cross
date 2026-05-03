extern "C" {
    fn hello_cpp() -> i32;
}

fn main() {
    let _ = unsafe { hello_cpp() };
    println!("Hello, world!");
}

#[cfg(test)]
mod test {
    #[test]
    fn test_something() {
        assert_eq!(1, 1);
    }
}
