# Iterated Prisoner's Dilemma Analysis Tool

[![Static Badge](https://badgen.net/pypi/v/IPD-axelrod?icon&color=green)](https://pypi.org/project/IPD-axelrod/)

## About

This is a tool to simulate the Iterated Prisoner's Dilemmma. To install, run: 
    `pip install IPD-axelrod`
You can then use it like this:
    `python3 -m IPD`
    Note that `IPD-axelrod` is only used for instalation - after that, use IPD

## The Prisoner's Delemma
The "prisoner's dilemma" is a scenario in game theory where two participants must independently choose to either cooperate for a mutual gain or betray the other for a greater personal gain. If both participants choose to betray one another, the total gain for both participants is lower than if both participants had just cooperated. This README assumes a basic understanding of this scenario and its reward schemes. To learn more, you can visit the [Wikipedia page](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma).

In the _iterated_ prisoner's dilemma, two players continuously play out the scenario for a given number of rounds and aim to maximize their total gain. The way a player behaves each round is determined by its _strategy_. Should a player aim to be as cooperative as possible? Or maybe seek to exploit their partner? Maybe a mix of both?

The motivation behind this project is to create a tool that can answer these questions through data visualization.

An initial "population", consisting of players each with its own strategy, plays the iterated prisoner's dilemma game. In each _generation_, each player plays against every other player in the population. Successive generations are created based on how effective each strategy was at producing gain. Strategies that were more effective in a given generation are more likely to produce offspring in the next generation to carry on their strategy. The population distribution over the course of each generation is then graphed.
  
tl;dr Strategies compete. Better strategies reproduce more successfully. Repeat. Graph.
 
## Brief Overview of Some Strategies
Strategies are a predetermined set of rules to play to iterated Prisoner's Dilemma game. Some of the strategies implemented in this project are listed below.
  * Kantian: 
  
     Always cooperates
     
  * Defector:
  
     Always betrays
     
  * Tit-for-Tat:
  
     Aims to cooperate. If the opponent betrayed in the last round, then betrays.
     
  * Tit-for-2-Tats:
  
     Aims to cooperate. If the opponent betrayed in the last two rounds, then betrays.
  
  * Tester: 
  
     The "Tit-for-2-Tats" exploiter. It acts cooperatively at first, but "tests" randomly by betraying and following up with a turn of cooperation. If the opponent doesn't retaliate, then it switches off between cooperating and betraying for the rest of the game.
  
  * ...and many more!

## License
The code within this repository is MIT licensed. See [LICENSE](./LICENSE) for details.
