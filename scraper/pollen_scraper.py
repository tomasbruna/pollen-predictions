#!/usr/bin/python
# Author: Tomas Bruna
# This script scrapes pollen data from http://www.atlantaallergy.com/pollen_counts
# from June 6 1991 up until 2018.

from bs4 import BeautifulSoup
import urllib


class PollenParser:

    def parse(self, year, month, day):
        url = self.__buildUrl(year, month, day)
        print("Parsing " + url)
        page = urllib.urlopen(url).read()
        self.soup = BeautifulSoup(page, "lxml")
        # Parse total pollen counts. If this span is missing, data
        # for this day has not been collected.
        countsSpan = self.soup.find_all("span", class_="pollen-num")
        if len(countsSpan) == 0:
            self.empty = True
            return False

        self.empty = False
        self.counts = int(countsSpan[0].text)
        self.__parseCategories()
        return True

    def __parseCategories(self):
        categories = self.soup.find_all("div", class_="gauge")

        self.levels = [None] * 3
        for i in range(0, 3):
            self.levels[i] = self.__determinePollenLevel(categories[i])

        self.contributors = [None] * 3
        for i in range(0, 3):
            self.contributors[i] = categories[i].p.text.encode('utf-8')\
                .strip().replace("\xa0", "").replace("\xc2", "")

    def __determinePollenLevel(self, category):
        levels = category.find_all("div", class_="gauge-segments")
        activeLevel = levels[0].find_all("span", class_="active")
        return str(activeLevel[0].text.split("=")[0])

    def __buildUrl(self, year, month, day):
        self.year = str(year)
        self.month = str(month).zfill(2)
        self.day = str(day).zfill(2)
        end = self.year + "/" + self.month + "/" + self.day
        return "http://www.atlantaallergy.com/pollen_counts/index/" + end

    def write(self, outFile):
        outFile.write(self.year + "\t" + self.month + "\t" + self.day + "\t")
        if self.empty:
            outFile.write("\t\t\t\t\t\t")
        else:
            outFile.write(str(self.counts) + "\t")
            for i in range(0, 3):
                outFile.write(self.levels[i] + "\t")
                outFile.write(self.contributors[i])
                if (i != 2):
                    outFile.write("\t")
        outFile.write("\n")


def writeHeader(outFile):
    outFile.write(
        "Year\tMonth\tDay\tTotal Count\tTree Level\tTree Top Contributors\t")
    outFile.write(
        "Grass Level\tGrass Top Contributors\tWeed Level\t Weed Top Contributors\n")


def main():
    parser = PollenParser()
    outFile = open("out.tsv", "w")
    writeHeader(outFile)

    longMonths = [1, 3, 5, 7, 8, 10, 12]
    for year in range(1991, 2019):
        for month in range(1, 13):
            lastDay = 30
            if (month in longMonths):
                lastDay = 31
            if (month == 2):
                if year % 4 == 0:
                    lastDay = 29
                else:
                    lastDay = 28
            for day in range(1, lastDay + 1):
                parser.parse(year, month, day)
                parser.write(outFile)

    outFile.close()


if __name__ == '__main__':
    main()
