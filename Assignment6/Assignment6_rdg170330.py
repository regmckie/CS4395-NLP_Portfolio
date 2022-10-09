import re
import requests
import pickle
from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.corpus import stopwords


def web_crawler(starting_url):
    """
    Crawls through several URLs from starting URL; will stop when we get
    15 relevant URLs.
    :param starting_url: the URL we start with (i.e., Wikipedia page of 'The Nightmare Before Christmas')
    :return: a list of URLs that we've visited (i.e., our 15 relevant URLs)
    """

    # Do some setting up by creating the BeautifulSoup object
    # we'll use in order to parse the web pages
    r = requests.get(starting_url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

    urls_visited = []

    # Get the links from the starting url
    web_links = soup.find_all('a')

    with open('urls.txt', 'w') as file:
        for link in web_links:
            # Break out of loop when we've gotten 15 relevant URLs
            if len(urls_visited) == 15:
                break

            link_string = str(link.get('href'))

            # Filters out the relevant URLs we want to keep
            if 'nightmare' in link_string or 'Nightmare' in link_string:
                if link_string.startswith('http') and 'cia' not in link_string \
                        and 'bbfc' not in link_string and 'web.archive.org' not in link_string \
                        and '4029tv' not in link_string and 'themarysue' not in link_string \
                        and 'movies.about.com' not in link_string and 'page=releases' not in link_string \
                        and 'rollingstone' not in link_string and 'books.google.com' not in link_string \
                        and 'xbox' not in link_string and '/guides/' not in link_string \
                        and 'syfy' not in link_string and 'moviehole' not in link_string:

                    # Write out relevant URLs to file and append to list
                    file.write(link_string + '\n')
                    urls_visited.append(link_string)
    file.close()

    return urls_visited


def check_if_visible(element):
    """
    Checks to see if an element is visible
    :param element:  element from the HTML code
    :return: True or False value depending on if the element is visible
    """

    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


def scrape_text(urls_visited):
    """
    Scrape the text from a webpage we visited via the URL, then
    write out the text to a file called "textfileX," where "X"
    is a number between 1-15 representing one of the URLs.
    :param urls_visited: A list of our 15 relevant URLs
    :return: N/A
    """

    counter = 0

    for url in urls_visited:
        # Increment counter for each text file
        counter += 1

        # Scrape text from URLs
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0', 'User-Agent': 'My User Agent 1.0'})
        html = urlopen(req, timeout=10)
        soup = BeautifulSoup(html, features='html.parser')
        data = soup.findAll(text=True)
        result = filter(check_if_visible, data)
        temp_list = list(result)
        text = ' '.join(temp_list)

        # Write text out to file
        with open(('textfile{}'.format(counter)), 'w', encoding='utf-8') as file:
            file.write(text)
        file.close()


def clean_up_file():
    """
    Cleans up the text files and rewrites the new text into a new file.
    This new file is called "reformatted_textfileX," where "X" is a
    number between 1-15 representing one of the files.
    :return: N/A
    """

    for counter in range(1, 16):
        # Read text files
        with open("textfile{}".format(counter), 'r', encoding='utf-8') as file:
            text = file.read()
        file.close()

        # Remove newlines and tabs from text
        text = ' '.join(text.split())

        # Write cleaned-up text to new files
        with open("reformatted_textfile{}".format(counter), 'w', encoding='utf-8') as file:
            file.write(text)
        file.close()


def find_important_terms():
    """
    Finds the top 40 terms from all 15 pages combined.
    :return my_10_terms: The 10 terms I chose from the 40 that were outputted
    """

    # Put all the text in each of the 15 files into one big file
    with open('all_text_reformatted.txt', 'w', encoding='utf-8') as file:
        for counter in range(1, 16):
            with open("reformatted_textfile{}".format(counter), 'r', encoding='utf-8') as f:
                text = f.read()
            f.close()
            file.write(text)    # Write text of all 15 file into the one big file
    file.close()

    # Lowercase text, remove stopwords, and punctuation
    with open('all_text_reformatted.txt', 'r', encoding='utf-8') as file:
        raw_text = file.read()
    file.close()

    all_text = word_tokenize(raw_text)
    tokens_from_all_text = [token.lower() for token in all_text]
    tokens_from_all_text = [token for token in tokens_from_all_text if token.isalpha() and
                            token not in stopwords.words('english')]

    # Write new text out to a new file
    with open('all_text_tokenized.txt', 'w', encoding='utf-8') as file:
        file.write(str(tokens_from_all_text))
    file.close()

    # Make unigrams list from text and dictionary to hold the count for each unigram
    with open('all_text_tokenized.txt', 'r') as file:
        raw_text = file.read()
    file.close()

    tokens_from_all_text = word_tokenize(raw_text)
    unigrams = tokens_from_all_text
    unigram_dict = {token:unigrams.count(token) for token in set(unigrams)}

    # Sort the dictionary and print out top 40 most common terms
    sorted_unigrams = sorted(unigram_dict.items(), key=lambda x: x[1], reverse=True)

    print("\nTop 40 most common terms in all 15 pages:")
    for counter in range(2, 42):
        print("{}.".format(counter - 1), sorted_unigrams[counter])

    # Pick 10 terms from the 40
    my_10_terms = ["film", "Disney", "Burton", "Jack", "Selick",
                    "Halloween", "holiday", "story", "Elfman", "animation"]

    return my_10_terms


def build_knowledge_base(my_10_terms):
    """
    Builds a knowledge base using the top 10 terms I hand-selected.
    This knowledge base will be a simple dictionary where the (key: value) pairs
    will be (term: sentences from 15 pages that include that term).
    :param my_10_terms: A list of the 10 terms I hand-selected.
    :return: N/A
    """
    
    # Open file with all text
    with open('all_text_reformatted.txt', 'r', encoding='utf-8') as file:
        raw_text = file.read()
    file.close()

    # Extract sentence from the text
    sentences = sent_tokenize(raw_text)

    # Create list to hold sentences that have the 10 terms
    # and a dictionary where they (key, value) pair is
    # (term, list of sentences that include that term)
    sentences_with_terms = []
    my_10_terms_dict = {"film": [], "Disney": [], "Burton": [], "Jack": [], "Selick": [],
                        "Halloween": [], "holiday": [], "story": [], "Elfman": [], "animation": []}

    # Iterate through the terms in the list and determine
    # if a sentence from all 15 pages has that term. If it does,
    # then add it to a list. Add that list into the dictionary.
    for term in my_10_terms:
        for sent in sentences:
            if term in sent:
                sentences_with_terms.append(sent)
        temp = sentences_with_terms
        my_10_terms_dict[term] += temp
        sentences_with_terms.clear()    # Clear the list for the next term

    # Pickle dictionary and read in the pickle file
    pickle.dump(my_10_terms_dict, open('my_10_terms_dict.p', 'wb'))
    my_10_terms_knowledge_base = pickle.load(open('my_10_terms_dict.p', 'rb'))

    # Write out the knowledge base (the dict) to a file
    with open('knowledge_base', 'w', encoding='utf-8') as file:
        for key, value in my_10_terms_knowledge_base.items():
            file.write(key)
            file.write(": ")
            file.write(str(value))
            file.write("\n")
    file.close()


if __name__ == "__main__":

    starting_url = "https://en.wikipedia.org/wiki/The_Nightmare_Before_Christmas"

    # Crawl through URLs and get 15 relevant URLs
    urls_visited = web_crawler(starting_url)

    # Scrape text from each URL
    scrape_text(urls_visited)

    # Clean up text in files
    clean_up_file()

    # Find the 40 most important terms from the pages
    my_10_terms = find_important_terms()

    # Build knowledge base using 10 words chosen from previous 40
    build_knowledge_base(my_10_terms)