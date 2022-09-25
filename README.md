# CS 4395 (Human Language Technologies/Natural Language Processing) Portfolio
This is Reg Gonzalez's portfolio for class CS 4395.001 (Human Language Technologies). This portfolio is for the Fall 2022 semester at the University of Texas at Dallas, taught by Karen Mazidi. 


### Assignment 0: Overview of NLP

The objective of this assignment was to create a GitHub portfolio for this class. We also had to write a summary about the historical & current current apporaches to NLP and a paragraph about our own personal interests in NLP; this was called an "Overview of NLP." You can see my "Overview of NLP" pdf [here.](https://github.com/regmckie/CS4395-NLP_Portfolio/blob/main/Overview%20of%20NLP.pdf)


### Assignment 1: Text Processing with Python

The objective of this assignment was to get comfortable programming in Python, using system arguments, creating classes, coding regular expressions, and performing file I/O and pickling. This program takes in an .csv file (titled "data.csv") as an argument, extracts the text from that file, reformats it, and displays the reformatted text onto the screen. There is a class called Person that holds in the text and a .display() function that displays the reformatted text. Finally, there is some pickling involved—essentially we just write the reformatted text into a .p file and read it in to display the information.

You should be able to just run the code normally; however, I worked/ran it through PyCharm. The .py file should already have the data.csv file as a system argument. 

In terms of the strengths and weakness of Python when it comes to text processing, I think a strength of the language is how easy it is to write. Prior to Python, I mostly had experience with C++ and Java, and comparatively speaking, it's much easier to write code in Python than the other two languages. It feels more intuitive and it's not really bogged down by superfluous syntax. Another strength is that there are a lot of useful methods for text processing that make the job a lot easier (e.g., .upper(), .lower(), .capitalize(), etc.). One weakness I've noticed, however, is that sometimes the program loads in slowly, particularly when you run the program for the first time. 

Last semester (Spring 2022), I took CS 4365 (Artificial Intelligence) and CS4375 (Intro to Machine Learning), both of which used Python in their class. Some of this was a review for me (e.g., lists, dictionaries, creating classes, etc.), but some of this was brand new. For example, while I've worked with regular expressions before in other classes, I never did so in Python. I also learned how to read/write pickle files and get experience with sysarg.

You can find the link to my program [here.](https://github.com/regmckie/CS4395-NLP_Portfolio/blob/main/Assignment1/Assignment1_rdg170330.py)


### Assignment 2: Exploring NLTK

The objective of this assignment was to practice using some features of the NLTK library in Python and look over documentation over professional-level natural language processing API. In this assignment, I created a Python notebook using Google Colab, imported and installed some NLTK libraries, and practiced using features of the libraries such as word tokenization, sentence tokenization, lemmatization, stemming, etc. There is also text blocks interspersed amongst the code blocks to give commentary about what exactly I did. 

You can find the link to a PDF printout of my program [here.](https://github.com/regmckie/CS4395-NLP_Portfolio/blob/main/Assignment2_rdg170330.pdf)


### Assignment 3: Word Guessing Game

The objective of this assignment was explore a text file using NLTK libraries in Python, as well as create a word guessing game for users to play. For this assignment, we had to read in a text file called "anat19.txt," tokenize the text from the file, and calculate the lexical diversity. We also had to do some preprocessing on the text, which included reducing the tokens to only alpha characters that weren't in the NLTK stopword list and had a length of > 5. Then, we lemmatized the tokens, made a list of unique lemmas, did POS (part of speech) tagging, and created a list of lemmas that were only nouns.

After all that preprocessing, we used that list of nouns as our word bank for the guessing game. The program would randomly pick a word from that list that the users would have to guess. 

The guessing game was essentially hangman: there would be a line for each letter in the word the user had to guess. The objective was to guess all the letters in the word. If the user accomplished that, the game would run infinitely, continuing to give users new words to guess. There was also a score system implemented. If the user guessed a letter right, their score would increment. If they guessed a letter wrong, their score would decrement. The game would end if the user input the "!" character or if they had a score < 0 (i.e., a negative score).

You can find the link to my program [here.](https://github.com/regmckie/CS4395-NLP_Portfolio/blob/main/Assignment3/Assignment3_rdg170330.py)


### Assignment 4: Exploring WordNet and SentiWordNet

The objective of this assignment was to learn some basic skills using WordNet and SentiWordNet in Python for natural language processing. This assignment is essentially just a series of steps demonstrating the use of both softwares. 

For our exploration with WordNet, some of these steps include: outputting the synsets of a noun; using the .defintion(), .examples(), and .lemmas() functions associated with that noun; outputting the hypernyms, hyponyms, meronyms, etc. of that nouns; etc. We also had to traverse the WordNet noun hierarchy, run the Wu-Palmer similarity metric, and run the Lesk algorithm.

For our exploration with SentiWordNet, we found the senti-synets of an "emotionally-charged word," output its polarity/sentiment scores, and finally create a sentence and output the sentiment scores for  each word in that sentence.

In the last part of this assignment we explore collocations a bit as well. We had to output the collocations of a specific text (i.e., text4, the Inaugural corpus) and calculate the point-wise mutual information, or PMI, score for one of those collocations. 

You can find the link to a PDF printout of my program [here.]
