use std::error::Error;
use clap::{ Parser, Subcommand };

use terminal_size::{ Width, Height, terminal_size };

// use slurmtool::progress::{new_progress_bar};
pub mod partition;
pub mod node;
use partition::PartitionMap;
use node::NodeMap;

/// CLI Application to fetch node details for a specific partition
#[derive(Parser)]
#[command(name = "Partition Node Viewer")]
#[command(about = "CLI to fetch and display node details for a partition", version = "1.0")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Fetch nodes for a specific partition
    Nodes {
        /// The name of the partition to fetch nodes from
        #[arg(short, long)]
        partition: String,

        /// The number of nodes to display in the partition
        /// Default is all (0)
        #[arg(short, long)]
        limit: Option<usize>,

        /// to debug, print all attributes of the node struct
        /// Default is false
        #[arg(short, long)]
        debug: bool,
    },
    GroupNodes {
        /// The name of the partition to fetch nodes from
        #[arg(short, long)]
        partition: String,
    },
}

fn main() -> Result<(), Box<dyn Error>> {
    let size = terminal_size();
    if let Some((Width(w), Height(h))) = size {
        println!("Your terminal is {} cols wide and {} lines tall", w, h);
    } else {
        println!("Unable to get terminal size");
    }

    let cli = Cli::parse();

    match cli.command {
        Commands::Nodes { partition, limit, debug } => {
            display_partition_nodes(&partition, limit, debug)?;
        }
        Commands::GroupNodes { partition } => {
            group_partition_nodes(&partition)?;
        }
    }
    Ok(())
}
/// Displays the nodes in the specified partition
fn display_partition_nodes(
    partition_name: &str,
    limit: Option<usize>,
    debug: bool
) -> Result<(), Box<dyn Error>> {
    let node_map: NodeMap = NodeMap::build()?;
    let partition_map: PartitionMap = PartitionMap::build()?;

    let partition = partition_map
        .get(partition_name)
        .ok_or_else(|| format!("Partition '{}' not found", partition_name))?;

    let nodes_to_display = limit.unwrap_or(partition.nodes.len());
    println!(
        "Partition: {} (showing {} of {} nodes)\n",
        partition.name,
        nodes_to_display,
        partition.nodes.len()
    );

    for node in partition.nodes.iter().take(nodes_to_display) {
        let node = node_map.get(node).unwrap();
        if debug {
            println!("{:#?}", node);
        } else {
            println!(
                "Node: {:<16}\n\tCPUTotal: {:<4}\n\tMEMORY: {}\n\n",
                node.name,
                node.pretty_cpu(),
                node.pretty_memory("GB")
            );
        }
    }

    Ok(())
}

/// Groups nodes in the specified partition by total_cpu and real_memory
fn group_partition_nodes(partition_name: &str) -> Result<(), Box<dyn Error>> {
    let node_map: NodeMap = NodeMap::build()?;
    let partition_map: PartitionMap = PartitionMap::build()?;

    let partition = partition_map
        .get(partition_name)
        .ok_or_else(|| format!("Partition '{}' not found", partition_name))?;

    let mut groups: std::collections::BTreeMap<
        (u32, u32),
        Vec<String>
    > = std::collections::BTreeMap::new();
    for node_name in &partition.nodes {
        if let Some(node) = node_map.get(node_name) {
            let total_cpu = node.cpu_total.unwrap_or(0);
            let real_memory_gb = node.real_memory.expect("Real memory missing").as_gb();
            groups.entry((total_cpu, real_memory_gb)).or_default().push(node.name.clone());
        }
    }

    for ((total_cpu, real_memory_gb), nodes) in groups {
        println!(
            "{} - Total CPU: {}, Real Memory: {} GB",
            partition_name,
            total_cpu,
            real_memory_gb
        );
        for node_name in nodes {
            println!("\t{}", node_name);
        }
    }

    Ok(())
}
