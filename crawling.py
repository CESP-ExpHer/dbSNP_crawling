
from bs4 import BeautifulSoup
import requests
from http.client import responses
import re
import os

class noSNP(Exception):
    pass

def getHTMLAsBeautifulSoup(url: str) -> BeautifulSoup:
    """
    :param url: URL address
    """
    r = requests.get(url)
    if r.status_code >= 400:
        raise requests.RequestException(str(r.status_code) + ": " + responses[r.status_code])
    if r.status_code != 200:
        print("Warning: response " + str(r.status_code) + "(" + responses[r.status_code] + ") for URL: " + url)
    return BeautifulSoup(r.text, "html.parser")


class Crawling:
    def __init__(self, fileName: str, SNP: str = None, Chr:str =None, Pos:str = None, GRCh: str = None, sep: str = ',') -> object:
        self.fileName = fileName
        self.SNP = SNP
        self.Chr = Chr
        self.Pos = Pos
        self.GRCh = GRCh
        self.sep = sep



    def getDataFromDBSNP(self, url: str, maxRetry: int = 2) -> dict:

        # define regular expression based on the GRCh
        if self.GRCh == "GRCh37":
            GRChRX = re.compile("[0-9]{1,2}[:][0-9]{1,20}\n\(GRCh37\)")
        elif self.GRCh == "GRCh38":
            GRChRX = re.compile("[0-9]{1,2}[:][0-9]{1,20}\n\(GRCh38\)")

        # flag indicating if the value was successfully retrieved
        success = False
        # number of remaining attempts
        attemptsRemaining = maxRetry
        resultDict = dict()

        while not success:
            try:
                attemptsRemaining -= 1
                bsData = getHTMLAsBeautifulSoup(url)

                # Check if the SNP exists
                exist = bsData.find('h2', attrs={"class": "search-results"})
                if exist != None:
                    break

                # get the chromosome position
                chromosomeData = bsData.find_all('dl', attrs={"class": "snpsum_dl_left_align"})

                # get the SNP name
                SNP_name = bsData.find_all('div', attrs={"class": "supp"})
                SNP_name = SNP_name[0].find_all('a')[0].get_text()

                # remove <br/>
                for removeBR in chromosomeData[0].findAll('br'):
                    removeBR.extract()

                # get chromosome and position info
                chromosome = chromosomeData[0].find_all('dd')[2]

                if (self.Chr and self.Pos) is not None:
                    # extract by GRCh; whether 37 or 38
                    resultDict[SNP_name] = self.GRCh
                elif self.SNP is not None:
                    chrPos = list(filter(lambda x: re.match(GRChRX, x), chromosome.contents))[0].split('\n')
                    resultDict[SNP_name] = chrPos[0].split(':') + chrPos

                success = True

            except requests.RequestException:
                if attemptsRemaining == 0:
                    raise noSNP("No SNP data found for " + url)

        return resultDict


    def crawlingFromFile(self) -> dict:
        resultDict = dict()
        newList = list()
        try:
            print("*********Reading file from " + self.fileName + "*********\n")
            inputFile = open(self.fileName, 'r')
            header = inputFile.readline().strip().split(self.sep)

            if (self.Chr and self.Pos is not None):
                Chr_index = header.index(self.Chr)
                Pos_index = header.index(self.Pos)
            elif self.SNP is not None:
                SNP_index = header.index(self.SNP)
            lines = inputFile.readlines()

            # Append column name in the result dictionary
            if (self.Chr and self.Pos is not None):
                header.append('SNP')
            elif self.SNP is not None:
                header.append('chromosome')
                header.append('position')
                header.append('chr_pos')
            header.append('GRChEncode')
            resultDict['Column'] = header

            for line in lines:
                line = line.strip().split(self.sep)
                if (self.Chr and self.Pos is not None):
                    url = "https://www.ncbi.nlm.nih.gov/snp/?term=" + line[Chr_index] +"%3A" + line[Pos_index]
                    SNPDict = self.getDataFromDBSNP(url=url)
                    for key, value in SNPDict.items():
                        print("Working on Chromosome:" + line[Chr_index] + " and Position:" + line[Pos_index])
                        temp = []
                        temp.extend([key, value])
                        #temp += line[Chr_index] + line[Pos_index]
                        newList.append(line+temp)
                elif self.SNP is not None:
                    url = "https://www.ncbi.nlm.nih.gov/snp/?term=" + line[SNP_index]
                    SNPDict = self.getDataFromDBSNP(url=url)
                    for key, value in SNPDict.items():
                        print('Working on ' + key)
                        if line[SNP_index] != key:
                            print('The SNP id is not found in the SNP Dictionary')
                            continue
                        newList.append(line + value)

            resultDict['resultList'] = newList

        except FileNotFoundError:
            print("Unable to open" + self.fileName)
        finally:
            print("*********Finished " + self.fileName + "*******")
        return resultDict



    def saveResult(self, outDir: str = None):
        resultDict = self.crawlingFromFile()

        fileWithoutExt = os.path.splitext(self.fileName)[0]
        dbSNP = open(f'{outDir}/dbSNP_{self.GRCh}_{fileWithoutExt}.txt', 'w')

        print('\t'.join(resultDict['Column']), file=dbSNP)
        print('\n'.join(map('\t'.join, resultDict['resultList'])), file=dbSNP)

        dbSNP.close()

if __name__ == "__main__":
    os.chdir("D:/A_SAUVER/PhD/Hormones and Reproductive factors/Summary Statistics")

    # Get Chromosome and Position based on SNP
    test = Crawling(fileName='menopause_menarche.txt', SNP='SNP', GRCh='GRCh37', sep='\t')
    test.saveResult(outDir=os.getcwd())

    # Get SNP id based on Chromosome and Position
    #test = Crawling(fileName='ChrPos_test100.txt', Chr='Chromosome', Pos='Position', GRCh='GRCh37', sep='\t')
    #test.saveResult(outDir=os.getcwd())



