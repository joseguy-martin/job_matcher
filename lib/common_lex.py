try:
    import spacy
    from os import remove
    from collections import Counter
except (ModuleNotFoundError, ImportError):
    with open("temp/.install", 'w') as f:
        quit()

nlp = spacy.load('en_core_web_sm')
doc = nlp(open('temp/all_text.txt', 'r').read())
# remove('temp/all_text.txt')
del nlp

verbs = [token.lemma_ for token in doc if token.is_stop != True and token.is_punct != True and token.pos_ == "VERB"]
verb_export = [x[0] for x in Counter(verbs).most_common(100)]
verb_export.sort()

noun_chunks = [chunk.text for chunk in doc.noun_chunks]
noun_export = [x[0] for x in Counter(noun_chunks).most_common(100)]
noun_export.sort()

del verbs, doc

with open('temp/common_verbs.txt', 'w') as f:
    f.writelines("\n".join(verb_export))

with open('temp/common_nouns.txt', 'w') as f:
    f.writelines("\n".join(noun_export))
