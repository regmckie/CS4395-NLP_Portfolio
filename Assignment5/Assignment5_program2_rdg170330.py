import pickle
import math
import codecs
from nltk import word_tokenize, ngrams


def unpack_dicts(unigram_dict, bigram_dict):
    """
    Unpacks the unigram and bigram dictionaries
    :param unigram_dict: The unigram dictionary of the specified language (i.e., English, French, or Italian)
    :param bigram_dict: The bigram dictionary of the specified language (i.e., English, French, or Italian)
    :return unigram_dictionary, bigram_dictionary: The unpacked unigram and bigram dictionaries
    """

    # Unpack the unigram dictionary
    with open(unigram_dict, 'rb') as handle:
        unigram_dictionary = pickle.load(handle)

    # Unpack the bigram dictionary
    with open(bigram_dict, 'rb') as handle:
        bigram_dictionary = pickle.load(handle)

    return unigram_dictionary, bigram_dictionary


def calculate_probabilities(text, unigram_dict, bigram_dict, no_of_tokens, vocab_size):
    """
    Calculates the probability that a line from the text, LangId.test, is either
    English, French, or Italian
    :param text: A line from the file, LangId.test
    :param unigram_dict: the unigram dictionary of the specified language
    :param bigram_dict: the bigram dictionary of the specified language
    :param no_of_tokens: the number of tokens of the specified language
    :param vocab_size: the number of unique tokens of the specified language
    :return prob_laplace: the probability (using laplace smoothing) that the text is either
    English, French, or Italian
    """

    # Make some unigrams and bigrams
    unigrams_line = word_tokenize(text)
    bigrams_line = list(ngrams(unigrams_line, 2))

    # prob_laplace is the probability with laplace smoothing
    # prob_gt is the probability with Good-Turing smoothing
    prob_laplace = 1
    prob_gt = 1

    # Calculate the probability using laplace smoothing
    for bigram in bigrams_line:
        b = bigram_dict[bigram] if bigram in bigram_dict else 0
        b_gt = bigram_dict[bigram] if bigram in bigram_dict else 1 / no_of_tokens
        u = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        if u == 0:
            prob_gt = prob_gt * (1 / no_of_tokens)
        else:
            prob_gt = prob_gt * (b_gt / u)
        prob_laplace = prob_laplace * ((b + 1) / (u + vocab_size))

    # Return the probability
    return prob_laplace


if __name__ == "__main__":
    # Unpack the dictionaries
    English_unigram_dict, English_bigram_dict = unpack_dicts("English_unigram.p", "English_bigram.p")
    French_unigram_dict, French_bigram_dict = unpack_dicts("French_unigram.p", "French_bigram.p")
    Italian_unigram_dict, Italian_bigram_dict = unpack_dicts("Italian_unigram.p", "Italian_bigram.p")

    # Read in the training files
    with open("LangId.train.English", "r") as file:
        English_text = file.read()
    file.close()

    with codecs.open("LangId.train.French", "r", encoding="utf-8") as file:
        French_text = file.read()
    file.close()

    with codecs.open("LangId.train.Italian", "r", encoding="utf-8") as file:
        Italian_text = file.read()
    file.close()

    # Get the number of tokens in each language and the vocab size
    E_unigrams = word_tokenize(English_text)
    F_unigrams = word_tokenize(French_text)
    I_unigrams = word_tokenize(Italian_text)

    E_unigram_dict = {t: E_unigrams.count(t) for t in set(E_unigrams)}
    F_unigram_dict = {t: F_unigrams.count(t) for t in set(F_unigrams)}
    I_unigram_dict = {t: I_unigrams.count(t) for t in set(I_unigrams)}

    English_N = len(E_unigrams)
    English_V = len(E_unigram_dict)
    French_N = len(F_unigrams)
    French_V = len(F_unigram_dict)
    Italian_N = len(I_unigrams)
    Italian_V = len(I_unigram_dict)

    # Read in the test file line by line
    test_file = open('LangId.test', 'r')
    lines = test_file.readlines()
    test_file.close()

    # Calculate the probability of each language for each line
    counter = 0
    for line in lines:
        counter += 1
        English_probability = calculate_probabilities(line, English_unigram_dict,
                                                      English_bigram_dict, English_N, English_V)
        French_probability = calculate_probabilities(line, French_unigram_dict,
                                                     French_bigram_dict, French_N, French_V)
        Italian_probability = calculate_probabilities(line, Italian_unigram_dict,
                                                      Italian_bigram_dict, Italian_N, Italian_V)

        # Write out the language with the highest probability for each
        # line on the file. For example, if English had a higher probability than
        # French or Italian for line 3, then write English.
        if English_probability > French_probability and English_probability > Italian_probability:
            my_answers = open("my_answers.txt", "a")
            my_answers.write("{} English\n".format(counter))
            my_answers.close()
        elif French_probability > English_probability and French_probability > Italian_probability:
            my_answers = open("my_answers.txt", "a")
            my_answers.write("{} French\n".format(counter))
            my_answers.close()
        elif Italian_probability > English_probability and Italian_probability > French_probability:
            my_answers = open("my_answers.txt", "a")
            my_answers.write("{} Italian\n".format(counter))
            my_answers.close()
        else:
            my_answers = open("my_answers.txt", "a")
            my_answers.write("{} PROBABILITY COULD NOT BE DETERMINED\n".format(counter))
            my_answers.close()

    # Read in the answers from my_answers.txt
    my_answers_file = open('my_answers.txt', 'r')
    my_answers_lines = my_answers_file.read()
    my_answers_list = my_answers_lines.split("\n")
    my_answers_file.close()

    # Read in the solutions from LandId.sol
    solutions_file = open('LangId.sol', 'r')
    solutions_lines = solutions_file.read()
    solutions_list = solutions_lines.split("\n")
    solutions_file.close()

    # Iterate through the list and compare my answers to the solution.
    # Compare the accuracy (i.e., get the percentage of correctly classified items)
    counter = 0
    correct_answers = 0
    line_numbers_with_wrong_answer = []
    for my_answer, solution in zip(my_answers_list, solutions_list):
        counter += 1
        if my_answer == solution:
            correct_answers += 1
        elif my_answer != solution:
            line_numbers_with_wrong_answer.append(counter)

    # Calculate and display accuracy
    accuracy = (correct_answers / 300) * 100
    print("Number of correct answers: ", correct_answers, "/ 300")
    print("Accuracy: {:.2f}%".format(accuracy))
    print("Lines that were wrong: ", set(line_numbers_with_wrong_answer))
