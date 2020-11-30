try:
    import spacy
    from os import remove
    from collections import Counter
except (ModuleNotFoundError, ImportError):
    with open('temp/.install', 'w') as f:
        quit()

# Load spacy and read file.
nlp = spacy.load('en_core_web_sm')
doc = nlp(open('temp/all_text.txt', 'r').read())
remove('temp/all_text.txt')
del nlp

# Get verbs, filtering for stopwords, punctuation, auxiliaries
verbs = [token.lemma_ for token in doc if not token.is_stop and token.pos_ == 'VERB' and token.tag_ != 'AUX']
verb_export = [x[0] for x in Counter(verbs).most_common(100)]
verb_export.sort()

# Get all noun chunks
noun_chunks = [chunk.text for chunk in doc.noun_chunks]
noun_export = [x[0] for x in Counter(noun_chunks).most_common(100)]
noun_export.sort()

del verbs, doc

# Write the results to the temp folder, handing off to mangonel.py
with open('temp/common_verbs.txt', 'w') as f:
    f.writelines('\n'.join(verb_export))

with open('temp/common_nouns.txt', 'w') as f:
    f.writelines('\n'.join(noun_export))
