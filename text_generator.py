import random
from nltk.util import ngrams
from collections import Counter

with open(input(), 'r', encoding='utf-8') as file:
    trigrams_list = list(ngrams(file.read().split(), 3))
    trigrams_dict_raw = dict(Counter(trigrams_list))

trigrams_dict_organized = {}
for x in trigrams_dict_raw:
    if f'{x[0]} {x[1]}' in trigrams_dict_organized:
        trigrams_dict_organized.get(f'{x[0]} {x[1]}').update({x[2]: trigrams_dict_raw.get(x)})
        continue
    trigrams_dict_organized.update({f'{x[0]} {x[1]}': {x[2]: trigrams_dict_raw.get(x)}})
for key in trigrams_dict_organized:
    trigrams_dict_organized[key] = dict(
        sorted(trigrams_dict_organized[key].items(), key=lambda item: item[1], reverse=True))


def generate_chain():
    first_word_options = [
        word for word in trigrams_dict_organized.keys() if not any(char in word for char in '?.!') and word[0].isupper()]
    chain = [random.choice(first_word_options)]
    current_iteration = 0

    while True:
        current_word = chain[-1]
        if current_iteration > 0:
            next_word_options = trigrams_dict_organized.get(f'{chain[-2].split()[-1]} {current_word}')
        else:
            next_word_options = trigrams_dict_organized.get(current_word)
        next_word = random.choices(list(next_word_options.keys()), weights=list(next_word_options.values()), k=1)[0]
        chain.append(next_word)
        if current_iteration > 1 and next_word[-1] in [".", "?", "!"]:
            break
        current_iteration += 1

    return chain


chain_length = 10

for _ in range(chain_length):
    print(" ".join(generate_chain()))
