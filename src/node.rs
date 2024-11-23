use std::error::Error;

#[derive(Debug, Default)]
pub struct Node {
    pub name: String,
    pub arch: Option<String>,
    pub cores_per_socket: Option<u32>,
    pub cpu_alloc: Option<u32>,
    pub cpu_effective: Option<u32>,
    pub cpu_total: Option<u32>,
    pub cpu_load: Option<f64>,
    pub available_features: Vec<String>,
    pub active_features: Vec<String>,
    pub gres: Option<String>,
    pub addr: Option<String>,
    pub hostname: Option<String>,
    pub version: Option<String>,
    pub os: Option<String>,
    pub real_memory: Option<u32>,
    pub allocated_memory: Option<u32>,
    pub free_memory: Option<u32>,
    pub sockets: Option<u32>,
    pub boards: Option<u32>,
    pub mem_spec_limit: Option<u32>,
    pub state: Option<String>,
    pub threads_per_core: Option<u32>,
    pub tmp_disk: Option<u32>,
    pub weight: Option<u32>,
    pub owner: Option<String>,
    pub mcs_label: Option<String>,
    pub partitions: Vec<String>,
    pub boot_time: Option<String>,
    pub slurmd_start_time: Option<String>,
    pub last_busy_time: Option<String>,
    pub resume_after_time: Option<String>,
    pub cfg_tres: Option<String>,
    pub alloc_tres: Option<String>,
    pub cap_watts: Option<String>,
    pub current_watts: Option<u32>,
    pub ave_watts: Option<u32>,
    pub ext_sensors_joules: Option<String>,
    pub ext_sensors_watts: Option<u32>,
    pub ext_sensors_temp: Option<String>,
    pub reservation_name: Option<String>,
    pub reason: Option<String>,
}
impl Node {
  pub fn from_fields(fields: &[(&str, &str)]) -> Self {
      let mut node = Node::default();

      for (key, value) in fields {
          match *key {
              "NodeName" => node.name = value.to_string(),
              "Arch" => node.arch = Some(value.to_string()),
              "CoresPerSocket" => node.cores_per_socket = value.parse().ok(),
              "CPUAlloc" => node.cpu_alloc = value.parse().ok(),
              "CPUEfctv" => node.cpu_effective = value.parse().ok(),
              "CPUTot" => node.cpu_total = value.parse().ok(),
              "CPULoad" => node.cpu_load = value.parse().ok(),
              "AvailableFeatures" => {
                  node.available_features = value.split(',').map(String::from).collect();
              }
              "ActiveFeatures" => {
                  node.active_features = value.split(',').map(String::from).collect();
              }
              "Gres" => node.gres = Some(value.to_string()),
              "NodeAddr" => node.addr = Some(value.to_string()),
              "NodeHostName" => node.hostname = Some(value.to_string()),
              "Version" => node.version = Some(value.to_string()),
              "OS" => node.os = Some(value.to_string()),
              "RealMemory" => node.real_memory = value.parse().ok(),
              "AllocMem" => node.allocated_memory = value.parse().ok(),
              "FreeMem" => node.free_memory = value.parse().ok(),
              "Sockets" => node.sockets = value.parse().ok(),
              "Boards" => node.boards = value.parse().ok(),
              "MemSpecLimit" => node.mem_spec_limit = value.parse().ok(),
              "State" => node.state = Some(value.to_string()),
              "ThreadsPerCore" => node.threads_per_core = value.parse().ok(),
              "TmpDisk" => node.tmp_disk = value.parse().ok(),
              "Weight" => node.weight = value.parse().ok(),
              "Owner" => node.owner = Some(value.to_string()),
              "MCS_label" => node.mcs_label = Some(value.to_string()),
              "Partitions" => {
                  node.partitions = value.split(',').map(String::from).collect();
              }
              "BootTime" => node.boot_time = Some(value.to_string()),
              "SlurmdStartTime" => node.slurmd_start_time = Some(value.to_string()),
              "LastBusyTime" => node.last_busy_time = Some(value.to_string()),
              "ResumeAfterTime" => node.resume_after_time = Some(value.to_string()),
              "CfgTRES" => node.cfg_tres = Some(value.to_string()),
              "AllocTRES" => node.alloc_tres = Some(value.to_string()),
              "CapWatts" => node.cap_watts = Some(value.to_string()),
              "CurrentWatts" => node.current_watts = value.parse().ok(),
              "AveWatts" => node.ave_watts = value.parse().ok(),
              "ExtSensorsJoules" => node.ext_sensors_joules = Some(value.to_string()),
              "ExtSensorsWatts" => node.ext_sensors_watts = value.parse().ok(),
              "ExtSensorsTemp" => node.ext_sensors_temp = Some(value.to_string()),
              "ReservationName" => node.reservation_name = Some(value.to_string()),
              "Reason" => node.reason = Some(value.to_string()),
              _ => {} // Ignore any unknown keys
          }
      }

      node
  }

    /// Parse the `scontrol` output into a vector of `Node` structs.
    pub fn parse_nodes(output: &str) -> Result<Vec<Self>, Box<dyn Error>> {
        let mut nodes = Vec::new();

        for line in output.lines() {
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

            nodes.push(Node::from_fields(&fields));
        }

        Ok(nodes)
    }
}

// tests for the node.rs file
#[cfg(test)]
mod tests {
    use super::*;

      #[test]
      fn test_node_from_fields() {
          let fields = vec![
              ("NodeName", "node1"),
              ("Arch", "x86_64"),
              ("CoresPerSocket", "2"),
              ("CPUAlloc", "1"),
              ("CPUEfctv", "1"),
              ("CPUTot", "2"),
              ("CPULoad", "0.00"),
              ("AvailableFeatures", "feature1,feature2"),
              ("ActiveFeatures", "feature1"),
              ("Gres", "gpu:1"),
          ];

          let node = Node::from_fields(&fields);

          assert_eq!(node.name, "node1");
          assert_eq!(node.arch, Some("x86_64".to_string()));
          assert_eq!(node.cores_per_socket, Some(2));
          assert_eq!(node.cpu_alloc, Some(1));
          assert_eq!(node.cpu_effective, Some(1));
          assert_eq!(node.cpu_total, Some(2));
          assert_eq!(node.cpu_load, Some(0.00));
          assert_eq!(node.available_features, vec!["feature1".to_string(), "feature2".to_string()]);
          assert_eq!(node.active_features, vec!["feature1".to_string()]);
          assert_eq!(node.gres, Some("gpu:1".to_string()));
        }

      #[test]
      fn test_node_from_fields_partial() {
        let fields = vec![
          ("NodeName", "node2"),
          ("Arch", "arm64"),
        ];

        let node = Node::from_fields(&fields);

        assert_eq!(node.name, "node2");
        assert_eq!(node.arch, Some("arm64".to_string()));
        assert_eq!(node.cores_per_socket, None);
        assert_eq!(node.cpu_alloc, None);
        assert_eq!(node.cpu_effective, None);
        assert_eq!(node.cpu_total, None);
        assert_eq!(node.cpu_load, None);
        assert!(node.available_features.is_empty());
        assert!(node.active_features.is_empty());
        assert_eq!(node.gres, None);
      }

      #[test]
      fn test_node_from_fields_empty() {
        let fields: Vec<(&str, &str)> = vec![];

        let node = Node::from_fields(&fields);

        assert_eq!(node.name, "");
        assert_eq!(node.arch, None);
        assert_eq!(node.cores_per_socket, None);
        assert_eq!(node.cpu_alloc, None);
        assert_eq!(node.cpu_effective, None);
        assert_eq!(node.cpu_total, None);
        assert_eq!(node.cpu_load, None);
        assert!(node.available_features.is_empty());
        assert!(node.active_features.is_empty());
        assert_eq!(node.gres, None);
      }

      #[test]
      fn test_node_from_fields_invalid_values() {
        let fields = vec![
          ("NodeName", "node3"),
          ("CoresPerSocket", "invalid"),
          ("CPUAlloc", "invalid"),
          ("CPULoad", "invalid"),
        ];

        let node = Node::from_fields(&fields);

        assert_eq!(node.name, "node3");
        assert_eq!(node.cores_per_socket, None);
        assert_eq!(node.cpu_alloc, None);
        assert_eq!(node.cpu_load, None);
      }

    #[test]
    fn test_parse_nodes() {
        let output = "\
            NodeName=node1 Arch=x86_64 CoresPerSocket=2 CPUAlloc=1 CPUEfctv=1 CPUTot=2 CPULoad=0.00 AvailableFeatures=feature1,feature2 ActiveFeatures=feature1 Gres=gpu:1\n\
            NodeName=node2 Arch=arm64";

        let nodes = Node::parse_nodes(output).unwrap();

        assert_eq!(nodes.len(), 2);
        assert_eq!(nodes[0].name, "node1");
        assert_eq!(nodes[0].arch, Some("x86_64".to_string()));
        assert_eq!(nodes[0].cores_per_socket, Some(2));
        assert_eq!(nodes[0].cpu_alloc, Some(1));
        assert_eq!(nodes[0].cpu_effective, Some(1));
        assert_eq!(nodes[0].cpu_total, Some(2));
        assert_eq!(nodes[0].cpu_load, Some(0.00));
        assert_eq!(nodes[0].available_features, vec!["feature1".to_string(), "feature2".to_string()]);
        assert_eq!(nodes[0].active_features, vec!["feature1".to_string()]);
        assert_eq!(nodes[0].gres, Some("gpu:1".to_string()));

        assert_eq!(nodes[1].name, "node2");
        assert_eq!(nodes[1].arch, Some("arm64".to_string()));
        assert_eq!(nodes[1].cores_per_socket, None);
        assert_eq!(nodes[1].cpu_alloc, None);
        assert_eq!(nodes[1].cpu_effective, None);
        assert_eq!(nodes[1].cpu_total, None);
        assert_eq!(nodes[1].cpu_load, None);
        assert!(nodes[1].available_features.is_empty());
        assert!(nodes[1].active_features.is_empty());
        assert_eq!(nodes[1].gres, None);
    }
}