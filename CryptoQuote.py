#! /usr/bin/python3
# Happy B-Day Mom!
import string
import random
from urllib.request import urlopen
import os.path
from pprint import pprint

# create an alphabet list
alpha = list(string.ascii_uppercase)
# shuffle the alphabet list
random.shuffle(alpha)
# create an empty dictionary
encrypt = {}
decrypt = {}

for index, letter in enumerate(alpha):
    encrypt[letter] = alpha[index-1]
    decrypt[alpha[index-1]] = letter

cipher = open('cipher.html', 'w')
cipher.write("""
<html>
<head>
<link rel="stylesheet" href="styles.css">
<title>eCryptoQuiz</title>
</head>
<body>
    <h2>
        Ciphertext <=> Plaintext
    </h2>
<div class="columnsClass">
""")
for key, value in sorted(decrypt.items()):
    cipher.write(f'{key}  <=>  {value}<br/>') # the cipher
cipher.write('</div></body></html>')
cipher.close()

if os.path.exists('text.txt'):
    print("getting quote from text.txt")
    text = open('text.txt')
    plaintext = str.upper(text.read()) # the text
    text.close()
else:
    print("...getting a quote from the web...")
    badquote = True
    while badquote:
        quotepage = random.randint(1, 5276)
        with urlopen(f'http://www.quotationspage.com/quote/{quotepage}.html') as response:
            html = str(response.read())
            quote = html.split('<dt>')[1].split('</dt>')[0].replace('<br>', '\n')
            if quote != "ERROR: No such quotation number.":
                badquote = False

    author = html.split('"author"')[1].split('</a>')[0].split('>')[-1].replace("Search for", "")
    if author == "\n":
        author = "*** :( ***"

    answer = open('answer.html', 'w')
    answer.write("The following quote was retrieved from: ")
    answer.write(f'<a href="http://www.quotationspage.com/quote/{quotepage}.html">www.quotationspage.com</a>')
    plaintext = str.upper(f'<br/>{quote} - {author}')
    answer.write(plaintext)
    answer.close()

ciphertext = open('ciphertext.html', 'w')
for letter in range(len(plaintext)):
    if plaintext[letter] in encrypt:
        ciphertext.write(encrypt[plaintext[letter]]) # the ciphertext
    elif plaintext[letter] == '\\': ciphertext.write('')
    else: ciphertext.write(plaintext[letter]) # the punct/space
ciphertext.close()
