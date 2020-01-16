from information import text, percent
import nltk
import lib
from termcolor import colored

# impartim textul in propozitii
print("Tokenize...")
sentences = nltk.tokenize.sent_tokenize(text)

# calculam frecventa cuvintelor
print("Word frequency...")
word_frequency = lib.word_counter(text)

# calculam punctajele pentru fiecare propozitie
print("Heuristic running...")
sentences_points = lib.heuristic(sentences, word_frequency)

# array cu indexii propozitiilor relevante
print("Selecting sentences...")
relevant_indexes = lib.relevant_sentences(sentences_points, percent)

[print(colored(s, 'green')) if i in relevant_indexes else print(s) for i, s in enumerate(sentences)]
