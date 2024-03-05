# Report: Berkeley Clock Synchronization Algorithm
### CS-351 Distributed Systems

## Programming language, tools
Python
1. threading -- parallel distributed components (nodes) simulation
2. time -- main algorithm purposes
3. socket -- nodes connection
4. random -- creating a time bias across nodes

## Challenges encountered and solutions devised.
1. Inconsistent logging due to threading -- ```SynchronizedPrinter``` class
2. Inconsistent port allocation -- ```find_free_ports``` function
3. A lot of customizable parameters involved -- ```settings.py```

## Assumptions or simplifications made during the development process.
