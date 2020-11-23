import spacy
from os import remove
from spacy.matcher import Matcher

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)
with open('input/job.txt', 'r') as j, open('input/resume.txt', 'r') as r:
    job_text = j.readlines()
    job_doc = nlp(j.read())
    resume_text = r.read()

# O(n)? 1
sentences = []
job_verbs = []
job_chunks = []
need_adding = []
resume_verbs = []
resume_chunks = []
resume_doc = nlp(resume_text)

for line in job_text:
    line_tokens = nlp(line)
    for i in range(0, len(line_tokens)):
        # https://stackoverflow.com/questions/47856247/extract-verb-phrases-using-spacy
        if line_tokens[i].pos_ == "VERB":
            job_verbs.append(line_tokens[i].lemma_.lower())
            try:
                if line_tokens[i+1].pos_ == "ADJ" and line_tokens[i+2].pos_ == "NOUN":
                    sentences.append(" ".join([line_tokens[i].text, line_tokens[i+1].text, line_tokens[i+2].text]))
            except IndexError:
                pass
            try:
                if line_tokens[i+1].pos_ == "NOUN":
                    if line_tokens[i+1].dep_ == "dobj":
                        sentences.append(" ".join([line_tokens[i].text, line_tokens[i+1].text]))
            except IndexError:
                pass
    for chunk in line_tokens.noun_chunks:
        job_chunks.append(chunk.text)

for token in resume_doc:
    if token.pos_ == "VERB":
        resume_verbs.append(token.lemma_.lower())

for chunk in resume_doc.noun_chunks:
    resume_chunks.append(chunk.text)

verb_filter = [x.replace("\n", "") for x in open('temp/common_verbs.txt').readlines()]
noun_filter = [x.replace("\n", "") for x in open('temp/common_nouns.txt').readlines()]

remove('temp/common_nouns.txt')
remove('temp/common_verbs.txt')

del job_text, resume_doc, line_tokens, nlp

verbs_need_adding = ([x for x in list(set(job_verbs)) if x not in list(set(resume_verbs)) and x not in verb_filter])
verb_matches = [x for x in list(set(job_verbs)) if x in list(set(resume_verbs)) and x not in verb_filter]
nouns_need_adding = ([x for x in list(set(job_chunks)) if x not in list(set(resume_chunks)) and x not in noun_filter])
noun_matches = [x for x in list(set(job_chunks)) if x in list(set(resume_chunks)) and x not in noun_filter]

in_filter_j = [x for x in list(set(job_verbs)) if x in verb_filter] + [x for x in list(set(job_chunks)) if x in noun_filter]
in_filter_n = [x for x in list(set(resume_verbs)) if x in verb_filter] + [x for x in list(set(resume_chunks)) if x in noun_filter]

print("caught!!")
print(in_filter_j)
print()
print(in_filter_n)

noun_matches = [x for x in list(set(job_chunks)) if x in list(set(resume_chunks)) and x not in noun_filter]

sentences = [x for x in list(set(sentences)) if "hours" not in x]

del resume_verbs, job_verbs, verb_filter

print(bcolors.BOLD + "\nVerb matches" + bcolors.ENDC)
print(bcolors.GREEN + " | ".join(verb_matches) + bcolors.ENDC + "\n")

print(bcolors.BOLD + "\nNoun chunk matches" + bcolors.ENDC)
print(bcolors.GREEN + " | ".join(noun_matches) + bcolors.ENDC + "\n")

print(bcolors.BOLD + "Add these verbs" + bcolors.ENDC)
print(bcolors.RED + " | ".join(verbs_need_adding) + bcolors.ENDC + "\n")

print(bcolors.BOLD + "Add these noun chunks" + bcolors.ENDC)
print(bcolors.RED + " | ".join(nouns_need_adding) + bcolors.ENDC + "\n")

print(bcolors.BOLD + "Phrases to consider" + bcolors.ENDC)
print(bcolors.BLUE + " | ".join(sentences) + bcolors.ENDC + "\n")
del sentences, verb_matches, need_adding
