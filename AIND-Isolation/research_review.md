
[NOTE THIS IS STILL A WORK IN PROGRESS]

# Review: Mastering the game of Go with deep neural networks and tree search

A review of the article published in Nature[link] by the Google DeepMind[link] team in which they describe how they built the famous AlphaGo.
This review is written in partial fulfillment of the Nanodegree in Artificial Intelligence (AIND) by Udacity[link to AIND].

## Article Overview

* What is described in this article?
* How did they do what they described?
* What makes it special?
* Results

## Goals

The goals laid out by the authors of this paper were two-fold. Firstly, they wanted to showcase the exciting possibilities of _deep learning_ by improving on the current state of the art in GO game playing agents to such a level previously thought impossible. Secondly, they wanted to move beyond the realm of conventional game playing agents and implement the concept of _self playing_ through _reinforcement learning_.


## Design Implementation

The authors set out to achieve their goals by the introduction two new types of board evaluation methods: _value networks_ and _policy networks_.

These evaluation methods were inspired by the recent advancements of convolutional neural networks (CNNs) in the domain of computer vision. The basic premise was to train a _value network_ to assign values (or weights) to each board position, indicating which positions provide a positional advantage.

Then, make a decision about which move to make next, they built two policy networks:
* $\rho_{\sigma}$: Trained on annotated expert moves using Supervised Learning (SL)
* $\rho_{\rho}$: Improving $\rho_{\sigma}$ through Reinforcement Learning (RL)


[TODO]


## Results

The results presented in this paper are unprecedented and caused a global upset, with experts predicting these results would only be achievable within  the next decade at best. Through the combination of the novel 'value networks' and 'policy networks' to evaluate and choose new board positions, AlphaGo defeated Fan Hui, the European Go champion by 5 games to 0, and boasts a 99.8% winning rate against other Go playing programs.
