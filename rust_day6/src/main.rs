use std::collections::HashSet;
use std::error::Error;
use std::fs;

fn find_marker(input: &str, sequence_length: usize) -> Option<usize> {
    input
        .chars()
        .collect::<Vec<char>>()
        .windows(sequence_length)
        .position(|window| window.iter().collect::<HashSet<_>>().len() == sequence_length)
        .map(|pos| pos + sequence_length)
}

fn find_sequence(input: &str, sequence_length: usize) -> usize {
    let file_chars: Vec<char> = input.chars().collect();
    // println!("Token {file_chars:?}");

    for position in 0..str::len(input) - sequence_length {
        let token: HashSet<char> = file_chars[position..=(position + sequence_length - 1)]
            .iter()
            .copied()
            .collect();

        // println!("checking in {position}");

        let len = token.len();

        if len == sequence_length {
            let location = position + sequence_length;
            // println!("Found match in {location}!");
            // println!("tokens {token:?}");
            return location;
        }

        // println!("token: {len}");
    }
    return 0;
}

fn main() -> Result<(), Box<dyn Error>> {
    // part 1

    let file_input: String = fs::read_to_string("../day6.txt")?;

    for line in file_input.lines() {
        let part1 = find_sequence(&line, 4);
        let token_start = &line[0..=6];
        let part1_marker = find_marker(line, 4).expect("Didn't find marker");
        println!("First part {part1} {part1_marker} for line starting with {token_start}");
    }

    for line in file_input.lines() {
        let part2 = find_sequence(&line, 14);
        let token_start = &line[0..=6];
        println!("Second part {part2} for line starting with {token_start}");
    }

    Ok(())
}
