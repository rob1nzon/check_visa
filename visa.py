#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

payload = {
  '__LASTFOCUS':'',
  '__EVENTTARGET':'',
  '__EVENTARGUMENT':'',
  'ctl00$CPH$txtR2Part1':'',
  'ctl00$CPH$txtR2Part2':'',
  'ctl00$CPH$txtR2Part3':'',
  'ctl00$CPH$txtR2Part4':'',
  'ctl00$CPH$txtDOB$txtDate':'',
  'ctl00$CPH$btnDOB': u'Подтвердить'

}


def get_session_id(resp, payload):
  soup = BeautifulSoup(resp, 'html.parser')
  s = soup.find_all('form')
  l1= str(s)[str(s).find('__VIEWSTATEGENERATOR'):str(s).find('__VIEWSTATEGENERATOR')+100]
  l2= str(s)[str(s).find('__EVENTVALIDATION'):str(s).find('__EVENTVALIDATION')+320]

  payload['__VIEWSTATEGENERATOR'] = l1[l1.find('value')+7:l1.find('>')-2]
  payload['__EVENTVALIDATION'] = l2[l2.find('value')+7:l2.find('>')-2]

  payload['__VIEWSTATE'] = str(s)[str(s).find('__VIEWSTATE" type="hidden" value="')+34:str(s).find('Poland-Russia')-19]
  return str(s)[str(s).find('trackingParam'):str(s).find('" autocomplete')]


def get_status():
  r = requests.get('http://www.vfsglobal.com/poland/russia/track_application.html')
  soup = BeautifulSoup(r.text, 'html.parser')
  surl = soup.find_all('a')[3]
  url = str(surl)[str(surl).find("https"):str(surl).find("target")-2]


  with requests.session() as s:
    resp = s.get(url)
    url =  'https://www.vfsvisaservices-russia.com/poland-Russia-tracking_new/'+get_session_id(resp.text,  payload)
    response_post = s.post(url, data=payload)
    #soup = BeautifulSoup(response_post.text, 'html.parser')
    ul= response_post.text.encode('utf-8')
    #print len('<td class="fnstatus" align="left" style="width: 95%"><table border="0" width="100%" cellpadding="5" style="border: solid 1px #000000;"><tr>')
    return str(ul)[str(ul).find('fnstatus')+143:str(ul).find('fnstatus')+450]



