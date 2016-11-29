from collections import defaultdict

"""
Note: Only skeleton code. Actual functionality yet to be implemented.
"""

def match_phrase_knowledge(phraselist,user_skill_list):
    """ 
    @param phraselist: A list of phrases/words identified by classifier and chunker. 
    @param user_skill_list: A list of skills provided by user. 
    Returns: A list of pairs of matched phrase-user skill.
    """
    return [('phrase','item')]

def sentence_generator(phrase,skill):
    """
    @param matched_pair: pair of phrase and matching user skill.
    Returns: A sentence which expresses that the candidate has given quality/skill. 
    """
    #phrase, resume_point = matched_pair
    return phrase+skill

def write_letter(phraselist, knowledge_base):
    """
    @param phraselist: a tuple containing two dictionaries for hard and soft skills.In each dictionary, key = phrase, value = part of speech tag from original sentence.
    @knowledge base: a tuple containing two dictionaries for hard and soft skills. In each dictionary, key = skill, value = a sentence describing how the user has that skill.
    Returns: A paragraph of cover letter text.
    """
    phard, psoft = phraselist
    uhard, usoft = knowledge_base
    mpairs_hard = match_phrase_knowledge(phard.keys(),uhard.keys())
    mpairs_soft = match_phrase_knowledge(psoft.keys(),usoft.keys())
    matched_pairs = list(set(mpairs_hard+mpairs_soft)) 
    sen = []
    for phrase,skill in mpairs_hard:
        sen.append(sentence_generator(phrase,skill))
        sen.append(uhard[skill])
    for phrase,skill in mpairs_soft:
        sen.append(sentence_generator(phrase,skill))
        sen.append(usoft[skill])

    return '. '.join(sen)+"."

phard = defaultdict()
phard['Hello'] = 'N'
phard['Preey'] = 'J'
phard['item'] = 'O'
psoft = defaultdict()
psoft['pretty print'] = 'NN'
psoft['item']= 'I was part of this'
usoft = psoft
uhard = phard
print write_letter((phard,psoft),(uhard,usoft))
