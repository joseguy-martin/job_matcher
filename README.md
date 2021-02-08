# Resume/Job Matching
A command line tool that compares a user-input resume with a user-input job description, generating suggestions to tailor the resume for the specified job.

## Components
mangonel.sh kicks off three components for matching. bulk_job_text.py and common_lex.py pull data and identify noise that can be filtered out from suggestions made by mangonel.py.

### **bulk_job_text.py**
Uses BeautifulSoup to pull a number of job descriptions from Indeed, saving to a local text file. 

### **common_lex.py**
Takes the local text file of scraped web data and translates into a set of common verbs and nouns identified using Spacy's `en_core_web_sm` model - saving to another set of local text files.

### **match.py**
Takes the common_lex files and generate a set of matches and suggestions. Display to the user.

### Usage (Mac/Linux)
* Clone/download this repository.
* Move your resume into the input folder.
* Run the match.sh file. It will ask for your resume file name and perform the matching process.
