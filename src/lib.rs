mod words;

pub const WORDS: &[&str] = words::LIST;

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
