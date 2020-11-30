try:
    import requests
    from bs4 import BeautifulSoup
    from time import sleep
except (ModuleNotFoundError, ImportError):
    with open('.install', 'w') as f:
        quit()

start_page = requests.get('https://www.indeed.com/jobs?q=analyst&l=New%20York%2C%20NY&vjk=747467bd98c63be2')
start_page_soup = BeautifulSoup(start_page.text, 'html.parser')
job_links = ["https://www.indeed.com"+x.get('href') for x in start_page_soup.find_all('a', class_='jobtitle turnstileLink')]
del start_page, start_page_soup

with open('mangonel-cli/temp/all_text.txt', 'w') as all_text:
    for link in job_links:
        job_soup = BeautifulSoup(requests.get(link).text, 'html.parser')
        all_text.write(job_soup.get_text())
        del job_soup
del job_links
