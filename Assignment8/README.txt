FILENAME:	README.txt (for Assignment 8: Chatbot Project)
DUE DATE:	11/13/2022
AUTHOR:		Reg Gonzalez
EMAIL:		rdg170330@utdallas.edu
COURSE:		CS 4395.001 (Fall 2022)
VERSION:	1.0

-------------------------------------------------------------

PROGRAM DESCRIPTION:

The objective of this assignment was to create a chatbot using some of the NLP techniques
we learned in class. 

The specific type of chatbot I implemented was a task-oriented dialogue agent that
specifically had knowledge about the movie "The Nightmare Before Christmas" (1993). The
chatbot specializes in answering questions about the movie using knowledge base that I created.
The knowledge base consists of several statements and facts about the movie that serve as 
potential responses when the uer asks the chatbot a question You can also ask the chatbot to
give you a fun fact, in which it will respond with a random fun fact that's also in the knowledge
base. 

I used several NLP techniques for this chatbot including tokenization, lemmatization, tf-idf
vectorization, and cosine similiarity. The chatbot also saves user information. The information
it can save is the user's name as well as their likes/dislikes about the movie.

HOW TO EXECUTE PROGRAM:

This program was made and run through an IDE (PyCharm, specifically). To run the program,
simply run it like you would any other in an IDE. An important thing to note is that I
used the punkt, wordnet, and omw-1.4 libraries in order to create my chatbot. Starting at
line 11 in the code, you can see these libraries that I downloaded. I commented them out
because I only needed to download/run them once in order to get my chatbot working. If you
don't already have those libraries downloaded, make sure to get them before running my chatbot.
