mod words;

pub const WORDS: &[&str] = words::LIST;

pub fn space_delimited(bits: usize) -> String {
    use rand::Rng;

    let mut rng = rand::thread_rng();
    let mut code = String::new();
    let mut sofar = 0;
    while sofar < bits {
        code.push_str(rng.choose(WORDS).unwrap());
        code.push(' ');
        sofar += 13;
    }
    code.pop();
    code
}

pub fn snake_case(bits: usize) -> String {
    use rand::Rng;

    let mut rng = rand::thread_rng();
    let mut code = String::new();
    let mut sofar = 0;
    while sofar < bits {
        code.push_str(rng.choose(WORDS).unwrap());
        code.push('_');
        sofar += 13;
    }
    code.pop();
    code
}


pub fn camel_case(bits: usize) -> String {
    use rand::Rng;

    let mut rng = rand::thread_rng();
    let mut code = String::new();
    let mut sofar = 0;
    while sofar < bits {
        let mut c = rng.choose(WORDS).unwrap().chars();
        code.push(c.next().unwrap().to_uppercase().next().unwrap());
        code.push_str(c.as_str());
        sofar += 13;
    }
    code
}

#[test]
fn has_length() {
    assert!(space_delimited(40).len() > 4);
    assert!(snake_case(40).len() > 4);
    assert!(camel_case(40).len() > 4);
}
