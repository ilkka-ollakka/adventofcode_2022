use rust_utility::read_file_and_split;
use std::collections::HashSet;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let mut scores: Vec<char> = Vec::new();

    for item in 'a'..='z' {
        scores.push(item);
    }
    for item in 'A'..='Z' {
        scores.push(item);
    }

    // part 1

    let data = read_file_and_split("day3.txt")?;

    let mut final_score_part1: i32 = 0;

    for line in data {
        // println!("data: {:#?}", line);
        let vector_string = line.chars().collect::<Vec<char>>();

        let length: usize = vector_string.len() / 2;
        let (left, right) = vector_string.split_at(length);
        let left_hash: HashSet<&char> = left.iter().collect();
        let right_hash: HashSet<&char> = right.iter().collect();

        // println!("left and right hash-sets: {:?} {:?}", left_hash, right_hash);

        let common = left_hash
            .intersection(&right_hash)
            .collect::<Vec<&&char>>()
            .pop()
            .unwrap();

        // println!("Common item {}", common);
        let common_score = scores.iter().position(|&x| x == **common).unwrap();
        println!("Common item {} score {}", common, common_score);
        final_score_part1 += (common_score as i32) + 1;
    }

    println!("part1 final score: {}", final_score_part1);
    // println!("scores: {:?}", scores);

    // part 2
    let data_part2 = read_file_and_split("day3.txt")?;

    let mut final_score_part2: i32 = 0;

    let mut stack: Vec<HashSet<char>> = Vec::with_capacity(2);
    for line in data_part2 {
        // println!("data: {:#?}", line);

        let string_hash: HashSet<char> = line.chars().collect();
        if stack.len() == 2 {
            let first_item = stack.pop().unwrap();
            let common_first = string_hash.intersection(&first_item).copied();

            let second_item = stack.pop().unwrap();
            let common_hash: HashSet<char> = common_first.collect();
            let common_second: char = second_item
                .intersection(&common_hash)
                .collect::<Vec<&char>>()
                .pop()
                .copied()
                .unwrap();
            // println!("common {:?}", common_second);
            let common_score = scores.iter().position(|&x| x == common_second).unwrap();

            final_score_part2 += (common_score as i32) + 1;

            stack.clear();
            continue;
        }
        stack.push(string_hash);
    }

    println!("part2 final score: {}", final_score_part2);
    Ok(())
}
