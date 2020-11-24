try:
    from time import sleep
    from selenium import webdriver
    from selenium.common import exceptions
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
except (ModuleNotFoundError, ImportError):
    with open('.install', 'w') as f:
        quit()

chrome_options = Options()
chrome_options.add_argument('--maximize-window')
b = webdriver.Chrome(options=chrome_options)

b.get('https://www.indeed.com/')
sleep(2)
b.find_element_by_xpath('/html/body/div/div[4]/div[1]/div/div/div/form/div[1]/div[1]/div/div[2]/input').send_keys('analyst')
b.find_element_by_xpath('/html/body/div/div[4]/div[1]/div/div/div/form/div[3]/button').send_keys(Keys.ENTER)

with open('temp/all_text.txt', 'w') as all_text:
    for x in range (2):
        jobs = b.find_elements_by_xpath('//div[@class="jobsearch-SerpJobCard unifiedRow row result clickcard"]')
        for i in range(len(jobs)):
            jobs[i].click()
            try:
                b.switch_to.frame('vjs-container-iframe')
            except exceptions.NoSuchFrameException:
                print('Frame switch failed at element', i)
                quit(1)
            all_text.write(b.find_element_by_xpath('//div[@id="jobDescriptionText"]').text)
            b.switch_to.default_content()
b.close()
del jobs
