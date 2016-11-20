import nltk
import feature_extractor, phrase_extractor, random

def most_freq(file_name,num):
    """ file is the name of the file in string.
        It only adds the $True$ sentences to the set
        it outputs the most frequent num words
    """
    words = ""
    f = open(file_name, mode='r')
    line = f.readline()
    while (line != ''):
        if (line[-7:] == "$True$\n"):
            words = words + line[:-7] + " "
        line = f.readline()
    f.close()
    tokens = nltk.word_tokenize(words)
    text = nltk.Text(tokens)
    fdist = nltk.FreqDist(text)
    print fdist.most_common(num)

def separator(file_name):
    """Separates the file into two files, labeled useful and not_useful
    """
    f = open(file_name, mode = 'r')
    useful = open('useful', 'w+',)
    line = f.readline()
    while (line != ''):
        if (line[-7:] == "$True$\n"):
            useful.write(line[:-7] + "\n")
        elif (line[-6:] == "$True$"):
            useful.write(line[:-6] + "\n")            
        line = f.readline()
    f.close()
    useful.close()

def generate_help_file():
    """ Generates a help file for identifying patterns in phrase extraction
    """
    skills = open('skills', 'w+')
    personal = open('personal', 'w+')
    labeled_set = generate_cat_labeled_set('./useful_cat_train')
    for (line, label) in labeled_set:
        if (label == "skills"):
            tagged = nltk.pos_tag(nltk.word_tokenize(line))
            (words,  tags) = phrase_extractor.split_tag(tagged)
            skills.write(" ".join(words) + '\n')
            skills.write(" ".join(tags) + '\n')
        else:
            tagged = nltk.pos_tag(nltk.word_tokenize(line))
            (words, tags) = phrase_extractor.split_tag(tagged)
            personal.write(' '.join(words) + '\n')
            personal.write(' '.join(tags) + '\n')
    skills.close()
    personal.close()

def generate_usefulness_labeled_set(file_name):
    """ Given a file name that contains sentences marked using the $True$ / $False
        notation, geneate a labeled set
    """
    f = open(file_name, mode = 'r')
    labeled_sen = []
    line = f.readline()
    while (line != ''):
        if (line[-7:] == "$True$\n"):
            labeled_sen.append((line[:-7], "useful"))
        elif (line[-6:] == "$True$"):
            labeled_sen.append((line[:-6], "useful"))
        elif (line[-7:] == "$False$"):
            labeled_sen.append((line[:-7], "useless"))
        else:
            labeled_sen.append((line[:-8], "useless"))
        line = f.readline()
    f.close()
    return labeled_sen

def generate_cat_labeled_set(file_name):
    """ Given a file name that contains labeled useful sentences (either with $skill$ tag or not)
        generate a labeled set
    """
    f = open(file_name, mode = 'r')
    labeled_sen = []
    line = f.readline()
    while (line != ''):
        if (line[-8:] == "$skill$\n"):
            labeled_sen.append((line[:-8], "skills"))
        elif (line[-7:] == "$skill$"):
            labeled_sen.append((line[:-7], "skills"))
        else:
            labeled_sen.append((line, "personal"))
        line = f.readline()
    f.close()
    return labeled_sen

def train_usefulness_classifier():
    labeled_set = generate_usefulness_labeled_set('../sentence_usefulness.txt')
    random.shuffle(labeled_set)
    div = len(labeled_set) // 2
    train_set = nltk.classify.apply_features(feature_extractor.sentence_features, labeled_set[div:])
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    return classifier

def train_cat_classifier():
    labeled_set = generate_cat_labeled_set('useful_cat_train')
    random.shuffle(labeled_set)
    div = len(labeled_set) // 2
    train_set = nltk.classify.apply_features(feature_extractor.cat_features, labeled_set[div:])
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    return classifier

def print_usefulness_accuracy():
    labeled_set = generate_usefulness_labeled_set('../sentence_usefulness.txt')
    random.shuffle(labeled_set)
    div = len(labeled_set) // 2
    train_set = nltk.classify.apply_features(feature_extractor.sentence_features, labeled_set[div:])
    test_set = nltk.classify.apply_features(feature_extractor.sentence_features, labeled_set[:div])
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print nltk.classify.accuracy(classifier, test_set)

def print_cat_accuracy():
    labeled_set = generate_cat_labeled_set('useful_cat_train')
    random.shuffle(labeled_set)
    div = len(labeled_set) // 2
    train_set = nltk.classify.apply_features(feature_extractor.cat_features, labeled_set[div:])
    test_set = nltk.classify.apply_features(feature_extractor.cat_features, labeled_set[:div])
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print nltk.classify.accuracy(classifier, test_set)