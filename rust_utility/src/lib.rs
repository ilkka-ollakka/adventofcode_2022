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

pub fn read_file_and_split(filename: &str) -> Result<Vec<String>, Box<dyn Error>> {
    let mut parsed_output: Vec<String> = Vec::new();

    let file = File::open(format!("../{}", filename))?;
    let mut filebuffer = BufReader::new(file);

    loop {
        let mut line: String = String::new();
        let read_amount = filebuffer.read_line(&mut line)?;

        if read_amount == 0 {
            break;
        }

        line = (*line.trim()).to_string();

        // println!("output: {:#?}", line);

        parsed_output.push(line);
    }

    return Ok(parsed_output);
}

pub fn read_daily_input(filename: &str, return_amount: usize) -> Result<Vec<u32>, Box<dyn Error>> {
    let file = BufReader::new(File::open(format!("../{}", filename)).expect("Cannot open file"));

    let mut elfs: Vec<u32> = Vec::new();
    let mut elf: u32 = 0;

    file.lines()
        .filter_map(|line| line.ok())
        .for_each(|string| {
            match string.parse::<u32>() {
                Ok(result) => elf += result,
                Err(_) => {
                    elfs.push(elf);
                    elf = 0;
                }
            };
        });

    if return_amount != usize::MAX {
        elfs.sort_by_key(|k| -1 * *k as i32);
        elfs.truncate(return_amount);
    }
    Ok(elfs)
}
