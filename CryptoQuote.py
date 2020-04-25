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
    page = str(page)
    error = "ERROR: No such quotation number."
    quote = str(error)
    while quote == error:
        with urlopen(f'http://www.quotationspage.com/quote/{page}.html') as response:
            html = response.read().decode('utf-8', errors='replace')
            quote = html.split('<dt>')[1].split('</dt>')[0].replace('<br>', '')
        if quote == error:
            page = str(randint(1, 42500))
        if len(quote) > 586:  # check if quote is too long to fit on 80x24 console
            quote = str(error)
            page = str(randint(1, 42500))

    author = html.split('"author"')[1]
    author = author.split('<b>')[1].split('</b>')[0]
    author = author.split('</a>')[0].split('>')[-1]

    return map(str.upper, (page, quote, author))


def encipher(cipher, text):
    return ''.join([cipher[c] if c in cipher else c for c in text])


def main():
    cipher = get_cipher()
    page, quote, author = get_quote(34949)

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
