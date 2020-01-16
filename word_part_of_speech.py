import urllib.request
import re
import math
from arrays import months, days


# functie peuristica pentru determina daca un cuvant este verb sau substantiv
def get_part_of_speech(word):
    word = word.lower().replace('ă', 'a').replace('î', 'i').replace('ș', 's').replace('ț', 't').replace('â', 'a')

    # luam continutul html al paginii
    try:
        with urllib.request.urlopen("https://dexonline.ro/definitie/" + word) as response:
            html = response.read().decode("utf-8")
    except:
        return 'noun'

    # numaram tagurile pentru verbe si substantive
    verbs = sum(1 for m in re.finditer('<abbr class="abbrev" data-html="true" title="verb">vb.</abbr>', html))
    nouns = sum(1 for m in re.finditer('<abbr class="abbrev" data-html="true" title="substantiv neutru">(s. n.)|(sn)</abbr>', html))
    adjs = sum(1 for m in re.finditer('<abbr class="abbrev" data-html="true" title="adjectiv">adj.</abbr>', html))

    # verificam daca primul tag e substantiv, adjectiv sau verb
    posVerb = re.search('<abbr class="abbrev" data-html="true" title="verb">vb.</abbr>', html)
    posVerb = math.inf if posVerb is None else posVerb.start()

    posNoun = re.search('<abbr class="abbrev" data-html="true" title="substantiv neutru">(s. n.)|(sn)</abbr>', html)
    posNoun = math.inf if posNoun is None else posNoun.start()

    posAdj = re.search('<abbr class="abbrev" data-html="true" title="adjectiv">adj.</abbr>', html)
    posAdj = math.inf if posAdj is None else posAdj.start()

    if posVerb < posNoun and posVerb < posAdj:
        value = 'v'
    elif posNoun < posVerb and posNoun < posAdj:
        value = 'n'
    elif posAdj < posNoun and posAdj < posVerb:
        value = 'a'
    else:  # daca nu gaseste nici-un adjectiv, substantiv sau verb dar gaseste pagina, probabilitatea este foarte mare sa fie un nume
        value = 'name'

    # calculam un punctaj care va fi pozitiv pentru verb si negativ pentru substantiv
    result = 0

    # primul tag primeste 30 de puncte
    if value == 'v':
        result += 30
        verbs -= 1
    else:
        result -= 30
        nouns -= 1

    # celelalte tag-uri primesc cate +/- 10 puncte
    result += verbs*10 - nouns*10 - adjs*20

    return 'name' if value == 'name' else 'noun' if result <= 0 else 'verb'


def contains_date_or_time(sentence):
    points = 0

    # pentru fiecare zi a saptamanii sau luna a anului adaug 5 puncte
    points += sum([10 for day in days if re.search(day, sentence)])

    points += sum([10 for month in months if re.search(month, sentence)])

    # in cazul in care avem o data exacta ii acordam un punctaj mai mare deoarece este mai importanta
    points += 50 if re.search(r"\d{1,2}(\.|-|\/)\d{1,2}(\.|-|\/)('?\d{2}|\d{4})", sentence) else 0

    # in cazul in care avem o ora exacta ii acordam un punctaj semnificativ
    points += 20 if re.search(r"\d{1,2}:\d{1,2}( ?AM| ?PM)?", sentence) else 0

    return points

