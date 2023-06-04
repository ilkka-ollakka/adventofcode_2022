use rust_utility::read_file_and_split;
use std::error::Error;

#[derive(Debug)]
struct RPS {
    score: u32,
    wins: String,
    loses_to: String,
}

fn map_own_to_piece(own_piece: &str) -> String {
    match own_piece {
        "X" => 'A'.to_string(),
        "Y" => 'B'.to_string(),
        "Z" => 'C'.to_string(),
        _ => 'A'.to_string(),
    }
}

fn end_score(opponent_piece: &str, own_piece: &str) -> u32 {
    let piece = get_piece_info(opponent_piece);

    if piece.wins == own_piece {
        return 6;
    } else if piece.loses_to == own_piece {
        return 0;
    }
    return 3;
}

fn get_piece_info(piece_mark: &str) -> RPS {
    match piece_mark {
        "A" => RPS {
            score: 1,
            wins: "B".to_string(),
            loses_to: "C".to_string(),
        },
        "B" => RPS {
            score: 2,
            wins: "C".to_string(),
            loses_to: "A".to_string(),
        },
        "C" => RPS {
            score: 3,
            wins: "A".to_string(),
            loses_to: "B".to_string(),
        },
        _ => RPS {
            score: 3,
            wins: "A".to_string(),
            loses_to: "B".to_string(),
        },
    }
}

fn own_piece_to_result_piece(opponent_piece: &str, own_piece: &str) -> String {
    let result_piece = get_piece_info(opponent_piece);
    match own_piece {
        "X" => result_piece.loses_to,
        "Y" => opponent_piece.to_string(),
        "Z" => result_piece.wins,
        _ => opponent_piece.to_string(),
    }
}

fn piece_score(piece: &str) -> u32 {
    return get_piece_info(piece).score;
}

fn main() -> Result<(), Box<dyn Error>> {
    let output = read_file_and_split("day2.txt")?;

    let mut final_score: u32 = 0;
    let mut final_score2: u32 = 0;

    for line in output {
        let line_split: Vec<&str> = line.split(" ").collect();
        let (opponent, own) = (line_split[0], line_split[1]);

        // println!("opponent {} own {}", opponent, own);
        let mapped_own = map_own_to_piece(&own);

        let score = end_score(&opponent, &mapped_own);
        let piece_score_result = piece_score(&mapped_own);

        let mapped_own2 = own_piece_to_result_piece(&opponent, &own);

        let score2 = end_score(&opponent, &mapped_own2);
        let piece_score2 = piece_score(&mapped_own2);

        final_score += score + piece_score_result;
        final_score2 += score2 + piece_score2;
    }

    println!("Part1 end score: {}", final_score);
    // Part 2

    println!("Part2 end score: {}", final_score2);
    Ok(())
}
