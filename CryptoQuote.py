#! /usr/bin/python3
# Happy B-Day Mom!
from string import ascii_uppercase
from random import shuffle, randint
from urllib.request import urlopen


def get_cipher():
    alpha = list(ascii_uppercase)
    shuffle(alpha)  # shuffle the alphabet list
    encrypt = {}  # create empty dicts to hold ciphers

    for index, character in enumerate(alpha):
        encrypt[character] = alpha[index - 1]

    return encrypt


def get_quote():
    quote_page = 1
    quote = ""
    bad_quote = True

    while bad_quote:
        quote_page = str(randint(1, 5276))
        with urlopen(f'http://www.quotationspage.com/quote/{quote_page}.html') as response:
            html = str(response.read())
            quote = html.split('<dt>')[1].split('</dt>')[0].replace('<br>', '\n')
            if quote != "ERROR: No such quotation number.":
                bad_quote = False

    author = html.split('"author"')[1].split('</a>')[0].split('>')[-1].replace("Search for", "")
    if author == "\n":
        author = "*** :( ***"

    return map(str.upper, [quote_page, quote, author])


class CryptoQuote:

    def __init__(self):
        self.encrypt = get_cipher()
        self.quote_page, self.quote, self.author = get_quote()

    def encipher(self, text):
        return ''.join([self.encrypt[c] if c in self.encrypt else c for c in text if c != '\\'])


def main():
    q = CryptoQuote()

    print('Cipher')
    for e, d in sorted(q.encrypt.items()):
        print(f'{e} <=> {d}')

    print(f'Quote Page = {q.quote_page}')
    print(f'{q.quote} - {q.author}')
    print(f'{q.encipher(q.quote)} - {q.encipher(q.author)}')


if __name__ == '__main__':
    main()
