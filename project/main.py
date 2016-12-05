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
    template = "My name is [NM] and I am a [GD] student at [IN].\nI study [MJ].\nI am very interested in this job posting for [PN] at [CN].\n[QT]\n[PQ].\nI think I would do well at this position. Thank you very much!\n[NM]"
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
        for adj in adjs.keys()[:10]:
            quality = cat.get_category(adj)
            qualities |= set(quality)

        metadata = ud.get_user_metadata(metadatafile)
        usr_skills, usr_qualities = ud.get_user_skills(skillsfile)


        matched_skills = []
        for usr_skill in usr_skills:
            if usr_skill.lower() in [s.lower() for s in skills]:
                matched_skills.append(usr_skill)
        
        matched_qualities = qualities & set(usr_qualities.keys())

        print "requirement qualities:" , qualities
        print matched_qualities
        print matched_skills


        result = self.template.replace('[NM]', metadata['name'])
        result = result.replace('[GD]', metadata['degree'])
        result = result.replace('[IN]', metadata['institution'])
        result = result.replace('[MJ]', metadata['major'])
        result = result.replace('[PN]', metadata['position'])
        result = result.replace('[CN]', metadata['company'])

        #Forms the [PQ] sentences
        pq_string = ""
        for key in matched_qualities:
            pq_string += self.headers[key] + " " + usr_qualities[key]

        result = result.replace('[PQ]', pq_string)
        print result
        return