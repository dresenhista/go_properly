from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import json
import pandas as pd
import os
import re
import requests
import re
import sys
import time
import yaml

def parse_listing(raw):
    txt = BeautifulSoup(raw)
    content = txt.find_all('div', {'id': '_ctl0_m_divAsyncPagedDisplays'})[0]
    kv = {}
    kv['base_description'] = content.find_all('span', {'class': 'd-textSoft'})[0].text
    kv['day_sold'] = txt.find_all('div', id='wrapperTable')[0].find_all('span', {'class': 'd-text'})[3].text
    kv['dom'] = txt.find_all('div', id='wrapperTable')[0].find_all('span', {'class': 'd-textStrong'})[0].text
    address = ' '.join(content.find_all('div', {'class': 'row'})[21].text.split()[1:])
    features = content.find_all('div', {'class' : 'col-xs-12'})
    if len(features) == 0:
        raise Exception('Re do.')
    i = 0 
    while True:
        try:
            kv[features[i].find_all('span', {'class': 'd-textStrong'})[0].text] = features[i].find_all('span', {'class': 'd-text'})[0].text
        except:
            break
        i += 1
    kv['rooms'] = []
    rooms = txt.find_all('div', {'class' : 'col-sm-4'})
    for i in xrange(4, len(rooms)-3, 3):
        kv['rooms'].append([rooms[i].text, rooms[i+1].text, rooms[i+2].text])
    return address, kv

def parse_url(browser, links):
    kv = {}
    failed = []
    while True:
        try:
            bs = BeautifulSoup(browser.page_source)
            entries = bs.find_all('div', {'class': 'multiLineDisplay'})
            for entry in entries:
                sys.stdout.flush()
                link = entry.find_all('span', {'class': 'formula J_formula'})[2].text.strip()
                if link in links:
                    continue
                else:
                    counter = 0
                    while True:
                        try:
                            print 'Going to ' + link
                            browser.find_element_by_link_text(link).click()
                            break
                        except:
                            if counter > 10:
                                failed.append(link)
                                break
                            counter += 1
                            print 'Waiting for link...' + link
                            sleep(1)
                    links.add(link)       
                    counter = 0
                    while True:
                        try:
                            sleep(2)
                            print 'Entering...'
                            key, value = parse_listing(browser.page_source)
                            print 'Processed ' + link
                            kv[key] = value
                            break
                        except Exception as e:
                            if counter > 10:
                                failed.append(link)
                                break
                            counter += 1
                            print e
                            sleep(1)
                try:
                    browser.find_element_by_id('_ctl0_m_btnClosePILP').click()
                except:
                    print e
                sleep(2)
            counter = 0
            kill = False
            while True:
                try:
                    button = browser.find_element_by_link_text('See More Results')
                    button.click()
                    break
                except Exception as e:
                    counter += 1
                    print e
                    if counter > 10:
                        kill = True
                        break
                    sleep(1)
            if kill:
                break
            sleep(1)
        except Exception as e:
            print e
            break
    return kv, links, failed
    
if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        urls = [l.strip() for l in f.readlines()]
    if len(sys.argv) > 2:
        with open(sys.argv[2]) as f:
            urls_processed = set(f.readlines())
    else:
        urls_processed = set() 
    base_dir = 'scraped_data/'
    browser = webdriver.Chrome('C:/Users/aruparell/Downloads/chromedriver_win32/chromedriver')
    for url in urls:
        browser.get(url)
        print ">>>>>> " + url
        sleep(5)
        identifier = url.split('?')[-1]
        entries, urls_used, failed = parse_url(browser, urls_processed)
        urls_processed = urls_processed.union(urls_used)
        with open('{}/{}.attrs'.format(base_dir, identifier), 'w+') as f:
            json.dump(entries, f)
        with open('{}/urls_processed_temp'.format(base_dir), 'w+') as f:
            f.write('\n'.join(urls_processed))
        with open('{}/{}.failed'.format(base_dir, identifier), 'w+') as f:
            f.write('\n'.join(failed))
        with open('{}/urls_processed'.format(base_dir), 'w+') as f:
            f.write('\n'.join(urls_processed))
            os.unlink('{}/urls_processed_temp'.format(base_dir)) 

