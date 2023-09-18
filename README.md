# GUI追加にあたっての追記部分
pythonをインストールしない人にも使えるようにしたい思い、GUIで操作できるように変更し、実行ファイル単体で動くように想定したものです。  
よってGUIを追加する部分のみの追加であり、元々の計算のメイン部分は変更しておりません。  
ソースいらないよって人はBuildの中のEXEfile.zipだけダウンロードでOKです。　　
distの方にもありますが、こっちはウイルスバスターとかが反応しちゃうかもしれません。  
中にあるexeファイル起動で立ち上がります。  
計算にはCPU負荷がそれなりにかかります。  
  
# ライブラリ関係  
GUIを使うのでPySimpleGUIが必要です。また、機能追加のためにpandasを使用しています。  
コードで動かす人は、main.pyを実行すればGUIが立ち上がります。  
mainに組み込んでしまったので、コードだけでさっくり動かしたい方は本家をご参照ください。  

# 使用方法
本プログラムの実行に[Idleon Toolbox](https://idleontoolbox.com/)を使用する箇所がございます。  
予めログインしておくことをお勧めします。  
画面の上部にもリンクをつけてあるのでそちらをクリックでもToolboxへ辿り着けます。  
このリンクはConstructionへの直リンクなので、ログイン済みであればすぐに歯車画面へ飛びます。  

1. ToolboxでコピーしたCogstruction Data（クリックするだけで良い）を左のテキストボックスに入れ、「Write COG」すると必要な `cog_datas.csv` が生成されます。（**必須**）。  
2. 同様にCogstruction Emptiesを右のテキストボックスに入れ、「Write EMP」で、 `empties_datas.csv` を生成します（**必須**）。  
3. GUI独自機能として「推す」ボタンで歯車生成に配置するキャラクタなどを計算から除外できます。  
 推さないキャラは配置されません。  
 よって下記バグの2は、この機能を使えば、解消できると思っていただいて結構です。  
 ボタンを押さない、あるいは全員推してチェックをつけると全キャラ配置されます。  
 注意点として、元々配置しているキャラクタも除外することが可能ですが、その場合インベに余っている歯車がないと計算ができないつくりになっています。  
4. その後、「押忍」で配置の計算を実行します。  
 計算には時間がかかりますので、リラックスしてしばらくお待ちください。  
 進捗はprogress barに表示されますが、途中で終了することがあります（最大の世代数を最大値に設定しているため、途中で打ち切りがあると一気に終わる）。
5. 完了すると、表示されているディレクトリに `output.txt` が生成されます。
 このデータの歯車情報を元に並び替えると、パラメータがGUI右下の枠の中にある数値になります。
 括弧内に今の配置から比較した、各数値の上昇幅を記載しております。 
 並び替えの費用対効果としてご参考にお願いいたします（並び替えは手動なので、1時間くらいかかると思います）。  
 なお、**必ずしもすべてのステータスが上昇するものではありません。**  
 ビルドレート＞フラグレート＞＞経験値ボーナスの順に重み付けされています。  
6. 生成されたテキストの中に、元々配置してあったXY座標（Pre-Coords）を追記しています。左下角が(0,0)です。  
 左がX,右がY座標です。  
 歯車生成にあたっているキャラクタ、配置していない歯車は、**歯車生成にあたっているキャラ左から右、そしてインベの歯車の左上から右の順に**spare#0,1,2…とナンバリングされます。  

# 並べ替え手順について
これが非常に困難ですが、並べ替えに関するTipsを紹介します。  
まず、テキストの下の方にあるSpare Cogを探します。  
このスペアは、このプログラムで検討した配置では使用しない歯車ですので、このスペアの中で、元々盤内に配してあった（PreーCoordがspare#nでない）歯車を探し、まずそれらをすべて取り除きます。  
すると盤内に空いたスペースができますので、その座標にどんどんと歯車を追加して順次繰り返していけば、混乱なく並べ替えができるはずです。  
それでも時間がかかるのはご愛嬌。  

## 以下はオリジナルの原文（英語）
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
