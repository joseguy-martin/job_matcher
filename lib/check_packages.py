try:
    import spacy
    import textract
    import bs4
except (ModuleNotFoundError, ImportError):
    with open('temp/.install', 'w') as f:
        quit()
