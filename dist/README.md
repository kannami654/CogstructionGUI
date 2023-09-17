パッケージ化したのでウィンドウズで動くと思います。
ToolBoxのConstructionの歯車情報を各々貼り付けて、テキストボックス下部のボタンを押した後に1番下のボタンを押すと実行します。
https://idleontoolbox.com/account/world-3/construction


以下原文

# Cogstruction

"Cogstruction" is a genetic algorithm that produces high quality cog arrays for the construction skill in the game "Legends of Idleon".

I have abandoned this project. I am not responding to questions or requests. Fork and share at your pleasure.

# How to get
There are two options.
1. Using your terminal, navigate to a place where you want to put the code, and copy+paste the following in your terminal: `git clone https://github.com/automorphis/Cogstruction.git`.
2. Click the big green **Code** button on GitHub and click `Download ZIP`. Unzip it wherever you want.  

# How to run
1. [Follow these instructions](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) for downloading Python, setting up a virtual environment, activating it, and installing packages. 
2. This project uses only one package that does not come with a standard Python installation, namely Numpy. After you have set up a virtual environment and activated it, install Numpy by opening a terminal and typing `pip install numpy`.
3. Open the `cog_datas.csv` file using Excel or a similar program and read the data carefully. The data that is currently there should serve as an example of how to fill it out with your own cogs.
4. Delete all the rows of `cog_datas.csv` except for the first one. Fill out the rest of the rows with your own cogs and your characters, including spare cogs on your cog shelf. Exclude any characters you intend to keep on the cog shelf. **Remember to remove cogs from your cog array to see their raw numbers; the numbers you see while they are currently in the cog array have adjacency bonuses already applied.** If you do not do this, the algorithm will give you a suboptimal array.
5. Open the `empties_datas.csv` file suing Excel or a similar program. Look at the data. If the row reads `0, 0`, then that means the lower-left coordinate in the array. If it reads `11, 7`, then that means the upper-right corner. These are the places you have **not** yet unlocked using flaggies.
6. Delete all the rows of `empties_datas.csv` except for the first one. Fill it out with all the places you have not yet unlocked using flaggies. **Remember that these coordinates are zero-indexed; there should be no `x` values more than 11 nor `y` values more than 7.**
7. Using a terminal, navigate to the project directory (using `cd`) and type `python main.py`.
8. Sit back and relax for about 5-15 min, depending on your machine.
9. After the algorithm terminates, open `output.txt` and put the cogs where it tells you to.

# To do

### Bugs
1. ~~You should have at least one more cog in `cog_datas.csv` than you have places to put them. If not, it will result in a bizarre Python error. This is a bug that I need to fix. This should not be a problem for almost all users, since most users have a non-empty cog shelf.~~
2. The algorithm may not place all your characters in the cog array. This is very unlikely, but technically possible. I am going to force the algorithm to always include all your characters.

### Improvements
1. Implement the excogia cog.
2. Implement adjacent player boosts for flaggy speeds.
3. Create a browser extension for automatic loading of Cog data using [Corbeno's API](https://github.com/Corbeno/Idleon-Api-Downloader).
4. Create a handsome output using cog sprites.

# How it works

A genetic algorithm is based off the principle of natural selection. The algorithm works as follows.

1. Randomly instatiate a large population of cog arrays, say 1000. 
2. Randomly pick a cog array *A* from the population. We are going to produce a new cog array from *A* and add it to the population. 
3. There are two ways to produce the new cog array; we decide between the two randomly. Flip a coin. If the coin comes up heads, perform a "one-point mutation" on the cog array *A* (described below). If it comes up tails, randomly pick another cog array *B* from the population and perform a "cross breed" on the two cog arrays *A* and *B* (described below).
   1. One-point mutation: Make a copy *A'* of *A*, and switch a random cog of the copy *A'* with a spare cog from the cog shelf of *A'*. Add the new mutated cog array to the population.
   2. Cross breed: We are going to "blend" the two arrays *A* and *B* in order to produce a third array *C*. For each coordinate, cog arrays *A* and *B* each have their own cog, which could be the same cog. Flip the coin. If it comes up heads, choose the cog from *A* and put it in the corresponding coordinates of *C*. If tails, choose the cog from *B* and put it in the corresponding coordinates of *C*. If the randomly chosen cog has already been placed elsewhere in *C*, just choose any cog that has not alredy been placed. Do this for each coordinate of the cog array. Add *C* to the population.
4. Repeat steps 2-3 for some subpopulation of cog arrays, say a random 500 of the 1000. The new population has size 1500.
5. Assign a single number to each cog array that measures the quality of the array; this is called the "objective" of the array. Higher objectives indicate higher quality. The objective should be a function of the build, flaggy, and exp rates of the array.
6. Sort the cog arrays by their objectives and throw out the bottom 500, leaving only a population of 1000. 
7. Repeat steps 4-6 until you're happy, say 200 times. 
8. Output the array with the highest objective of the current population of 1000.
