import fileinput
import os, sys, string

fileobject = open('one-indexed-files.txt', 'rt')
fout = open("modified.txt", "wt")
for line in fileobject:
    word = line.split(" ")
    fout.write(word[0])
    if("1\n" in word[1]):
        fout.write(' glass\n')
    elif("2\n" in word[1]):
        fout.write(' paper\n')
    elif("3\n" in word[1]):
        fout.write(' cardboard\n')
    elif('4\n' in word[1]):
        fout.write(' plastic\n')
    elif('5\n' in word[1]):
        fout.write(' metal\n')
    elif('6\n' in word[1]):
        fout.write(' trash\n')
    
fileobject.close()
fout.close()       