#! /usr/bin/python
# Happy B-Day Mom!
import string
import random
import urllib2
import os.path

# a list of the alphabet
alpha = list(string.ascii_uppercase)
random.shuffle(alpha)
code = dict()
for x in range(len(alpha)):
    code[alpha[x]] = alpha[(x+1)%len(alpha)] # a shuffled alphabet dictionary

cipher = open('cipher.html', 'w')
cipher.write("""
<html>
<head>
<style>
table, th, td {
    border: 1px solid black;
    text-align: center;
}
table {
    margin: auto;
}
td {
    padding-left, padding-right: 2px;
}
h2 {
    text-align: center;
}
tr:nth-child(even) {background-color: #f2f2f2}
</style>
</head>
<body>
    <h2>
        Left column is ciphertext; <br/>right column is plaintext.
    </h2>
<table>
""")
for key, value in sorted(code.items(), key=lambda (k,v): (v,k)):
    cipher.write('<tr><td>%s  <=>  %s<br/></td>' % (value, key)) # the cipher
cipher.write('</tr></table></body></html>')
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
