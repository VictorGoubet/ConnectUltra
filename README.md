[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]

<a name="readme-top"></a>
<br />
<div align="center">
  <a href="https://github.com/VictorGoubet/ConnectUltra">
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRq4fznCFt-0SH25M9VBnb9DF_RXRG4y9aX0_J5tcX4d4xFsGQvmEEBrVw1zEPNw5AxyVg&usqp=CAU" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Connect Ultra</h3>

  <p align="center">
    <i>Could a simple AI beats us at connect 4 ?</i>
    <br />
    <a href="https://github.com/VictorGoubet/ConnectUltra/blob/master/ConnectUltra.py"><strong>Check the code »</strong></a>
    <br />
    <br />
    <a href="https://github.com/VictorGoubet/ConnectUltra/issues">Report Bug</a>
    •
    <a href="https://github.com/VictorGoubet/ConnectUltra/issues">Request Feature</a>
  </p>
</div>





## About The Project
</br>

[![Product Name Screen Shot][product-screenshot]](screenshot.PNG)

The connect 4 is a simple game where you have to align four of your coins on a same row, column or diagonal. Usually, this game is played on a 7x6 grid. However, in this imlementation we complicated things by playing on a 12x6 grid.

Could an AI beats us at this simple game? Let's see.

<p align="right"><a href="#readme-top">🔝</a></p>


## Implementation

### Min Max theorem

The AI implementation use a simple and well known algorithm called minmax. This algorithm comes from the Game Theory and can be explained easly. Let's first concider the connect4 game. It's a sequential game, where all players know all the information of the game (eg position of all the coins). This game is not a cooperation game but a null zero sum game where each player action aims to increase its payoff and decrease the opponent's one. Therefore, the players actions tend to follow the MinMax von Neuman theorem where the game can be modelized in a normal shape and each action can be predicted using a backpropagation of the potential payoffs. Let's analyze the following example:

[![Product Name Screen Shot][product-screenshot]](minmax.PNG)


Here we see that the player 0 (max) can predict the payoff brought by each action by simulating for each of theses action the next most probable action of the player1.

### Limitation

This strategy is great, and have wonderful results for simple games. However, it's also a heavy method which require to explore the tree of the game until its end which for the connect4 game (and especially on a 12x6 board) is not possible. One of the optimisation we implemented is the alpha-beta pruning. But even by using this technic, the AI is block at a depth of 4 or 5. We are then forced to implement an heurisitic function which will be charged to approximate the payoff of a state of the board by concidering only the next actions at a depth of 1. The power of the AI is strongly determined by the type of heuristic you implement. 

### Heuristic

We choose to implement the following heuristic:

<img src="https://latex.codecogs.com/svg.image?score&space;=&space;\sum_{\forall&space;a&space;\epsilon&space;actions(s)}^{}&space;(CA&space;*&space;fitness(a)&space;-&space;CD&space;*&space;opponent\_fitness(a))"> </img>

The score of a board state is the sum of the payoff of each actions minus the opponent payoff for each of these actions. Moreover an attack and defense coefficient is added to push to take risky decision or to play for equality. 

Now we can analyse how do we compute the payoff of an action.

<img src="https://latex.codecogs.com/svg.image?Fitness&space;=&space;\sum_{\forall&space;&space;x&space;\epsilon&space;[R,&space;C,&space;D1,&space;D2]}^{}&space;(eval\_crd(x,&space;[player1,&space;player2]))"></img>

Here we compute the score of the action according to its relevancy on the current row, column and on the two diagonals. This score is computed using a simple rule:

*For each 4-subsets of the row/column/diagonal we count how many of the player's coins are in the row and we set the fitness as a polynamial function of this count*

<img src="https://latex.codecogs.com/svg.image?Fitness\_crd(player,&space;crd)&space;=&space;\sum_{\forall&space;&space;x&space;\epsilon&space;4\_subsets}^{}(3^{\sum_{\forall&space;&space;c&space;\epsilon&space;crd}^{}([1\;if\;c\;\epsilon\;player\;else\;0])})"></img>


Were are good with the explanations! Let's move to the tests.

<p align="right"><a href="#readme-top">🔝</a></p>

## Getting Started


### Prerequisites

You will just need python >= 3.0. You can check the version by using the following command.

  ```sh
  > python -V
  > 3.0.0
  ```

### Installation

You can follow the different steps inorder to get the programm working on your computer


1. Clone the repo
   ```sh
   git clone https://github.com/VictorGoubet/ConnectUltra.git
   ```
2. Install python packages
   ```sh
   pip install -r requirements.txt
   ```
3. Execute the python script
   ```sh
   python GameOfLife.py
   ```

The windows should appear! The interface is pretty intuitive, have fun!

<p align="right"><a href="#readme-top">🔝</a></p>





<!-- CONTACT -->
-----
</br>

[![LinkedIn][linkedin-shield]][linkedin-url]
</br>
Victor Goubet - victorgoubet@orange.fr  


<!-- MARKDOWN LINKS & IMAGES -->
[forks-shield]: https://img.shields.io/github/forks/VictorGoubet/ConnectUltra.svg?style=for-the-badge
[forks-url]: https://github.com/VictorGoubet/ConnectUltra/network/members
[stars-shield]: https://img.shields.io/github/stars/VictorGoubet/ConnectUltra.svg?style=for-the-badge
[stars-url]: https://img.shields.io/github/issues/VictorGoubet/ConnectUltra/stargazers
[issues-shield]: https://img.shields.io/github/issues/VictorGoubet/ConnectUltra.svg?style=for-the-badge
[issues-url]: https://github.com/VictorGoubet/ConnectUltra/issues
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/victorgoubet/
[product-screenshot]: screenshot.PNG
