use std::error::Error;

use rust_utility::read_daily_input;

fn main() -> Result<(), Box<dyn Error>> {
    let elfs = read_daily_input("day1.txt", 3)?;

    println!("Max elf: {}", elfs[0]);

    println!("Max 3 elfs: {}", elfs.iter().sum::<u32>());

    Ok(())
}
