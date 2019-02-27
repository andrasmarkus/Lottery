import urllib.request
import collections
import operator
import math
from bs4 import BeautifulSoup

class Lottery:
#This class represents a HTML table reader to find the most popular/unpopular numbers of the hungarian lottery numbers including 5-ös,6-os and Skandinav ( or known as 7-es) lottery. This class works with the latest results.
#More information about these lotteries available on: https://www.szerencsejatek.hu/. Also this git repository contains the previous results from the beggining. Last updated: 26.02.19.
#	Methods: 
#	- init: initialize a defaultdict: keys will be the selectable numbers of the lottery type and values will be set to zero. Then the program gets around the HTML table which contains the previous selected numbers. The corressponding value will be increased with one. Finally, the class orders the dictionary for the selection.
#		params:
#			* url: the corresponding url to the HTML table with the previous numbers
#			* num: the range of the selectable numbers
#			* position: the start index of the HTML table with the selected numbers
#	- popular: 	choose the most common selected numbers ( return with the neccessery count of the numbers, if there are more with the same value, they will be printed as well)
#		param:
#			* wining: count of the selected numbers
#	- unpopular:  choose the rarest selected numbers ( return with the neccessery count of the numbers, if there are more with the same value, they will be printed as well)
#		param:
#			* wining: count of the selected numbers

    def __init__(self, url, num, position):
        self.url = url
        self.num = num
        self.position = position
        self.d = collections.defaultdict()
        for i in range(self.num):
            i = i+1
            self.d[i] = 0

        request = urllib.request.Request(self.url)
        response = urllib.request.urlopen(request)
        raw = response.read().decode('utf-8')
        self.table = BeautifulSoup(raw, 'html.parser')

        for row in self.table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                if column_marker > self.position:
                    if column.get_text() is not "":
                        index = int(column.get_text())
                        value = self.d[index] + 1
                        self.d[index] = value
                column_marker += 1

        self.d = sorted(self.d.items(), key=operator.itemgetter(1))

    def popular(self, wining):

        i = self.num-1
        tmp = i-wining
        while True:
            if i <= tmp:
                if self.d[tmp][1] == self.d[tmp+1][1]:
                    tmp = tmp-1
                else:
                    break
            print(str(self.d[i][0]), end=";")
            i = i-1

    def unpopular(self, wining):

        i = 0
        tmp = i+wining
        while True:
            if i >= tmp:
                if self.d[tmp][1] == self.d[tmp+1][1]:
                    tmp = tmp+1
                else:
                    break
            print(str(self.d[i][0]), end=";")
            i = i+1

    def interval(self, interval):
        print("\n" + str(interval) + "-os lottó intervallum nyerőszámai:")
        for i in range(self.num-1, 0, -int(math.ceil(self.num / interval))):
            print(str(self.d[i][0]), end=";")


lottery5url = "https://bet.szerencsejatek.hu/cmsfiles/otos.html"
l1 = Lottery(lottery5url, 90, 10)
print("\n5-ös lottó nyerőszámai:")
l1.popular(5)
print("\n5-ös lottó vesztőszámai:")
l1.unpopular(5)
l1.interval(5)

lottery6url = "https://bet.szerencsejatek.hu/cmsfiles/hatos.html"
l2 = Lottery(lottery6url, 45, 12)
print("\n6-os lottó nyerőszámai:")
l2.popular(6)
print("\n6-os lottó vesztőszámai:")
l2.unpopular(6)
l2.interval(6)

lottery7url = "https://bet.szerencsejatek.hu/cmsfiles/skandi.html"
l3 = Lottery(lottery7url, 35, 10)
print("\n7-es lottó nyerőszámai:")
l3.popular(7)
print("\n7-ös lottó vesztőszámai:")
l3.unpopular(7)
l3.interval(7)
