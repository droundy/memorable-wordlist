const BITS: usize = 44;

fn main() {
    println!("## Example output with {} bits entropy\n", BITS);
    println!("`space_delimited`:\n```");
    for _ in 1..10 {
        println!("{}", memorable_wordlist::space_delimited(BITS));
    }
    println!("```\n`snake_case`:\n```");
    for _ in 1..10 {
        println!("{}", memorable_wordlist::snake_case(BITS));
    }
    println!("```\n`kebab_case`:\n```");
    for _ in 1..10 {
        println!("{}", memorable_wordlist::kebab_case(BITS));
    }
    println!("```\n`camel_case`:\n```");
    for _ in 1..10 {
        println!("{}", memorable_wordlist::camel_case(BITS));
    }
    println!("```");
}
