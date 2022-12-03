use std::error::Error;
use std::fs::File;
use std::io::BufRead;
use std::io::BufReader;
use thiserror::Error;

#[derive(Debug, Error)]
#[non_exhaustive]
pub enum AOCError {
    #[error("Error Parsing value")]
    ParsinError,
    #[error("Couldn't open file: {0}")]
    FileError(std::io::Error),
}

pub fn read_file_and_split(filename: &str) -> Result<Vec<(String, String)>, Box<dyn Error>> {
    let mut parsed_output: Vec<(String, String)> = Vec::new();

    let file = File::open(format!("../{}", filename))?;
    let mut filebuffer = BufReader::new(file);

    loop {
        let mut line: String = String::new();
        let read_amount = filebuffer.read_line(&mut line)?;

        if read_amount == 0 {
            break;
        }

        line = (*line.trim()).to_string();

        let mut splitted_output = line.split(" ");

        parsed_output.push((
            splitted_output.next().unwrap().to_string(),
            splitted_output.next().unwrap().to_string(),
        ));
    }

    return Ok(parsed_output);
}

pub fn read_daily_input(filename: &str, return_amount: usize) -> Result<Vec<u32>, Box<dyn Error>> {
    let file = File::open(format!("../{}", filename))?;
    let mut filebuffer = BufReader::new(file);

    let mut elfs: Vec<u32> = Vec::new();
    let mut elf: u32 = 0;

    loop {
        let mut line: String = String::new();
        let read_amount = filebuffer.read_line(&mut line)?;

        if read_amount == 0 {
            // End of File
            break;
        }

        line = (*line.trim()).to_string();

        //println!("read {} content '{}'", read_amount, line.trim());

        if line.is_empty() {
            elfs.push(elf);
            elf = 0;
            continue;
        }

        let result: u32 = line.parse()?;

        elf += result;
    }

    elfs.sort_by_key(|k| -1 * *k as i32);
    if return_amount != usize::MAX {
        elfs.truncate(return_amount);
    }
    Ok(elfs)
}
