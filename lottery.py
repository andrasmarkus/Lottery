import urllib.request
from bs4 import BeautifulSoup
import collections
import operator


class Lottery:

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
        print()
        print(self.d)

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


lottery5url = "https://bet.szerencsejatek.hu/cmsfiles/otos.html"
l1 = Lottery(lottery5url, 90, 10)
print("\n5-ös lottó nyerőszámai:")
l1.popular(5)
print("\n5-ös lottó vesztőszámai:")
l1.unpopular(5)

lottery6url = "https://bet.szerencsejatek.hu/cmsfiles/hatos.html"
l2 = Lottery(lottery6url, 45, 12)
print("\n6-os lottó nyerőszámai:")
l1.popular(6)
print("\n6-os lottó vesztőszámai:")
l2.unpopular(6)

lottery7url = "https://bet.szerencsejatek.hu/cmsfiles/skandi.html"
l3 = Lottery(lottery7url, 35, 10)
print("\n7-es lottó nyerőszámai:")
l3.popular(7)
print("\n7-ös lottó vesztőszámai:")
l3.unpopular(7)
