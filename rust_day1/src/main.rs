use rust_utility::{read_daily_input, AOCError};

fn main() -> Result<(), AOCError> {
    let elfs = read_daily_input("day1.txt", 3)?;
    // println!("elfs: {:#?}", elfs);

    // println!("Elfs {:#?}", elfs);

    println!("Max elf: {}", elfs[0]);

    println!("Max 3 elfs: {}", elfs.iter().sum::<u32>());

    //elfs.pop().unwrap();

    // println!("max elf: {}", result);

    //result += elfs.pop().unwrap() + elfs.pop().unwrap();

    // println!("max 3 elfs amount: {:#?}", result);

    Ok(())
}
