// use crossterm::{
//     event::{self, Event, KeyCode},
//     execute,
//     terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
// };
// use ratatui::{
//     backend::CrosstermBackend,
//     layout::{Constraint, Direction, Layout},
//     style::{Color, Modifier, Style},
//     widgets::{Block, Borders, List, ListItem, ListState, Paragraph},
//     Terminal,
// };
use std::{error::Error};
pub mod partition;
pub mod node;
use partition::{PartitionMap};
use node::{NodeMap};
fn main() -> Result<(), Box<dyn Error>> {
    // Fetch node data
    let node_map: NodeMap = NodeMap::build()?;

    // Fetch partition data
    let partition_map: PartitionMap = PartitionMap::build()?;

    //  get the partition 'veryhimem' from the partition map
    let p_of_choice = "veryhimem";
    let partition = partition_map.get(p_of_choice).unwrap();

    println!("Partition: {}\n", partition.name);
    for node in partition.nodes.iter() {
        let node = node_map.get(node).unwrap();
        println!(
            "Node: {:<16}\n\tCPUTotal: {:<4}\n\tMEMORY: {}\n\n",
            node.name, 
            node.pretty_cpu(),
            node.pretty_memory("GB"),
        );

    }

    return Ok(());

}