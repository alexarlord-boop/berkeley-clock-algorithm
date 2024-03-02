# Distributed Systems Programming Exercise: Berkeley Clock Synchronization Algorithm
## Overview
Clock synchronization is a fundamental issue in distributed systems, ensuring that all nodes operate on a consistent timeline for event ordering, coordination, and consistency maintenance. This exercise involves implementing the Berkeley Clock Synchronization Algorithm, which aims to synchronize time across multiple nodes within a distributed system. You are free to choose any programming language (e.g., Python, Java, C++, Go) to complete this task.

## Objectives
To grasp the challenges and solutions related to clock synchronization in distributed systems.
To implement the Berkeley Clock Synchronization Algorithm.
To simulate network communication between a master node and several slave nodes.

## Requirements
Proficiency in the chosen programming language.
Understanding of basic networking concepts and inter-process communication.
Familiarity with concurrency and multi-threading if applicable to the chosen language.

## Task Description
### 1. Master Node Implementation
Develop a master node that periodically requests current times from slave nodes.
Calculate the average time offset, excluding the master's own time.
Dispatch an adjustment message to each slave, dictating the clock adjustment needed.

### 2. Slave Node Implementation
Implement slave nodes that, upon request, send their current time to the master.
Adjust their clocks according to the master's adjustment directive.

### 3. Network Communication

Utilize the networking capabilities of your chosen language to facilitate communication between the master and slave nodes.
For simplicity, simulate the entire network within a single machine (localhost), using distinct port numbers for communication.

## Deliverables
### 1. Code for Master and Slave Nodes
Scripts or program files for both the master and slave components of the synchronization algorithm.
### 2. Documentation
A concise report detailing your approach, the chosen programming language, any significant challenges encountered, and solutions devised. Highlight any assumptions or simplifications made during the development process.
### 3. Execution Instructions
Clear instructions on how to compile (if applicable) and run your implementation, including any necessary installation steps for dependencies.

## Evaluation Criteria
+ Functionality: Accurate implementation of the clock synchronization logic as per the Berkeley Algorithm.
+ Code Quality: Clarity, structure, and adherence to best practices in the chosen programming language.
+ Resilience: Consideration of and handling for potential errors or network issues in the implementation.

## Additional Challenges (Optional)
1. Introduce fault tolerance mechanisms to manage the failure of the master node, including master reelection among the slaves.
2. Implement dynamic node management, allowing nodes to join or leave the network without disrupting the synchronization process.

## Submission Guidelines
Submit all source code and documentation.
Ensure your code is adequately commented to explain the implementation logic and major decisions.
Include a README file detailing setup, compilation (if needed), and execution steps.