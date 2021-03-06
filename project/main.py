import nltk, utility
import feature_extractor as fe
import phrase_extractor as pe
import categorize as cat
import userdata as ud
import operator


class LetterGenerator:
    'Class for the letter generator'
    usefulness_classifier = None
    cat_classifier = None
    template = "My name is [NM] and I am a [GD] student at [IN].\nI study [MJ].\nI am very interested in this job posting for [PN] at [CN].\n[QT]\n[PQ].\nI think I would do well at this position. Thank you very much!\n[NM]"
    headers = {
        "creativity": "Creativity defines who I am. ",

        "communication": "I communicate effectively in complex and difficult situations. ",

        "collaboration":"Working in a team environment is something I enjoy a lot. ",

        "responsibility": "I will do everything I can to complete the tasks assigned to me. ",

        "leadership": "While I am a good follower, I also know how to lead a team. ",

        "entrepreneurial": "Building something that's never been built before is thrilling to me. ",

        "diverse": "I have worked in diverse teams and interculturally competent. ",

        "motivated": "I am highly driven and passionate about my work. ",

        "detail": "While being able to see the big picture is important, I am also able to scrutinize the details. ",

        "agile": "I am able to adapt to different environments very quickly. ",

        "execute": "I love to make things happen. I get things done."
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

    def generate_cl(self, example = 1):
        if (example == 1):
            metadatafile = "metadata1.txt"
        elif (example == 2):
            metadatafile = "metadata2.txt"
        else:
            metadatafile = "metadata.txt"
        skillsfile = "skills.txt"

        """ This is the main function of the project
            It opens a file named original0 and operate on it.
        """
        f = open('original' + str(example), mode = 'r')
        
        sents = []
        line = f.readline()
        while (line != ''):
            sent_lst = nltk.sent_tokenize(line)
            sents = sents + sent_lst
            line = f.readline()
        f.close()
        
        useful_sents = []
        print "Classifying Useful Sentences..."
        for sent in sents:
            label = self.usefulness_classifier.classify(fe.sentence_features(sent))
            if (label == 'useful'):
                useful_sents.append(sent)
                #print sent
        
        skills_sents = []
        personal_sents = []
        print "Classifying Sentence Cateogories.."
        for sent in useful_sents:
            label = self.cat_classifier.classify(fe.cat_features(sent))
            if (label == 'skills'):
                skills_sents.append(sent)
                #print sent + ": SKILLS"
            else:
                personal_sents.append(sent)
                #print sent + ": PERSONAL"
        
        skills = {}
        for sent in skills_sents:
            tagged = nltk.pos_tag(nltk.word_tokenize(sent))
            pe.extract_skill_phrase(tagged, skills)
        #print "SKILLS EXTRACTED: ", skills
        
        adjs = {}
        for sent in personal_sents:
            tagged = nltk.pos_tag(nltk.word_tokenize(sent))
            pe.extract_adjectives(tagged, adjs)
        
        qualities = []
        i= 0 
        for adj in adjs.keys():
            quality = cat.get_category(adj)
            qualities += quality
            i+=1
            print i, adj, quality
        counts = {}
        for item in qualities:
            if item in counts:
                counts[item] += 1
            else:
                counts[item] = 1
        sorted_counts = sorted(counts.items(), key=operator.itemgetter(1))
        top_three = sorted_counts[-3:]
        qualities = [i for (i,j) in top_three]

        metadata = ud.get_user_metadata(metadatafile)
        usr_skills, usr_qualities = ud.get_user_skills(skillsfile)


        matched_skills = []
        for usr_skill in usr_skills:
            if usr_skill.lower() in [s.lower() for s in skills]:
                matched_skills.append(usr_skill)
        
        matched_qualities = set(qualities) & set(usr_qualities.keys())

        print "requirement qualities:" , qualities
        print matched_qualities
        print matched_skills

        result = self.template.replace('[NM]', metadata['name'])
        result = result.replace('[GD]', metadata['degree'])
        result = result.replace('[IN]', metadata['institution'])
        result = result.replace('[MJ]', metadata['major'])
        result = result.replace('[PN]', metadata['position'])
        result = result.replace('[CN]', metadata['company'])

        if (matched_skills == []):
            result = result.replace('[QT]', '')
        else:
            qt_part = ""
            for item in matched_skills:
                qt_part = qt_part + item + ", "
            qt_sent = "I have experience in " + qt_part + "and other relevant areas."
            result = result.replace('[QT]', qt_sent)

        #Forms the [PQ] sentences
        pq_string = ""
        for key in matched_qualities:
            pq_string += (self.headers[key] + " " + usr_qualities[key] + "\n")

        result = result.replace('[PQ]', pq_string)
        print "--------------- OUTPUT -----------------\n"
        print result
        return