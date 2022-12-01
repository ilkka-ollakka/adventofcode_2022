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

pub fn read_daily_input(filename: &str, return_amount: usize) -> Result<Vec<u32>, AOCError> {
    let file = match File::open(format!("../{}", filename)) {
        Ok(x) => x,
        Err(x) => return Err(AOCError::FileError(x)),
    };
    let mut filebuffer = BufReader::new(file);

    let mut elfs: Vec<u32> = Vec::new();
    let mut elf: u32 = 0;

    loop {
        let mut line: String = String::new();
        let read_amount = match filebuffer.read_line(&mut line) {
            Ok(x) => x,
            Err(..) => return Err(AOCError::ParsinError),
        };

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

        let result: u32 = match line.parse() {
            Ok(x) => x,
            Err(y) => {
                println!("Could not parse {} as u32, error {}", line, y);
                return Err(AOCError::ParsinError);
            }
        };
        elf += result;
    }

    elfs.sort_by_key(|k| -1 * *k as i32);
    if return_amount == usize::MAX {
        Ok(elfs)
    } else {
        Ok(elfs[0..return_amount].to_vec())
    }
}
