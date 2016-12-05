from collections import defaultdict

meta_tags = ['name','year','degree','major','institution','position','company']
quality_tags = ['skills','creativity','communication','collaboration','responsibility','leadership','entrepreneurial','diverse','motivated','detail','agile','execute']

def get_user_metadata(filename):
    extracted = defaultdict(str)
    f = open(filename)
    data = f.read().split('\n')
    for datum in data:
        parts = datum.split(':')
        tag = parts[0].strip()
        if tag in meta_tags and parts[1].strip():
            extracted[tag] = parts[1].strip()
    f.close()
    return extracted


def get_user_skills(filename):

    qualities = defaultdict(str)
    f = open(filename)
    data = f.read().split('\n')
    for datum in data:
        parts = datum.split(':')
        tag = parts[0].strip()
        if tag in quality_tags and parts[1].strip():
            qualities[tag] = parts[1].strip()

    skills = qualities['skills'].split(",")
    qualities.pop('skills')
    f.close() 
    return skills,qualities

