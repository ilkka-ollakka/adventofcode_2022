use rust_utility::{read_daily_input, AOCError};

fn main() -> Result<(), AOCError> {
    let elfs = read_daily_input("day1.txt", 3)?;
    // println!("elfs: {:#?}", elfs);

    let mut result: u32 = 0;
    let mut counter: u32 = 0;

    println!("Elfs {:#?}", elfs);

    for value in elfs {
        if counter == 0 {
            println!("Max elf: {}", value);
        }
        result += value;
        counter += 1;
        if counter == 3 {
            println!("Max 3 elfs: {}", result);
            break;
        }
    }

    //elfs.pop().unwrap();

    // println!("max elf: {}", result);

    //result += elfs.pop().unwrap() + elfs.pop().unwrap();

    // println!("max 3 elfs amount: {:#?}", result);

    Ok(())
}
