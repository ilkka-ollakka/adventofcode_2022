// use std::collections::HashSet;
use std::error::Error;
use std::fs::File;
use std::io::BufRead;
use std::io::BufReader;

fn one_fully_in_other(&left: &(i32, i32), &right: &(i32, i32)) -> bool {
    (left.0 >= right.0 && left.1 <= right.1) || (right.0 >= left.0 && right.1 <= left.1)
}

fn one_overlaps_other(&left: &(i32, i32), &right: &(i32, i32)) -> bool {
    left.0 <= right.1 && right.0 <= left.1
}
fn main() -> Result<(), Box<dyn Error>> {
    // part 1

    let file = File::open("../day4.txt")?;
    let filebuffer = BufReader::new(file);

    let mut part1_score = 0;
    let mut part2_score = 0;

    for line in filebuffer.lines() {
        // println!("data: {:#?}", line);
        let line = line?;
        let string = line.trim();
        let ranges: Vec<i32> = string
            .split([',', '-'])
            .map(|x| x.parse::<i32>().unwrap())
            .collect();

        let (left, right) = ((ranges[0], ranges[1]), (ranges[2], ranges[3]));

        println!("Checking pairs {:?} - {:?}", left, right);
        if one_fully_in_other(&left, &right) {
            println!("fully in others");
            part1_score += 1;
        }
        if one_overlaps_other(&left, &right) {
            part2_score += 1;
        }
    }
    println!("End scores: part1={part1_score} part2={part2_score}");

    Ok(())
}
