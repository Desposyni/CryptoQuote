#! /usr/bin/python3
# Happy B-Day Mom!
from string import ascii_uppercase
from random import shuffle, randint
from urllib.request import urlopen


def get_cipher():
    alpha = list(ascii_uppercase)
    shuffle(alpha)  # shuffle the alphabet list
    cipher = {}  # create empty dict to hold cipher

    for i, c in enumerate(alpha):
        cipher[c] = alpha[i - 1]

    return cipher


def get_quote(page=0):
    quote = ''
    error = "ERROR: No such quotation number."
    while quote in error:
        page = str(randint(1, 42500)) if quote in error or page == 0 else str(page)
        with urlopen(f'http://www.quotationspage.com/quote/{page}.html') as response:
            html = response.read().decode('utf-8')
            quote = html.split('<dt>')[1].split('</dt>')[0].replace('<br>', '\n').replace('\\', '')

    author = html.split('"author"')[1].split('</a>')[0].split('>')[-1].replace("Search for", "")
    if author == "\n":
        author = "*** :( ***"

    return map(str.upper, (page, quote, author))


def encipher(cipher, text):
    return ''.join([cipher[c] if c in cipher else c for c in text])


def main():
    cipher = get_cipher()
    page, quote, author = get_quote()

    def word_wrap(text, wrap=80):
        words = []
        for word in text.split():
            if len(' '.join(words)) + len(word) < wrap:
                words.append(word)
            else:
                print(' '.join(words))
                words = [word]
        else:
            print(' '.join(words))

    for k, v in sorted(cipher.items()):
        print(f'{k}:{v}', end='')
        print(' , ', end='') if k not in ['M', 'Z'] else print()

    print(f'http://www.quotationspage.com/quote/{page}.html')

    word_wrap(quote)
    print(f'{author:>{len(quote) if len(quote) < 80 else 80}}')
    print()
    word_wrap(encipher(cipher, quote))
    print(f'{encipher(cipher, author):>{len(quote) if len(quote) < 80 else 80}}')


if __name__ == '__main__':
    main()
