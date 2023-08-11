import random
from nltk.util import ngrams
from collections import Counter

with open(input(), 'r', encoding='utf-8') as file:
    bigrams_list = list(ngrams(file.read().split(), 3))
    bigrams_dict_raw = dict(Counter(bigrams_list))

bigrams_dict_organized = {}
for x in bigrams_dict_raw:
    if f'{x[0]} {x[1]}' in bigrams_dict_organized:
        bigrams_dict_organized.get(f'{x[0]} {x[1]}').update({x[2]: bigrams_dict_raw.get(x)})
        continue
    bigrams_dict_organized.update({f'{x[0]} {x[1]}': {x[2]: bigrams_dict_raw.get(x)}})
for key in bigrams_dict_organized:
    bigrams_dict_organized[key] = dict(
        sorted(bigrams_dict_organized[key].items(), key=lambda item: item[1], reverse=True))


# print(bigrams_dict_organized)
def generate_chain():
    first_word_options = [
        word for word in bigrams_dict_organized.keys() if not any(char in word for char in '?.!') and word[0].isupper()]
    chain = [random.choice(first_word_options)]
    current_iteration = 0

    while True:
        current_word = chain[-1]
        if current_iteration > 0:
            next_word_options = bigrams_dict_organized.get(f'{chain[-2].split()[-1]} {current_word}')
        else:
            next_word_options = bigrams_dict_organized.get(current_word)
        next_word = random.choices(list(next_word_options.keys()), weights=list(next_word_options.values()), k=1)[0]
        chain.append(next_word)
        if current_iteration > 1 and next_word[-1] in [".", "?", "!"]:
            break
        current_iteration += 1

    return chain


chain_length = 10

for _ in range(chain_length):
    print(" ".join(generate_chain()))
