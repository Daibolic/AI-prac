import nltk, utility
import feature_extractor as fe
import phrase_extractor as pe
import categorize as cat
import userdata as ud


metadatafile = "metadata.txt"
skillsfile = "skills.txt"

class LetterGenerator:
    'Class for the letter generator'
    usefulness_classifier = None
    cat_classifier = None
    template = "My name is [NM] and I am a [GD] student at [IN].\nI am very interested in this job posting for [PN] at [CN].\nI have experience in [SK] which makes me an appropriate candidate for this job.\n[PQ].\nI think I would do well at this position. Thank you very much!\n[NM]"
    headers = {
        "creativity": "Creativity defines who I am. ",

        "communication": "I communicated effectively under different situations. ",

        "collaboration":"Working in a team environment is something I enjoy a lot. ",

        "responsibility": "I will do everything I can to complete the tasks assigned to me. ",

        "leadership": "While I am a good follower, I also know how to lead a team. ",

        "entrepreneurial": "Making brand new things gives me thrills all the time. ",

        "diverse": "I have met people from many different backgrounds through out my life so far. ",

        "motivated": "I not only do things, I do them with passion. ",

        "detail": "While being able to see the big picture is important, I am also able to scrutinize the details. ",

        "agile": "I am able to adapt to different environments very quickly. ",

        "execute": "I love the feeling of making things happen. "
    }


    def __init__(self, naive = True):
        """ Initializor.
            If the naive flag is on, it uses all data to train the classifiers,
            else, it tries to train each classifiers with the highest accuracy using
            only half the data as training set, the other half as test set.
        """
        if (naive):
            self.usefulness_classifier = utility.train_usefulness_classifier(True)
            self.cat_classifier = utility.train_cat_classifier(True)
            return
        else:
            first_pair_u = utility.get_classifier_accuracy('u')
            first_pair_c = utility.get_classifier_accuracy('c')
            classi_u = first_pair_u[0]
            classi_c = first_pair_c[0]
            acc_u = first_pair_u[1]
            acc_c = first_pair_c[0]
            i = 0
            while (i < 10):
                i += 1
                (classifier_u, accuracy_u) = utility.get_classifier_accuracy('u')
                (classifier_c, accuracy_c) = utility.get_classifier_accuracy('c')
                if (accuracy_u > acc_u):
                    classi_u = classifier_u
                    acc_u = accuracy_c
                if (accuracy_c > acc_c):
                    classi_c = classifier_c
                    acc_c = accuracy_c
            self.usefulness_classifier = classi_u
            self.cat_classifier = classi_c
            return

    def generate_cl(self):
        """ This is the main function of the project
            It opens a file named original and operate on it.
        """
        f = open('original', mode = 'r')
        
        sents = []
        line = f.readline()
        while (line != ''):
            sent_lst = nltk.sent_tokenize(line)
            sents = sents + sent_lst
            line = f.readline()
        f.close()
        
        useful_sents = []
        for sent in sents:
            label = self.usefulness_classifier.classify(fe.sentence_features(sent))
            if (label == 'useful'):
                useful_sents.append(sent)
        
        skills_sents = []
        personal_sents = []
        for sent in useful_sents:
            label = self.cat_classifier.classify(fe.cat_features(sent))
            if (label == 'skills'):
                skills_sents.append(sent)
            else:
                personal_sents.append(sent)
        
        skills = {}
        for sent in skills_sents:
            tagged = nltk.pos_tag(nltk.word_tokenize(sent))
            pe.extract_skill_phrase(tagged, skills)
        
        adjs = {}
        for sent in personal_sents:
            tagged = nltk.pos_tag(nltk.word_tokenize(sent))
            pe.extract_adjectives(tagged, adjs)
        
        qualities = set()
        for adj in adjs:
            quality = cat.get_category(adj)
            qualities.add(quality)

        metadata = ud.get_user_metadata(metadatafile)
        skills, qualities = ud.get_user_skills(skillsfile)
        
        return