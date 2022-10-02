import codecs
import pickle
from nltk import word_tokenize, ngrams


def create_unigrams_and_bigrams(input_file):
    """
    Creates a list of unigrams and bigrams from the input file specified.
    Also, this method creates a dictionary of unigrams and bigrams with
    the counts for each respective unigram/bigram.
    :param input_file: The relative path of the input file for each language
    (i.e., English, French, and Italian)
    :return unigram_dictionary, bigram_dictionary: The dictionaries that hold the unigrams/bigrams
    and their counts
    """

    # Read in the file
    if input_file == "LangId.train.English":
        with open(input_file, 'r') as file:
            text = file.read()
        file.close()
    elif input_file == "LangId.train.French" or "LangId.train.Italian":
        with codecs.open(input_file, 'r', encoding = 'utf-8') as file:
            text = file.read()
        file.close()

    # Remove newlines from text and tokenize the text
    text = text.replace("\n", "")
    tokens = word_tokenize(text)

    # Make a unigrams and bigrams list
    unigrams = tokens
    bigrams = list(ngrams(unigrams, 2))

    # Create dictionary of counts for the unigrams and bigrams list
    unigram_dictionary = {token:unigrams.count(token) for token in set(unigrams)}
    bigram_dictionary = {bigram:bigrams.count(bigram) for bigram in set(bigrams)}

    # Return the dictionaries
    return unigram_dictionary, bigram_dictionary


def pickle_dicts(unigram_dict, bigram_dict, unigram_filename, bigram_filename):
    """
    Pickles the unigram and bigram dictionaries
    :param unigram_dict: The unigram dictionary of the specified language
    :param bigram_dict: The bigram dictionary of the specified langauge
    :param unigram_filename: The filename that'll be used when pickling the unigram dictionary
    :param bigram_filename: The filename that'll be used when pickling the bigram dictionary
    :return: N/A
    """

    # Pickle the unigram dict
    with open(unigram_filename, 'wb') as handle:
        pickle.dump(unigram_dict, handle)

    # Pickle the bigram dict
    with open(bigram_filename, 'wb') as handle:
        pickle.dump(bigram_dict, handle)


if __name__ == "__main__":
    # Build the unigram and bigram dictionary for each langauge.
    # After getting the dictionaries for a language, pickle them.
    unigram_dict, bigram_dict = create_unigrams_and_bigrams("LangId.train.English")
    pickle_dicts(unigram_dict, bigram_dict, "English_unigram.p", "English_bigram.p")

    unigram_dict, bigram_dict = create_unigrams_and_bigrams("LangId.train.French")
    pickle_dicts(unigram_dict, bigram_dict, "French_unigram.p", "French_bigram.p")

    unigram_dict, bigram_dict = create_unigrams_and_bigrams("LangId.train.Italian")
    pickle_dicts(unigram_dict, bigram_dict, "Italian_unigram.p", "Italian_bigram.p")
