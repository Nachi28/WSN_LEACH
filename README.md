# WSN Simulation using LEACH Protocol

This Python code simulates a Wireless Sensor Network (WSN) using the LEACH (Low Energy Adaptive Clustering Hierarchy) protocol. It models sensor nodes, energy consumption, packet loss, and cluster head formation to study the performance of the network. The code generates output data like Packet Delivery Ratio (PDR) and End-to-End Delay (E2E Delay), saving results to an Excel file.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Installation

1. Install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/).
2. Install Visual Studio Code from [https://code.visualstudio.com/](https://code.visualstudio.com/).
3. Clone this repository or download the ZIP file.
4. Open the project folder in Visual Studio Code.
5. Install the required Python libraries:
```
pip install numpy matplotlib openpyxl pandas
```

## Usage

1. Delete the existing `hi.xlsx` file in the project directory, if present.
2. Create a new Excel file in the project directory and copy its full path.
3. Open `run_Leach.py` and `wsn_final.py` scripts and replace references to `hi.xlsx` with the new file path.
4. Run the `run_Leach.py` script to start the simulation.
5. To view the generated plots, run the `wsn_project_prototype.py` script.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Code Structure

### Libraries Used

- **NumPy**: For numerical operations, like generating random numbers and performing mathematical calculations.
- **Matplotlib**: For plotting graphs to visualize the sensor network.
- **openpyxl**: For reading from and writing to Excel files.
- **pandas**: For data manipulation and analysis, especially for processing Excel files.

### Classes

#### WSN
Defines the WSN architecture and contains constants for energy consumption, distance calculations, and packet loss.

**Attributes**:
- `xm`, `ym`: Dimensions of the area.
- `n`: Total number of nodes.
- `sink`: Sink node.
- `nodes`: All sensor nodes.
- `ETX`, `ERX`, `Efs`, `Emp`, `EDA`: Energy model constants.
- `bitrate`: Data transmission bitrate.
- `f_r`: Fusion rate for packet loss.
- `CM`, `DM`: Control message size and data size.
- `do`: Distance threshold.
- `m_n`: Number of malicious nodes.
- Node state tracking attributes (`n_dead`, `flag_first_dead`, etc.)

#### Node
Represents a sensor node in the network. Initializes nodes, including normal and malicious nodes, and plots the network.

**Attributes**:
- `id`: Node identifier.
- `xm`, `ym`: Coordinates.
- `energy`: Energy level.
- `packets`: Data packets.
- `type`: Node type (normal or cluster head).
- `G`: Cluster head flag.
- `head_id`: ID of the cluster head it is associated with.

#### Leach
Implements the LEACH protocol, handling cluster head selection, cluster formation, and data transmission phases. Calculates PDR and E2E Delay and manages simulation rounds.

**Attributes**:
- `p`: Probability of being selected as a cluster head.
- `period`: Cycle period.
- `heads`, `members`: Lists of cluster heads and non-cluster head members.
- `cluster`: Cluster dictionary.
- `r`: Current round.
- `r_empty`: Count of empty rounds.
- `totalpdrfor_N`, `avg_EtoE_Delay_for_eachN`: Performance metrics.

### Functions

- `dist(x, y)`: Calculates the distance between two nodes.
- `trans_energy(data, dis)`: Computes the energy consumed for transmitting data over a given distance.
- `node_state(r)`: Updates the state of nodes (alive or dead) based on their energy levels.
- `init_nodes()`: Initializes normal sensor nodes.
- `init_malicious_nodes()`: Initializes malicious sensor nodes.
- `plot_wsn()`: Plots the WSN showing normal nodes, malicious nodes, and the base station.
- `optimum_number_of_clusters()`: Calculates the optimal number of clusters.
- `cluster_head_selection()`: Selects cluster heads based on a threshold probability.
- `cluster_formation()`: Forms clusters by associating non-cluster head nodes with the nearest cluster head.
- `to_excel(data)`: Appends data to an existing Excel file.
- `set_up_phase()`: Executes the setup phase of LEACH, including cluster head selection and cluster formation.
- `end_to_end_delay(distance, delivered_packets, bitrate)`: Calculates the E2E Delay for packet transmission.
- `steady_state_phase()`: Simulates the steady-state phase where cluster members send data to the cluster head, and the cluster head sends data to the base station.
- `leach()`: Runs the LEACH protocol for one round.
- `run_leach()`: Runs the LEACH protocol until all nodes are dead.

## Output
The output of the simulation includes:

- Total Rounds: The number of rounds until all nodes are dead.
- Avg PDR for N nodes: The average Packet Delivery Ratio for the given number of nodes.
- Avg End-to-End Delay of each node: The average E2E Delay for the given number of nodes.


