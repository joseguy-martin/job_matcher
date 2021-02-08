import requests
from bs4 import BeautifulSoup

# Get the start page and gather the links to each job
start_page = requests.get('https://www.indeed.com/jobs?q=analyst&l=New%20York%2C%20NY&vjk=747467bd98c63be2')
start_page_soup = BeautifulSoup(start_page.text, 'html.parser')
job_links = ["https://www.indeed.com"+x.get('href') for x in start_page_soup.find_all('a', class_='jobtitle turnstileLink')]
del start_page, start_page_soup

# Write each job into the all-text file for scraping by common_lex
with open('temp/all_text.txt', 'w') as all_text:
    for link in job_links:
        job_soup = BeautifulSoup(requests.get(link).text, 'html.parser')
        all_text.write(job_soup.findAll('div', {'class':'jobsearch-jobDescriptionText'})[0].get_text())
        del job_soup
del job_links
