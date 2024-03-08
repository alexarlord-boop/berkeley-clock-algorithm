# Report: Berkeley Clock Synchronization Algorithm
### CS-351 Distributed Systems

[Task description in detail](/task.md)

[Solution contents in detail](/implementation.md)

## Programming language, libs
Python
1. threading -- parallel distributed components (nodes) simulation
2. time -- Berkeley algorithm purposes
3. socket -- nodes connection
4. random -- creating a time bias across nodes

## Challenges encountered and solutions devised.
1. Inconsistent logging due to threading -- [SynchronizedPrinter](/utilities/logging.py) class
2. Inconsistent port allocation -- [find_free_ports](/utilities/ports.py) function
3. A lot of customizable parameters involved -- [settings.py](/settings.py)

## Assumptions or simplifications made during the development process.
1. Master and Slave nodes are independent entities (classes) without interchangeable functionality.
2. To obtain time data from the slave nodes, master node initiate a thread lock for exclusive access to shared resources.
3. In order to show dynamic slave node management, a simulation function ```simulate_slave_lifecycle``` is created.

## Improvements and TODOs.
1. For the fault tolerance challenge, master and slave nodes should be interchangeable.
