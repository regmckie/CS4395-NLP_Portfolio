import sys
import os
import re
import nltk
import random
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def preprocess_text(raw_text):
    """
    Performs preprocessing on raw text (e.g., tokenization, lemmatizing, tagging, etc.)
    :param raw_text: The raw text from anat19.txt (the input file)
    :return (tokens_anat19, nouns): A list of tokens from the text & a list of nouns from the text
    """

    # Before doing preprocessing on the text, calculate and
    # display the lexical diversity

    # Tokenize the text
    tokens_of_raw_text = word_tokenize(raw_text)

    # Get the number of unique tokens
    unique_tokens = set(tokens_of_raw_text)

    # Calculate and display the lexical diversity
    print("\nLexical diversity of 'anat19.txt': %.2f" % (len(unique_tokens) / len(tokens_of_raw_text)))

    # Make the text lowercase & reduce the tokens to only those that are alpha, not in
    # the list of stopwords, and have a length of > 5
    tokens_anat19 = [token.lower() for token in tokens_of_raw_text if token.isalpha() and
                     token not in stopwords.words('english') and len(token) > 5]

    # Lemmatize the tokens
    wnl = WordNetLemmatizer()
    tokens_lemmatized = [wnl.lemmatize(token) for token in tokens_anat19]

    # Create a list of unique lemmas
    unique_lemmatized_tokens = list(set(tokens_lemmatized))

    # Tag the list of unique lemmas and print the first 20 tags
    tagged_unique_lemmas = nltk.pos_tag(unique_lemmatized_tokens)
    print("\nList of first 20 tagged lemmas: ", tagged_unique_lemmas[:20])

    # Create a list of lemmas that are only NOUNS
    nouns = [word for word,tag in tagged_unique_lemmas if (tag == "NN" or tag == "NNS"
                                                           or tag == "NNP" or tag == "NNPS")]

    # Print the number of tokens and the number of nouns
    print("\nNumber of tokens from 'anat19.txt': ", len(tokens_anat19))
    print("Number of nouns from 'anat19.txt': ", len(nouns))

    # Return tokens and nouns
    return (tokens_anat19, nouns)


def make_dictionary(tokens, nouns):
    """
    Makes a dictionary of {noun:count of noun in tokens}
    :param tokens: A list of tokens from anat19.txt
    :param nouns: A list of nouns from anat19.txt
    :return list_sorted_nouns: A list of the 50 most common nouns from anat19.txt
    """

    # Create dictionary of {noun:count of noun in tokens}
    noun_count = {t:tokens.count(t) for t in nouns}

    # Sort the dictionary
    sorted_nouns = sorted(noun_count.items(), key = lambda x: x[1], reverse = True)

    # Print out the 50 most common nouns
    print("\n50 most common nouns and their counts:")
    for counter in range(50):
        print(sorted_nouns[counter])

    # Save sorted nouns into a list that'll be used for the guessing game
    list_sorted_nouns = []
    index = 0
    for noun in sorted_nouns:
        list_sorted_nouns.append(noun[0])
        index = index + 1
        if index > 49:  # Once we get the first 50 nouns, then break out of the loop
            break

    # Return list of 50 most common nouns
    return list_sorted_nouns


def guessing_game(fifty_sorted_nouns, points):
    """
    Creates a word guessing game for the user—like hangman. The user will
    guess a letter for the given word. If the letter is in the word, the user's score
    will be incremented. If the letter isn't in the word, the user's score will
    be decremented. The game goes on infinitely until the user inputs the "!"
    character or until they get a negative score.
    :param fifty_sorted_nouns: A list of words. One will randomly be chosen for the user to guess.
    :param points: The cumulative points the user has.
    :return: N/A
    """
    print("\nLet's play a word guessing game!")

    # Randomly choose one of the words from the 50 nouns
    word_to_guess = random.choice(fifty_sorted_nouns)

    # To store the user's guess
    user_guesses = ""

    # Keep playing the game until the user has a negative score
    # or until they enter the "!" character
    while user_guesses != "!" or points > 0:

        # Boolean variable to see if user guessed word right
        word_guessed_right = True

        # Print out the character if user guessed it right
        # and an underscore if user guessed it wrong
        for character in word_to_guess:
            if character in user_guesses:
                print(character)
            else:
                print("_")
                word_guessed_right = False

        # If word_guessed_right == True, that means the user won.
        # Recursively call the game to continue playing (and keep
        # a cumulative score)
        if word_guessed_right:
            print("You solved it!")
            print("The word was: ", word_to_guess)
            guessing_game(fifty_sorted_nouns, points)

        # Prompt the user for their guess and add
        # their guess to a list of guesses
        guess = input("Guess a letter: ")
        user_guesses = user_guesses + guess

        if guess is "!":
            print("Thanks for playing! See you again next time!")
            exit()
        elif guess in word_to_guess:
            points = points + 1     # Increment points if user guesses correctly
            print("Right! Score is ", points)
            print("List of letters you've guessed: ", set(user_guesses))
        elif guess not in word_to_guess:
            points = points - 1     # Decrement points if user guesses wrong
            print("Sorry, guess again. Score is ", points)
            print("List of letters you've guessed: ", set(user_guesses))
            if points == 0:
                print("Be careful! If your score goes negative, you will lose the game")

            # If score < 0, then the user has lost, so exit the program
            if points < 0:
                print("Uh-oh! Score is less than 0. You lost.")
                print("The word was: ", word_to_guess)
                exit()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        # If no system argument is present, print an error message
        # and exit the program
        print("ERROR: No system argument for 'anat19.txt'. Terminating program now...")
        exit()
    else:
        input_file = sys.argv[1]

        # Read in the file
        with open(os.path.join(os.getcwd(), input_file), 'r') as file:
            raw_text = file.read()
        file.close()

        # Call method to preprocess text
        tokens, nouns = preprocess_text(raw_text)

        # Call method to make dictionary
        fifty_sorted_nouns = make_dictionary(tokens, nouns)

        # Call method to make/play word guessing game
        starting_points = 5
        guessing_game(fifty_sorted_nouns, starting_points)
