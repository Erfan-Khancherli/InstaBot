from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
import time
import requests
from bs4 import BeautifulSoup
import re
import json
import pyautogui



class InstagramBot:

    def __init__(self, username , password):

        self.username = username
        self.password = password
        self.base_url = 'https://www.instagram.com'
        self.driver = webdriver.Firefox()
        self.login()

    def login(self ):
        self.driver.get('{}/accounts/login/'.format(self.base_url))
        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        self.driver.find_elements_by_xpath("//div[contains(text(), 'Log In')]")[0].click()
        time.sleep(6)
    def see_user(self ,user):
    
        self.driver.get('{}/{}/'.format(self.base_url , user))
    
    def follow_user(self ,user):
        self.see_user(user)
        self.driver.find_elements_by_xpath("//button[contains(text(), 'Follow')]")[0].click()
    def Like_Post(self , user):
        self.see_user(user)
        links = self.driver.find_elements_by_xpath("//div/a")
        valid_links = []

        for i in range(0,len(links)):
            href = links[i].get_attribute('href')
            if href.startswith('https://www.instagram.com/p/'):
                valid_links.append(href)

        for link in valid_links: 
            try :
                self.driver.get(link)
                a = self.driver.find_element_by_xpath('//*[name()="svg"][@aria-label="Like"][@height="24"]')
                time.sleep(2)
                a.click()
            except Exception:
                continue
            
    def List_Follower_Following(self , user):            
        self.see_user(user)
        txt = requests.get('{}/{}/'.format(self.base_url , user))
        soup = BeautifulSoup(txt.text , 'html.parser')
        Followers = re.findall("<meta content=\"([0-9k KMm\.,]+) Followers" , str(soup))
        Following = re.findall("<meta content=\"[0-9k KMm\.,]+ Followers,\s([0-9k KMm\.,]+) " , str(soup))
        f= open("Folowers_Following.txt", "w")
        f.write('Number of Followers : '+ str(Followers[0]+'\n----------')) 
        f.close()
            
        self.driver.find_element_by_partial_link_text("follower").click()

        WebDriverWait(self.driver, 10).until(lambda d: d.find_element_by_css_selector('div[role="dialog"]'))

        SCROLL_PAUSE = 1 
        
        while True:
            last_height = self.driver.execute_script('''
            var fDialog = document.querySelector('div[role="dialog"] .isgrP');
            fDialog.scrollTop = fDialog.scrollHeight
            return fDialog.scrollHeight;
            ''')
                
            time.sleep(SCROLL_PAUSE)

            new_height = self.driver.execute_script('''
            var fDialog = document.querySelector('div[role="dialog"] .isgrP');
            fDialog.scrollTop = fDialog.scrollHeight
            return fDialog.scrollHeight;
            ''')
            if new_height == last_height:
                break
            last_height = new_height
            
        list_Follow = []
        for i in range(1, int(Followers[0])):
            xpath = "/html/body/div[4]/div/div/div[2]/ul/div/li[{}]/div/div[1]/div[2]/div[1]/span/a".format(i)
            followers_elems = self.driver.find_elements_by_xpath(xpath)
            followers_temp = [e.text for e in followers_elems]  # List of followers (username, full name, follow text)
            list_Follow.append(followers_temp)
            f= open("Folowers_Following.txt", "a")
            f.write('\nfollower[{}]:'.format(i)+(str(list_Follow[i-1])[2:-2])+'\n----------')
            f.close()
            
        self.see_user(user)

        self.driver.find_element_by_partial_link_text("following").click()

        WebDriverWait(self.driver, 10).until(lambda d: d.find_element_by_css_selector('div[role="dialog"]'))

        SCROLL_PAUSE = 1.5
                
        while True:
            last_height = self.driver.execute_script('''
            var fDialog = document.querySelector('div[role="dialog"] .isgrP');
            fDialog.scrollTop = fDialog.scrollHeight
            return fDialog.scrollHeight;
            ''')
                    
            time.sleep(SCROLL_PAUSE)
   
            new_height = self.driver.execute_script('''
            var fDialog = document.querySelector('div[role="dialog"] .isgrP');
            fDialog.scrollTop = fDialog.scrollHeight
            return fDialog.scrollHeight;
            ''')
            if new_height == last_height:
                break
            last_height = new_height
              
        list_Following = []

        for i in range(1, int(Following[0])):
            xpath = "/html/body/div[4]/div/div/div[2]/ul/div/li[{}]/div/div[1]/div[2]/div[1]/span".format(i)
            following_elems = self.driver.find_elements_by_xpath(xpath)
            following_temp = [e.text for e in following_elems]  # List of followers (username, full name, follow text)
            list_Following.append(following_temp)
            f= open("Folowers_Following.txt", "a")
            f.write('\nfollowing[{}]:'.format(i)+(str(list_Following[i-1])[2:-2])+'\n----------')
            f.close()   
            
    def comment(self , user):
        
        self.see_user(user)

        links = self.driver.find_elements_by_xpath("//div/a")
        valid_links = []

        for i in range(0,len(links)):
            href = links[i].get_attribute('href')
            if href.startswith('https://www.instagram.com/p/'):
                valid_links.append(href)
        if len(valid_links) == 0:
            print('No Post')
        else : 
            k=[]
            Max=0
            Link_list = []
            try:
                for link in valid_links:
                
                    self.driver.get(link)
                    time.sleep(3)
                    try :
                        p_element = self.driver.find_elements_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div[2]')[0].text
                        if 'Liked' == p_element.find('Liked'):
                            p = re.findall("(\d.*) " , p_element)
                            p1=re.sub(r',' , '' , p[0])
                            p1=int(int(p1)+1)
                            if p1 > Max : 
                                Max=p1
                                Link_list.append(link)
                        else : 
                            p = re.findall("(\d.*) " , p_element)
                            p1=re.sub(r',' , '' , p[0])
                            p1=int(p1)
                            if p1 > Max : 
                                Max=p1
                                Link_list.append(link)
                    except IndexError:
                        continue
                self.driver.get(Link_list[-1])
                time.sleep(1)
                selector=self.driver.find_element_by_xpath('//*[name()="svg"][@aria-label="Comment"]').click()
                pyautogui.typewrite('hi : )')
                pyautogui.press('enter')
            except IndexError:
                print('just has videos ')
    def comment_find(self , user):
        pass
            

if __name__ == '__main__':
    print('+---------------------------------+')
    print('|    Welcome to Instagram Bot     |')
    print('|                                 |')
    print('|1-Follow User                    |')
    print('|2-Like All Of User Post          |')
    print('|3-Comment the Best Post          |')
    print('|4-Follower and Following List    |')
    print('|                                 |')
    print('+---------------------------------+')
    Number=int(input("what do you want ?!!! : "))
    if Number == 1 or Number == 2 or Number == 3 or Number == 4 :
        user = input("whats your attack user ?!!")
    if Number == 1:
        username = input('whats your instagram username ?!')
        password = input('whats your instagram password ?!')
        ig_bot = InstagramBot(username,password)
        ig_bot.follow_user(user)
    if Number == 2:
        username = input('whats your instagram username ?!')
        password = input('whats your instagram password ?!')
        ig_bot = InstagramBot(username,password)
        ig_bot.Like_Post(user)
    if Number == 3:
        username = input('whats your instagram username ?!')
        password = input('whats your instagram password ?!')
        ig_bot = InstagramBot(username,password)
        ig_bot.comment(user)
    if Number == 4:
        username = input('whats your instagram username ?!')
        password = input('whats your instagram password ?!')
        ig_bot = InstagramBot(username,password)
        ig_bot.List_Follower_Following(user)
