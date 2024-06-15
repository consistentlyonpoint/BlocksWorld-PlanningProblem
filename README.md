# Blocks World Problem w/ Planning

## Overview
This report presents an ai agent designed to solve a given Blocks World Problem.  The agent solves for the sequence of actions to reach a goal state. The agent presented offers a linear-time algo-rithm to build a sequence of action to move the blocks to the goal state.

## The Transportation Problem
In this assignment, the algorithm is presented a **classical planning problem** of domain Blocks World (BW). Russell & Norvig (2020) describe BW domain as
>“…a set of cube-shaped blocks sitting on an arbitrarily-large table. The blocks can be stacked, but only one block can fit directly on top of another. A robot arm can >pick up a block and move it to an-other position, either on the table or on top of another block. The arm can pick up only one block at a time, so it cannot pick up a >block that has another one on top of it.” (Russell, 2020)

In Figure 1, the sample BW problem has a set of 3 blocks with a goal state of stacking all blocks in a single column, starting at the bottom with block ‘C’, then ‘B’, and ‘A” at the top. 

<figure>
  <img src="https://github.gatech.edu/storage/user/36047/files/81a77679-1b0e-43e9-958a-1be850126b0f" alt="Alt text">
  <figcaption>Figure 1: “Diagram of the blocks-world problem”. (Russell, 2020).</figcaption>
</figure>

## Funcionality
The agent uses a planning approach to find the sequence. The algorithm uses re-cursion with a recursive count cap per block per method. Neither Generate nor Test are used. For each action of moving a block, the agent does use a set of re-quirements. Functions and Boolean checks, defined in Figure-2, include On(b, x) – block ‘b’ is on ‘x’ (‘x’ is either another block or ‘Table’); Clear(‘x’) – returns True if nothing is on ‘x’ (always True for ‘x’ == ‘Table’). 

<figure>
        <img src="https://github.gatech.edu/storage/user/36047/files/a39507b6-a138-4342-8820-6d61986e89ea" alt="Alt text">
        <figcaption>Figure 2: Blocks-world planning problem with methods for Move and MoveToTable (Russell, 2020).</figcaption>
</figure>

For the problem in Figure 1, a sequence solution, using the terminology from Figure 2, is MoveToTable (‘C’, ‘A’), Move(‘B’, ‘Table’, ‘C’), Move(‘A’, ‘Table’, ‘B’).

### 2.1	Unstack-Stack
The initial version of the agent uses a non-efficient, linear-time algorithm of Un-stack-Stack (US). Presented by Slaney & Thiébaux (2001), the algorithm, captured in Figure 3, unstacks all blocks in the initial state, then stacks the blocks. Un-stacking all blocks has the Effect of all blocks, ‘b’, return true for Clear(‘b’). 
 
<figure>
    <img src="https://github.gatech.edu/storage/user/36047/files/cb724d0e-3442-4afb-abc0-784bf35e80ba" alt="Alt text">
    <figcaption>Figure 3: The Unstack-Stack Algorithm (Slaney, 2001).</figcaption>
</figure>

#### Performance
The agent, employing the US algorithm, finds a sequence to reach goal state for all local and submission test cases. The number of blocks has no bearing on the success of the agent finding a valid sequence. However, the agent only returns an optimal path in 50% (10/20) of the submission test cases. Although, scaling is not a factor in optimality.

## Efficiency
Slaney & Thiébaux tested the US and GN1 algorithms for time performance and plan length/solution quality. Below, Figure 4 includes their findings for time and Figure 5 captures “average plan length” (Slaney, 2001). 
 
<figure>
    <img src="https://github.gatech.edu/storage/user/36047/files/fd980b4f-8d25-4d01-b621-dee9edf2ee53" alt="Alt text">
    <figcaption>Figure 4: Evaluation of search algorithms. is the branch-ing factor; is the maximum depth of the search tree; is the depth of the shallowest solution. (Slaney, 2001).</figcaption>
</figure>

<figure>
  <img src="https://github.gatech.edu/storage/user/36047/files/a597dc98-52be-4cfc-bc88-fcd715b967c5">
  <figcaption>Figure 5: Figure 5—	“Average plan length as a function of n: (num-ber of moves)/n”. (Slaney, 2001).</figcaption>
</figure>

Slaney & Thiébaux found the average plan lengths converge when approaching the worst case, with length approximately 2*n – 2, where ‘n’ is input size of the problem.

## References
1. Russell, S. J., & Norvig, P. (2020). Artificial intelligence: A Modern Approach. 4th Edition, Prentice-Hall, Upper Saddle River.
2. Slaney, J., Thiébaux, S. (2001). Blocks World revisited, Artificial Intelli-gence, 125 (1-2), pp. 119-153. doi: 10.1016/S0004-3702(00)00079-5
