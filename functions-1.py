#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 19:03:35 2020

@author: luna
"""
from urllib import parse
import urllib.parse as urlparse
from urllib.parse import parse_qs
#a package to fetch and grab the HTML files itself
import requests
#import the urlopen function 
from urllib.request import urlopen as uReq
#pull the data from the HTML file and parse HTML files
from bs4 import BeautifulSoup as soup
#translate HTML to python
import lxml
import pandas as pd
import csv
import re
from tld import get_tld
from bs4 import BeautifulSoup
import urllib.request
from spellchecker import SpellChecker
from lxml import etree
import requests
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation
import ipaddress



def start_url(url):
    """Split URL into: protocol, host, path, params, query and fragment."""
    if not parse.urlparse(url.strip()).scheme:
        url = 'http://' + url
    protocol, host, path, params, query, fragment = parse.urlparse(url.strip())

    result = {
        'url': host + path + params + query + fragment,
        'protocol': protocol,
        'host': host,
        'path': path,
        'params': params,
        'query': query,
        'fragment': fragment
    }
    return result



"""lines refers to the tld.txt file which contains the list of 
valid Top Level Domains and will be used in check_valid_tld function"""
PATH='/Users/luna/Desktop/'
file = open(PATH + 'tlds.txt', 'r')
lines=file.readlines()





def read_file(archive):
    """Read the file with the URLs."""
    with open(archive, 'r') as f:
        urls = ([line.rstrip() for line in f])
        return urls
    



""""""""""LEXICAL FEATURES"""""""""""

def count(text, character):
    """Return the amount of certain character in the text, 
        if non exists returns zero."""
    return text.count(character)

#count("https://www.bbc.com/news/world-52015486", "@")

def length(text):
    """Return the length of a string."""
    return len(text)



def count_params(query):
    """Return number of parameters."""
    return len(parse.parse_qs(query))


#count_params(dict_url['query'])
#Domain

def check_word_server_client(host):
    """Return whether the "server" or "client" keywords exist in the domain."""
    if "server" in host.lower() or "client" in host.lower():
        return True
    return False

#check_word_server_client(dict_url['host'])

def check_valid_tld(url, TLDlist): 
    """Check for presence of valid Top-Level Domains (TLD) in url."""
    """Takes, a list of valid TLDs"""
    for i in range (len(TLDlist)):   
        if ("."+get_tld(url)==TLDlist[i].strip()):
            return True
            break
        
           
#check_tld(url, lines)       
    

def count_subdomains(host):
    subdomains = host.split('.')[:-2]
    return len(subdomains)

#count_subdomains(dict_url['host'])
    



"""""""WEB PAGE APPEARANCE  FEATURES- Scraped Data"""""""

def check_copyright(url):
    """return true for the copyright notice, if any, in Text"""
    try:
        sauce = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(sauce,'lxml')
        temp = soup.prettify().encode('UTF-8')
        #\xc2\xa9 is unicode symbol for copyright sign
        if(b'\xc2\xa9' in temp):
            return True
        else:
            return False
    except Exception:
        return '?'       
            
    
#check_copyright("https://profile.theguardian.com/signin")

def get_copyright(url):
    """If a page has a copyright symbol ©, extract texts of the tag containing the symbol"""
    
    try:
        sauce = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(sauce,'lxml')
        temp = soup.prettify().encode('UTF-8')
        #\xc2\xa9 is unicode symbol for copyright sign
        if(b'\xc2\xa9' in temp):
                webpage = requests.get(url)
                soup = BeautifulSoup(webpage.content,'html.parser')
                symbol = u'\N{COPYRIGHT SIGN}'.encode('utf-8')
                symbol = symbol.decode('utf-8')
                pattern = r'' + symbol
                for tag in soup.findAll(text=re.compile(pattern)):
                    copyrightTexts = tag.parent.text
                    print(copyrightTexts)       
        else:
                return '?'
    except Exception:
        return '?'       
                 

    
#get_copyright(2)
  

def get_page_header(search_url):
      """get the title of the page"""  
      try:
          uclient=uReq(search_url)
          pagehtml=uclient.read()
          uclient.close()
          pagesoup=soup(pagehtml, "html.parser")
          return pagesoup.title.text
      except Exception:
          return '?'
    
    
#get_page_header(2)

def get_page_body(search_url):
        """get the first part body of the page"""
        try:
        #HTTP GET requests
            uclient=uReq(search_url)
            pagehtml=uclient.read()
            uclient.close()
            pagesoup=soup(pagehtml, "html.parser")        
            return pagesoup.p.text
        except Exception:
            return 'URL Not Found'
    



def get_top10_commonwords(url):
        """"get a list with 10 most common words and their frequencies from most to less common"""
        try: # We get the url
            r = requests.get(url)
            soup = BeautifulSoup(r.content)
            # get the words within paragrphs
            text_p = (''.join(s.findAll(text=True))for s in soup.findAll('p'))
            c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))
            # get the words within divs
            text_div = (''.join(s.findAll(text=True))for s in soup.findAll('div'))
            c_div = Counter((x.rstrip(punctuation).lower() for y in text_div for x in y.split()))
            # We sum the two countesr and get a list with words count from most to less common
            total = c_div + c_p
            #list_most_common_words = total.most_common() 
            return total.most_common(10)
        except Exception:
            return '?'


def get_img_cnt1(url):
    """Return the number of images in a page"""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content)
        
        return len(soup.find_all('img'))
    except Exception:
            return '?'


def get_img_cnt2(url):
    """Return the number of images in a page"""

    try:
        response = requests.get(url)
        parser = etree.HTMLParser()
        root = etree.fromstring(response.content, parser=parser)
    
        return int(root.xpath('count(//img)'))
    except Exception:
            return '?'


#get_img_cnt('https://rubikscode.net/2019/12/02/scraping-images-with-python/')


    
def spell_check(text):
    """Return number of misspelled words in a text"""
    words = text.split()
    my_list = [] # make empty list
    for current_word in words:
        my_list.append(current_word.lower()) 
        spell = SpellChecker()
    return len(spell.unknown(my_list))

#spell_check(text)  
    
    

""""""""""CONNECTION FEATURES"""""""""

def count_redirects(url):
    """Return the number of redirects in a URL."""
    try:
        response = requests.get(url)
        if response.history:
            return len(response.history)
        else:
            return 0
    except Exception:
        return '?'

#count_redirects("https://docs.python.org/3.2/library/csv.html")


def valid_ip(host):
    """Return if the domain has a valid IP format (IPv4 or IPv6)."""
    try:
        ipaddress.ip_address(host)
        return True
    except Exception:
        return False
    



--------- """compile all functions"""


def attributes():
    """Output file attributes."""
    lexical = [ 
            'dot_url', 'hyphe_url', 'question_url',  
            'atsign_url', 'len_url','copyright_sign',
            'copyright_text','page_title','page_body',
            'top_10_words','image_count','dot_host', 
            'bar_host','atsign_host','and_host','server_client', 
            'subdomains_count','valid_ip','validate_tld', 
            'count_parameters', 
            #'count_redirect' 
            ]
    
    
    
    list_attributes = []
    list_attributes.extend(lexical)
    return list_attributes


    
 
def main(example_urls):
    """outputs a csv file with all the extracted feature from the list of URLs"""
    #first create and empty csv file
    dataset="/Users/luna/Downloads/dataset.csv"
    PATH='/Users/luna/Desktop/'
    file = open(PATH + 'tlds.txt', 'r')
    lines=file.readlines()
    with open(dataset, "w") as output:
        writer = csv.writer(output)
        writer.writerow(attributes())
        count_url = 0
        for url in example_urls:
            count_url = count_url + 1
            dict_url = start_url(url)

            # URL
            dot_url = str(count(url, '.'))
            hyphe_url = str(count(url, '-'))
            question_url = str(count(url, '?'))
            atsign_url = str(count(url, '@'))
            len_url = str(length(url))
            copyright_sign=check_copyright(url)
            copyright_text=get_copyright(url)
            page_title=get_page_header(url)
            page_body=get_page_body(url)
            top_10_words=get_top10_commonwords(url)
            image_count=str(get_img_cnt2(url))
        
            
            # DOMAIN
            dot_host = str(count(dict_url['host'], '.'))
            bar_host = str(count(dict_url['host'], '/'))
            atsign_host = str(count(dict_url['host'], '@'))
            and_host = str(count(dict_url['host'], '&'))
            server_client = str(check_word_server_client(dict_url['host']))
            subdomains_count=str(count_subdomains(dict_url['host']))
        
            
            # HOST
            validate_ip = valid_ip(dict_url['host'])
            validate_tld = str(check_valid_tld(url,lines ))
            count_parameters = str(count_params(dict_url['query']))
            #count_redirect = str(count_redirects(dict_url['protocol'] + '://' + dict_url['url']))
            
            
            
            _lexical=[ 
            dot_url, hyphe_url, question_url,  
            atsign_url, len_url,copyright_sign,
            copyright_text, page_title, page_body,
            top_10_words, image_count, dot_host, 
            bar_host, atsign_host , and_host, server_client, 
            subdomains_count, validate_ip, validate_tld, 
            count_parameters, 
            #count_redirect 
            ]
        
            
            result = []
            result.extend(_lexical)
        
            writer.writerow(result)
            
"""compile all functions"""
            

example_urls = ["https://www.slideshare.net/weaveworks/client-side-monitoring-with-prometheus",
                "http://cartaobndes.gov.br.cv31792.tmweb.ru/",
                "https://paypal.co.uk.yatn.eu/m/",
                "http://college-eisk.ru/cli/",
                "https://dotpay-platnosc3.eu/dotpay/"
               ]




main(example_urls)
              
"""  

def main(url):
    
    PATH='/Users/luna/Desktop/'
    file = open(PATH + 'tlds.txt', 'r')
    lines=file.readlines()
    
    dict_url = start_url(url)

            # URL
    dot_url = str(count(url, '.'))
    hyphe_url = str(count(url, '-'))
    question_url = str(count(url, '?'))
    atsign_url = str(count(url, '@'))
    len_url = str(length(url))
    copyright_sign=check_copyright(url)
    copyright_text=get_copyright(url)
    page_title=get_page_header(url)
    page_body=get_page_body(url)
    top_10_words=get_top10_commonwords(url)
    image_count=str(get_img_cnt2(url))

    
    # DOMAIN
    dot_host = str(count(dict_url['host'], '.'))
    bar_host = str(count(dict_url['host'], '/'))
    atsign_host = str(count(dict_url['host'], '@'))
    and_host = str(count(dict_url['host'], '&'))
    server_client = str(check_word_server_client(dict_url['host']))
    subdomains_count=str(count_subdomains(dict_url['host']))

    
    # HOST
    validate_ip = valid_ip(dict_url['host'])
    validate_tld = str(check_valid_tld(url,lines ))
    count_parameters = str(count_params(dict_url['query']))
    #count_redirect = str(count_redirects(dict_url['protocol'] + '://' + dict_url['url']))
    
    
    
    _lexical=[ 
    dot_url, hyphe_url, question_url,  
    atsign_url, len_url,copyright_sign,
    copyright_text, page_title, page_body,
    top_10_words, image_count, dot_host, 
    bar_host, atsign_host , and_host, server_client, 
    subdomains_count, validate_ip, validate_tld, 
    count_parameters, 
    #count_redirect 
    ]

    
    result = []
    result.extend(_lexical)
    return result


url="https://jobs.sub.ericsson.com/main/auth/1/login?jobId=350044"
            
main(url)

    
      """      