import json
import re
from word_part_of_speech import get_part_of_speech, contains_date_or_time
import math


# array cu toate cuvintele irelevante pentru text ( sursa: https://github.com/stopwords-iso/stopwords-ro )
# in aceast array sunt incluse si pronumele si adverbele pentru a nu fi considerate de clasificatorul de cuvinte ca fiind nume de persoane
with open("./stopwordsro.json") as json_file:
    stopwords = json.load(json_file)


# functie pentru a calcula frecventa cuvintelor
def word_counter(text):
    words = re.findall(r'\w+', text)
    words_frequency = {}

    for word in words:
        wordLr = word.lower()
        if words_frequency.keys().__contains__(word):
            words_frequency[wordLr] += 1
        else:
            words_frequency[wordLr] = 1

    return words_frequency


# functia euristica
def heuristic(sentences, word_frequency):
    result = []

    for sentenceIterator, sentence in enumerate(sentences):
        points = 0

        words = re.findall(r'\w+', sentence)

        # in cazul in care sunt specificate date calendaristice sau ore exacte propozitia primeste prioritate
        points += contains_date_or_time(sentence)

        for i, word in enumerate(words):
            if word.isdigit():
                continue

            word = word.lower()

            if word in stopwords:  # daca cuvantul e un stopword scadem numarul de aparitii in text a cuvantului
                points -= word_frequency[word]
            else:
                part_of_speech = get_part_of_speech(word)  # verb daca e verb, name daca e nume, noun daca e substantiv sau adjectiv
                if words[i][0].isupper():
                    if part_of_speech == 'verb':  # este cel mai probabil un verb
                        points += 11
                    elif part_of_speech == 'name':  # este cel mai probabil un nume
                        points += 97
                    elif part_of_speech == 'noun' and i != 0:  # este posibil sa reprezinte o locatie
                        points += 23
                elif part_of_speech == 'verb':  # cel mai probabil un verb
                    points += 11
                elif part_of_speech == 'noun':  # cel mai probabil un substantiv sau alta parte de vorbire
                    points -= 7

        result.append([sentenceIterator, points])

    return result


def relevant_sentences(sentence_scores, percent):
    sentences_count = len(sentence_scores)

    number_of_sentences = sentences_count * percent/100  # calculam primele cate propozitii trebuie sa luam
    number_of_sentences = 1 if number_of_sentences < 1 else math.ceil(number_of_sentences)

    sentence_scores.sort(key=lambda x: x[1], reverse=True)

    result = []
    i = 0

    while len(result) < number_of_sentences:
        result.append(sentence_scores[i][0])
        i += 1

    return result
