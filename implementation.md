# Implementation 
Intuitive approach for Berkeley algo solution design

# Core parts
### 0. main program
1. Runs master node
2. Spin up slave nodes.

### 1. master node
1. Tracks ingoing connections of slave nodes.
2. Requests data from slave nodes.
3. Calculates new time.
4. Sends updates to slave nodes.

### 3. slave node
1. Connects to master node 
2. Disconnects from master node
3. Receives time updates, request codes
4. Sends status code (running?) on demand and termination

### 4. settings
1. Log related strings
2. Setup variables

### 5. utilities
1. Free ports determination
2. Synchronised log printing


## Challenge 1: Node management
function ```simulate_slave_lifecycle``` generates slave nodes on free ports, then kills them after a limited lifetime.
Nodes join and leave the network without disrupting the synchronization process.

## Challenge 2: Fault tolerance - master node reelection