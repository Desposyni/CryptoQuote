#! /usr/local/bin/python3
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
            html = str(response.read())

            iso_to_utf = {'\\x92': "'", '\\x97': '-', '\\x91': "'"}
            for iso, utf in iso_to_utf.items():
                html = html.replace(iso, utf)
            html = bytes(html, 'iso8859-1').decode('utf-8', errors='replace')

            quote = html.split('<dt>')[1].split('</dt>')[0]
            bad_chars = ('<br>', '\\')
            for char in bad_chars:
                quote = quote.replace(char, '')

        if quote == error:
            page = str(randint(1, 42500))
        if len(quote) > 500:  # check if quote is too long
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
    print(f'{author:>{len(quote) if len(quote) < 70 else 70}}')
    print()
    word_wrap(encipher(cipher, quote))
    print(f'{encipher(cipher, author):>{len(quote) if len(quote) < 70 else 70}}')


if __name__ == '__main__':
    main()
