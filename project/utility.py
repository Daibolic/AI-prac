import nltk

def most_freq(file, encoding, num):
    """ file is the name of the file in string.
        It only adds the $True$ sentences to the set
        it outputs the most frequent num words
    """
    words = ""
    f = open(file, mode='r', encoding=encoding)
    line = f.readline()
    while (line != ''):
        if (line[-7:] == "$True$\n"):
            words = words + line[:-7] + " "
        line = f.readline()
    f.close()
    tokens = nltk.word_tokenize(words)
    text = nltk.Text(tokens)
    fdist = nltk.FreqDist(text)
    print(fdist.most_common(num))

def separator(file, encoding):
    """Separates the file into two files, labeled useful and not_useful
    """
    f = open(file, mode = 'r', encoding = encoding)
    useful = open('useful', 'w+', encoding='utf8')
    not_useful = open('useless', 'w+', encoding='utf8')
    line = f.readline()
    while (line != ''):
        if (line[-7:] == "$True$\n"):
            useful.write(line[:-7] + "\n")
        elif (line[-6:] == "$True$"):
            useful.write(line[:-6] + "\n")
        else:
            not_useful.write(line[:-8] + "\n")
        line = f.readline()
    f.close()
    useful.close()
    not_useful.close()

