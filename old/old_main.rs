mod node;
mod partition;

use clap::Parser;
use std::error::Error;
use std::process;
use node::Node;
use partition::Partition;

#[derive(Parser)]
#[command(
    author = "Your Name",
    version = "1.0",
    about = "A simple CLI for parsing Slurm node and partition information"
)]
struct Cli {
    #[arg(long)]
    fetch_nodes: bool,

    #[arg(long)]
    fetch_partitions: bool,

    #[arg(short, long)]
    input: Option<String>,
}

fn main() {
    let cli = Cli::parse();

    if cli.fetch_nodes {
        match fetch_and_parse_nodes() {
            Ok(nodes) => {
                for node in nodes {
                    println!("{:#?}", node);
                }
            }
            Err(e) => {
                eprintln!("Error fetching nodes: {}", e);
                process::exit(1);
            }
        }
    } else if cli.fetch_partitions {
        match Partition::fetch_and_parse_partitions() {
            Ok(partitions) => {
                for partition in partitions {
                    println!("{:#?}", partition);
                }
            }
            Err(e) => {
                eprintln!("Error fetching partitions: {}", e);
                process::exit(1);
            }
        }
    } else if let Some(input_file) = cli.input {
        println!("Input file: {}", input_file);
    } else {
        eprintln!("No action specified. Use --fetch-nodes or --fetch-partitions.");
        process::exit(1);
    }
}

fn fetch_and_parse_nodes() -> Result<Vec<Node>, Box<dyn Error>> {
    let output = std::process::Command::new("scontrol")
        .args(["show", "node", "-a", "--oneliner"])
        .output()?;

    if !output.status.success() {
        return Err(format!(
            "Failed to execute scontrol: {}",
            String::from_utf8_lossy(&output.stderr)
        )
        .into());
    }

    let stdout = String::from_utf8(output.stdout)?;
    Node::parse_nodes(&stdout)
}
