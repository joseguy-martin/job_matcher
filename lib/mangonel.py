try:
    import spacy
    import docx2txt
    from os import remove
    import slate3k as slate
    from spacy.matcher import Matcher
except (ModuleNotFoundError, ImportError):
    with open('temp/.install', 'w') as f:
        quit()

# Set of colors for command line display
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

# Load spacy's English model and read the input files
nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)
with open('input/job.txt', 'r') as j:
    job_text = j.readlines()
    job_doc = nlp(j.read())

# User input for resume file
resume_file = input('Please enter filename for your resume:\n')
resume_file_type = resume_file.split('.')[len(resume_file.split('.'))-1].lower()
while True:
    try:
        with open(resume_file, 'r') as r:
            if 'pdf' in resume_file_type:
                resume_text = "\n".join(slate.PDF(r))
                break
            elif 'txt' in resume_file_type:
                resume_text = r.read()
                break
            elif 'docx' in resume_file_type:
                resume_text = docx2txt.process(r)
            else:
                print("Unsupported file type. Try again.")
    except FileNotFoundError:
        print('File not found. Try again.')

# Initialize variables
job_verbs = []
job_chunks = []
need_adding = []
resume_verbs = []
resume_chunks = []
phrases_to_consider = []
resume_doc = nlp(resume_text)

# Read noun chunks and verbs from the job text
for line in job_text:
    line_tokens = nlp(line)
    for i in range(len(line_tokens)):
        # Read verb phrases from the job text
        if line_tokens[i].pos_ == 'VERB':
            job_verbs.append(line_tokens[i].lemma_.lower())
            try:
                if line_tokens[i+1].pos_ == 'ADJ' and line_tokens[i+2].pos_ == 'NOUN':
                    phrases_to_consider.append(' '.join([line_tokens[i].text, line_tokens[i+1].text, line_tokens[i+2].text]))
            except IndexError:
                pass
            try:
                if line_tokens[i+1].pos_ == 'NOUN':
                    if line_tokens[i+1].dep_ == 'dobj':
                        phrases_to_consider.append(' '.join([line_tokens[i].text, line_tokens[i+1].text]))
            except IndexError:
                pass
    for chunk in line_tokens.noun_chunks:
        job_chunks.append(chunk.text)

# Read verbs from the resume
for token in resume_doc:
    if token.pos_ == 'VERB':
        resume_verbs.append(token.lemma_.lower())

# Read noun chunks from the resume
for chunk in resume_doc.noun_chunks:
    resume_chunks.append(chunk.text)

# Generate filter lists from the common files and remove
verb_filter = [x.replace('\n', '') for x in open('temp/common_verbs.txt').readlines()]
noun_filter = [x.replace('\n', '') for x in open('temp/common_nouns.txt').readlines()]
remove('temp/common_nouns.txt')
remove('temp/common_verbs.txt')

del job_text, resume_doc, line_tokens, nlp

# Match verbs and nouns
verbs_need_adding = ([x for x in list(set(job_verbs)) if x not in list(set(resume_verbs)) and x not in verb_filter])
verb_matches = [x for x in list(set(job_verbs)) if x in list(set(resume_verbs)) and x not in verb_filter]
nouns_need_adding = ([x for x in list(set(job_chunks)) if x not in list(set(resume_chunks)) and x not in noun_filter])
noun_matches = [x for x in list(set(job_chunks)) if x in list(set(resume_chunks)) and x not in noun_filter]
phrases_to_consider = [x for x in list(set(phrases_to_consider)) if 'hours' not in x]

# Capture and display the words that were filtered
in_filter_j = [x for x in list(set(job_verbs)) if x in verb_filter] + [x for x in list(set(job_chunks)) if x in noun_filter]
in_filter_n = [x for x in list(set(resume_verbs)) if x in verb_filter] + [x for x in list(set(resume_chunks)) if x in noun_filter]
print('caught!!')
print(in_filter_j)
print()
print(in_filter_n)

del resume_verbs, job_verbs, verb_filter

# Display
print(bcolors.BOLD + '\nVerb matches' + bcolors.ENDC)
print(bcolors.GREEN + ' | '.join(verb_matches) + bcolors.ENDC + '\n')

print(bcolors.BOLD + '\nNoun chunk matches' + bcolors.ENDC)
print(bcolors.GREEN + ' | '.join(noun_matches) + bcolors.ENDC + '\n')

print(bcolors.BOLD + 'Add these verbs' + bcolors.ENDC)
print(bcolors.RED + ' | '.join(verbs_need_adding) + bcolors.ENDC + '\n')

print(bcolors.BOLD + 'Add these noun chunks' + bcolors.ENDC)
print(bcolors.RED + ' | '.join(nouns_need_adding) + bcolors.ENDC + '\n')

print(bcolors.BOLD + 'Phrases to consider' + bcolors.ENDC)
print(bcolors.BLUE + ' | '.join(phrases_to_consider) + bcolors.ENDC + '\n')

del phrases_to_consider, verb_matches, need_adding
