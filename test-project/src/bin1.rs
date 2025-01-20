use anyhow::Result;

fn main() {
    println!("Hello, world!");
    if let Err(e) = run_something() {
        eprintln!("{e}");
        std::process::exit(1);
    }
}

fn run_something() -> Result<()> {
    Ok(())
}

#[cfg(test)]
mod test {
    #[test]
    fn test_something() {
        assert_eq!(1, 1);
    }
}
