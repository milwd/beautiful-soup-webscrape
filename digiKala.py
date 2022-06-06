
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd


def extractText(txt, sth):
	tagStart = '<'+sth+'>'
	tagEnd = '</'+sth+'>'
	res1 = txt.find(tagStart)
	res2 = txt.find(tagEnd)
	if (res1 != -1):
		theIt = txt[res1+len(tagStart):res2]
		return theIt
	else:
		return None


def replaceMultiple(txt, dic):
	for i, j in dic.items():
		txt = txt.replace(i, j)
	return txt


def checkActive(ro):
	if ro != None:
		return ro.text
	else:
		return None


def result(inp):
	global replaceDict
	out1 = checkActive(inp)
	if out1:
		return replaceMultiple(out1, replaceDict)
	else:
		return 'not available'


# https://www.digikala.com/incredible-offers/
originalUrl = "https://www.digikala.com"
urlLink = originalUrl + "/incredible-offers/"

names = []
offs = []
prices = []
replaceDict = {'  ':'', '\n':''}
itemCount = 0
noPages = 3

for i in range(1, noPages):
	url = urlLink + '?pageno=' + str(i)
	print('\nWebscraping page : <', url, '>')
	r = Request(url, headers={'User-Agent':'Mozilla/5.0'})
	print('request sent ...')
	webpage = urlopen(r).read()
	print('response received!')
	print('page parsing initialized ...')
	soup = BeautifulSoup(webpage, 'html.parser')
	for row in soup.findAll('div', attrs={'class':'c-product-list__item js-product-list-content'}):
		itemCount += 1
		rName = row.find('div', attrs={'class':'c-product-box__title js-ab-not-app-incredible-product'})
		rPrice = row.find('div', attrs={'class':'c-price__value-wrapper js-product-card-price'})
		rOff = row.find('div', attrs={'class':'c-price__discount-oval'})
		name = result(rName)
		price = result(rPrice)
		off = extractText(str(rOff), 'span')
		names.append(name)
		prices.append(price)
		offs.append(off)
	print('page', i, 'done!')

print(itemCount, ' items read totally!')

dic = {'Name':names, 'Price':prices, 'Off':offs}
df = pd.DataFrame(dic)

df.to_csv('file1.csv', index=False, encoding='utf-8')
df.to_html('file2.html')
# name : c-product-box__title js-ab-not-app-incredible-product
# price : c-price__value-wrapper js-product-card-price
# off : c-price__discount-oval : <span>

