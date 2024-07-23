import time
from urllib import parse
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SwufeGoogleCrawler:
    def __init__(self, gg_search_url) -> None:
        self.gg_search_url = gg_search_url
        option = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(options=option)
        
    def get_paper_all_message(self, paper_title):
        strto_pn = parse.quote(paper_title)
        url = self.gg_search_url + strto_pn
        self.browser.get(url)
        time.sleep(1)
        for _ in range(5):
            try:
                element = self.browser.find_element(By.CSS_SELECTOR, "[class='gs_r gs_or gs_scl']")
                element = element.find_element(By.CSS_SELECTOR, "[class='gs_fl']")
                temp_content = element.text
                cited = temp_content.split(' ')[2].split('：')[-1]
                
                links = element.find_elements(By.XPATH, "a")
                links[1].click()
                time.sleep(1)
                
                element = self.browser.find_element(By.CSS_SELECTOR, "[class='gs_citi']")
                element.click()
                time.sleep(1)
                
                element = self.browser.find_element(By.XPATH, "/html/body")
                BibTeX = element.text
                return BibTeX
            except:
                input("现在谷歌正进行人机识别，请完成后输入ok")
                time.sleep(1)
        time.sleep(1)
        
    def get_cited(self, paper_title):
        strto_pn = parse.quote(paper_title)
        url = self.gg_search_url + strto_pn
        self.browser.get(url)
        time.sleep(1)
        for _ in range(5):
            try:
                element = self.browser.find_element(By.CSS_SELECTOR, "[class='gs_r gs_or gs_scl']")
                element = element.find_element(By.CSS_SELECTOR, "[class='gs_fl']")
                temp_content = element.text
                cited = temp_content.split(' ')[2].split('：')[-1]
                break
            except:
                input("现在谷歌正进行人机识别，请完成后输入ok")
        return cited
    
    def cited_website_update(self, paper_title):
        strto_pn = parse.quote(paper_title)
        url = self.gg_search_url + strto_pn
        self.browser.get(url)
        time.sleep(2)
        Temp_dic = {}
        for _ in range(1):
            try:
                element = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'被引用次数')]")))
                citations  = re.search(r'被引用次数：(\d+)', element.text)
                Temp_dic['cite'] = citations.group(1) if citations else 'miss'
                time.sleep(1)
                break
            except:
                input("现在谷歌正进行人机识别，请完成后输入ok")
                time.sleep(2)
            Temp_dic['cite'] = 'miss'
        return Temp_dic

    @staticmethod
    def refind(BibTeX, pattern):
        pattern_str = re.findall(pattern + '={.+}', BibTeX)[0]
        return re.findall('{.+}', pattern_str)[0][1:-1]

    def website_update(self, paper_title):
        strto_pn = parse.quote(paper_title)
        url = self.gg_search_url + strto_pn
        self.browser.get(url)
        time.sleep(2)
        Temp_dic = {}
        for _ in range(1):
            try:
                element = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.gs_ggs.gs_fl")))
                citations  = re.search(r'被引用次数：(\d+)', element.text)
                try:
                    pdf_element = element.find_element(By.CSS_SELECTOR, "a")
                    pdf_link = pdf_element.get_attribute('href')
                    Temp_dic['website'] = pdf_link
                except:
                    Temp_dic['website'] = ''
                time.sleep(1)
                break
            except:
                input("现在谷歌正进行人机识别，请完成后输入ok")
                time.sleep(2)
            Temp_dic['cite'] = 'miss'
        return Temp_dic