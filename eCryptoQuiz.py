#! usr/bin/python2.7
# Happy B-Day Mom!
import random
import urllib2
import os.path

# a list of the alphabet
alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
         'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
key = list(alpha)

badshuffle = True # starts with a bad shuffle
while badshuffle:
    random.shuffle(key) # shuffles
    for x in range(len(alpha)):
        if key[x] != alpha[x]: # if they're different
            badshuffle = False
        else: # if a letter got mapped to itself
            badshuffle = True
            break # exits for-loop, enters while-loop again, so it can reshuffle

code = dict()
for x in range(len(alpha)):
    code[alpha[x]] = key[x] # a shuffled alphabet dictionary

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
        response = urllib2.urlopen('http://www.quotationspage.com/quote/%d.html' % quotepage)
        html = response.read()
        quote = html.split('<dt>')[1].split('</dt>')[0].replace('<br>', '\n')
        if quote != "ERROR: No such quotation number.":
            badquote = False
            
    author = html.split('"author"')[1].split('</a>')[0].split('>')[-1].replace("Search for", "")
    if author == "\n":
        author = "*** :( ***"

    answer = open('answer.txt', 'w')
    answer.write("The following quote was retrieved from:\n")
    answer.write('http://www.quotationspage.com/quote/%d.html\n\n' % quotepage)
    answer.write(quote + "\n" + author)
    answer.close()
    text = (quote + "\n" + author)
    plaintext = str.upper(text) # the text

cipher = open('cipher.txt', 'w')
cipher.write(str(code).replace(',', '\n')) # the cipher
cipher.close()

ciphertext = open('ciphertext.txt', 'w')
for letter in range(len(plaintext)):
    if plaintext[letter] in code:
        ciphertext.write(code[plaintext[letter]]) # the ciphertext

    else: ciphertext.write(plaintext[letter]) # the punct/space
ciphertext.close()
