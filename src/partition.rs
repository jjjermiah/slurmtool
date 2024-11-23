use std::error::Error;

#[derive(Debug, Default)]
pub struct Partition {
    pub name: String,
    pub allow_groups: Option<String>,
    pub allow_accounts: Vec<String>,
    pub allow_qos: Option<String>,
    pub alloc_nodes: Option<String>,
    pub default: bool,
    pub qos: Option<String>,
    pub default_time: Option<String>,
    pub disable_root_jobs: bool,
    pub exclusive_user: bool,
    pub grace_time: Option<u32>,
    pub hidden: bool,
    pub max_nodes: Option<u32>,
    pub max_time: Option<String>,
    pub min_nodes: Option<u32>,
    pub lln: bool,
    pub max_cpus_per_node: Option<String>,
    pub max_cpus_per_socket: Option<String>,
    pub nodes: Vec<String>,
    pub priority_job_factor: Option<u32>,
    pub priority_tier: Option<u32>,
    pub root_only: bool,
    pub req_resv: bool,
    pub oversubscribe: bool,
    pub over_time_limit: Option<String>,
    pub preempt_mode: Option<String>,
    pub state: Option<String>,
    pub total_cpus: Option<u32>,
    pub total_nodes: Option<u32>,
    pub select_type_parameters: Option<String>,
    pub job_defaults: Option<String>,
    pub def_mem_per_cpu: Option<u32>,
    pub max_mem_per_node: Option<u32>,
    pub tres: Option<String>,
    pub tres_billing_weights: Option<String>,
}
impl Partition {
    pub fn from_fields(fields: &[(&str, &str)]) -> Self {
        let mut partition = Partition::default();

        for (key, value) in fields {
            match *key {
                "PartitionName" => {
                    partition.name = value.to_string();
                }
                "AllowGroups" => {
                    partition.allow_groups = Some(value.to_string());
                }
                "AllowAccounts" => {
                    partition.allow_accounts = value
                        .to_string()
                        .split(',')
                        .map(|s| s.to_string())
                        .collect();
                }
                "AllowQos" => {
                    partition.allow_qos = Some(value.to_string());
                }
                "AllocNodes" => {
                    partition.alloc_nodes = Some(value.to_string());
                }
                "Default" => {
                    partition.default = *value == "YES";
                }
                "QoS" => {
                    partition.qos = Some(value.to_string());
                }
                "DefaultTime" => {
                    partition.default_time = Some(value.to_string());
                }
                "DisableRootJobs" => {
                    partition.disable_root_jobs = *value == "YES";
                }
                "ExclusiveUser" => {
                    partition.exclusive_user = *value == "YES";
                }
                "GraceTime" => {
                    partition.grace_time = value.parse().ok();
                }
                "Hidden" => {
                    partition.hidden = *value == "YES";
                }
                "MaxNodes" => {
                    partition.max_nodes = value.parse().ok();
                }
                "MaxTime" => {
                    partition.max_time = Some(value.to_string());
                }
                "MinNodes" => {
                    partition.min_nodes = value.parse().ok();
                }
                "LLN" => {
                    partition.lln = *value == "YES";
                }
                "MaxCPUsPerNode" => {
                    partition.max_cpus_per_node = Some(value.to_string());
                }
                "MaxCPUsPerSocket" => {
                    partition.max_cpus_per_socket = Some(value.to_string());
                }
                "Nodes" => {
                    partition.nodes = expand_node_range(value);
                }
                "PriorityJobFactor" => {
                    partition.priority_job_factor = value.parse().ok();
                }
                "PriorityTier" => {
                    partition.priority_tier = value.parse().ok();
                }
                "RootOnly" => {
                    partition.root_only = *value == "YES";
                }
                "ReqResv" => {
                    partition.req_resv = *value == "YES";
                }
                "OverSubscribe" => {
                    partition.oversubscribe = *value == "YES";
                }
                "OverTimeLimit" => {
                    partition.over_time_limit = Some(value.to_string());
                }
                "PreemptMode" => {
                    partition.preempt_mode = Some(value.to_string());
                }
                "State" => {
                    partition.state = Some(value.to_string());
                }
                "TotalCPUs" => {
                    partition.total_cpus = value.parse().ok();
                }
                "TotalNodes" => {
                    partition.total_nodes = value.parse().ok();
                }
                "SelectTypeParameters" => {
                    partition.select_type_parameters = Some(value.to_string());
                }
                "JobDefaults" => {
                    partition.job_defaults = Some(value.to_string());
                }
                "DefMemPerCPU" => {
                    partition.def_mem_per_cpu = value.parse().ok();
                }
                "MaxMemPerNode" => {
                    partition.max_mem_per_node = value.parse().ok();
                }
                "TRES" => {
                    partition.tres = Some(value.to_string());
                }
                "TRESBillingWeights" => {
                    partition.tres_billing_weights = Some(value.to_string());
                }
                _ => {} // Ignore any unknown keys
            }
        }

        partition
    }

    pub fn fetch_and_parse_partitions() -> Result<Vec<Self>, Box<dyn Error>> {

				let output = std::process::Command::new("scontrol")
					.args(["show", "partition", "-a", "--oneliner"])
					.output()?;
        let mut partitions = Vec::new();

				if !output.status.success() {
						return Err(format!(
								"Failed to execute scontrol: {}",
								String::from_utf8_lossy(&output.stderr)
						)
						.into());
				}
				let stdout = String::from_utf8(output.stdout)?;

        for line in stdout.lines() {
            let fields: Vec<(&str, &str)> = line
                .split_whitespace()
                .filter_map(|kv| {
                    let mut parts = kv.splitn(2, '=');
                    match (parts.next(), parts.next()) {
                        (Some(key), Some(value)) => Some((key, value)),
                        _ => None,
                    }
                })
                .collect();

            partitions.push(Partition::from_fields(&fields));
        }

        Ok(partitions)
    }
}

// example value:
// "node[39-40,42-43]"
fn expand_node_range(value_from_output: &str) -> Vec<String> {
    let mut nodes = Vec::new();
    let mut range = value_from_output;

    // first extract only the content inside the brackets
    if let Some((_, range_part)) = range.split_once('[') {
        range = range_part.strip_suffix(']').unwrap_or(range_part);
    }

    // then split the content by comma
    for subrange in range.split(',') {
        // if the subrange contains a dash, then it is a range
        if let Some((start, end)) = subrange.split_once('-') {
            // if the subrange is a range, then parse the start and end values
            if let (Ok(start), Ok(end)) = (start.parse::<u32>(), end.parse::<u32>()) {
                // then iterate over the range and add each node to the nodes vector
                for i in start..=end {
                    nodes.push(format!("{}", i));
                }
            }
        } else {
            // if the subrange does not contain a dash, then it is a single node
            nodes.push(format!("{}", subrange));
        }
    }
    println!("{:?}", range);
    println!("{:?}", nodes);
    nodes
}
