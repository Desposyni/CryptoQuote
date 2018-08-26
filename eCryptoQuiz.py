#! /usr/bin/python3
# Happy B-Day Mom!
import string
import random
import urllib2
import os.path

# create an alphabet list
alpha = list(string.ascii_uppercase)
# shuffle the alphabet list
random.shuffle(alpha)
# create an empty dictionary
code = dict()

for x in range(len(alpha)):
    code[alpha[x]] = alpha[(x+1)%len(alpha)] # a shuffled alphabet dictionary

cipher = open('cipher.html', 'w')
cipher.write("""
<html>
<head>
<style>
body {
    font-family: Monaco, monospace;
    text-align: center;
    }
.columnsClass {
    column-count: 2;
    column-rule: 1px solid lightblue;
}

</style>
</head>
<body>
    <h2>
        Ciphertext <=> Plaintext
    </h2>
<div class="columnsClass">
""")
for key, value in sorted(code.items(), key=lambda (k,v): (v,k)):
    cipher.write('%s  <=>  %s<br/>' % (value, key)) # the cipher
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
        response = urllib2.urlopen('http://www.quotationspage.com/quote/%d.html' % quotepage)
        html = response.read()
        quote = html.split('<dt>')[1].split('</dt>')[0].replace('<br>', '\n')
        if quote != "ERROR: No such quotation number.":
            badquote = False

    author = html.split('"author"')[1].split('</a>')[0].split('>')[-1].replace("Search for", "")
    if author == "\n":
        author = "*** :( ***"

    answer = open('answer.html', 'w')
    answer.write("The following quote was retrieved from:\n")
    answer.write('http://www.quotationspage.com/quote/%d.html\n\n' % quotepage)
    plaintext = str.upper("\n\n" + quote + "\n\n\n\n- " + author)
    answer.write(plaintext)
    answer.close()

ciphertext = open('ciphertext.html', 'w')
for letter in range(len(plaintext)):
    if plaintext[letter] in code:
        ciphertext.write(code[plaintext[letter]]) # the ciphertext

    else: ciphertext.write(plaintext[letter]) # the punct/space
ciphertext.close()
