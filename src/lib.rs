//! A set of memorable words, with convenience passphrase functions
//!
//! The list of words is just [`WORDS`](WORDS).
//!
//! You may likely prefer to use one of the provided passphrase
//! generators.  These accept a number of bits of entropy desired.
//! This corresponds to the `log2` of the number of passphrases that
//! should be possible to generate.  This interface allows the number
//! of memorable words to be adjusted without making your code any
//! less secure.  You get to decide how secore the passphrase needs to
//! be.  If your concern is a network attacker, then you might think
//! that the 44 bits of entropy [advertized by
//! xkcd](https://m.xkcd.com/936) is sufficient.  If you are concerned
//! about an offline attack on a hashed password file, then you'd
//! better ask for more entropy or ensure that you use a seriously
//! slow hashing algorithm and a good salt.
//!
//! Note that while the algorithm guarantees the number of bits of
//! entropy you request, it doesn't go far above that.  So the fewer
//! bits you request, the easier to remember the result should be.

mod words;

/// The list of memorable words
///
/// This list is ordered from "most memorable" to "least" so if you
/// want to use a subset you may use the first `N` words.
pub const WORDS: &[&str] = words::LIST;

const NUM_BITS: usize = 14;

fn words_for_bits(bits: usize) -> impl Iterator<Item=&'static str> {
    use rand::Rng;

    let num_words = if bits % NUM_BITS == 0 { bits/NUM_BITS } else { bits/NUM_BITS + 1 };
    let number_per_word = (bits as f64/num_words as f64).exp2() as usize;
    let mut words = Vec::with_capacity(num_words);
    let mut rng = rand::thread_rng();
    for _ in 0..num_words {
        words.push(rng.choose(&WORDS[0..number_per_word]).unwrap());
    }
    words.into_iter().map(|&x| x)
}

/// Generate a space-delimited passphrase
///
/// The passphrase will be generated with `bits` amount of entropy.
pub fn space_delimited(bits: usize) -> String {
    let mut code = String::new();
    for w in words_for_bits(bits) {
        code.push_str(w);
        code.push(' ');
    }
    code.pop();
    code
}

/// Generate a snake_case passphrase
///
/// The passphrase will be generated with `bits` amount of entropy.
pub fn snake_case(bits: usize) -> String {
    let mut code = String::new();
    for w in words_for_bits(bits) {
        code.push_str(w);
        code.push('_');
    }
    code.pop();
    code
}

/// Generate a kebab-case passphrase
///
/// The passphrase will be generated with `bits` amount of entropy.
pub fn kebab_case(bits: usize) -> String {
    let mut code = String::new();
    for w in words_for_bits(bits) {
        code.push_str(w);
        code.push('-');
    }
    code.pop();
    code
}


/// Generate a CamelCase passphrase
///
/// The passphrase will be generated with `bits` amount of entropy.
pub fn camel_case(bits: usize) -> String {
    let mut code = String::new();
    for w in words_for_bits(bits) {
        let mut c = w.chars();
        code.push(c.next().unwrap().to_uppercase().next().unwrap());
        code.push_str(c.as_str());
    }
    code
}

#[test]
fn has_length() {
    assert!(space_delimited(41).len() > 4);
    assert!(snake_case(40).len() > 4);
    assert!(camel_case(40).len() > 4);
    assert!(kebab_case(40).len() > 4);
}

#[test]
fn num_bits_correct() {
    assert!(1 << NUM_BITS <= WORDS.len());
}
