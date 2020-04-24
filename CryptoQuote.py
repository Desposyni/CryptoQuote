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


def get_quote():
    page = 1
    quote = ""
    bad_quote = True

    while bad_quote:
        page = str(randint(1, 42500))
        with urlopen(f'http://www.quotationspage.com/quote/{page}.html') as response:
            html = str(response.read())
            quote = html.split('<dt>')[1].split('</dt>')[0].replace('<br>', '\n').replace('\\', '')
            bad_quote = True if quote == "ERROR: No such quotation number." else False

    author = html.split('"author"')[1].split('</a>')[0].split('>')[-1].replace("Search for", "")
    if author == "\n":
        author = "*** :( ***"

    return map(str.upper, [page, quote, author])


def encipher(cipher, text):
    return ''.join([cipher[c] if c in cipher else c for c in text if c not in '\\'])


def main():
    cipher = get_cipher()
    page, quote, author = get_quote()

    for k, v in sorted(cipher.items()):
        print(f'{k}:{v}', end='')
        print(' , ', end='') if k not in ['M', 'Z'] else print('\n')

    print(f'http://www.quotationspage.com/quote/{page}.html')
    print(f'{quote}')
    print(f'{author:>{len(quote)}}')
    print(f'{encipher(cipher, quote)}')
    print(f'{encipher(cipher, author):>{len(quote)}}')


if __name__ == '__main__':
    main()
