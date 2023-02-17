import os
from crawling import *
from selenium import webdriver
import pandas as pd


def loadProxy(SNP, top=10):
    browser = webdriver.Chrome()
    url = 'https://ldlink.nci.nih.gov/?var=' + SNP + '&pop=CEU%2BTSI%2BFIN%2BGBR%2BIBS&genome_build=grch37&r2_d=r2&window=500000&collapseTranscript=true&annotate=forge&tab=ldproxy'
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    a = soup.find('a', attrs={"id": "ldproxy-results-link"})
    tempUrl = 'https://ldlink.nci.nih.gov/' + a.get('href')
    success = False
    print('calculating proxy SNP for ' + SNP + '.....')
    while not success:
        try:
            bsData = getHTMLAsBeautifulSoup(tempUrl)
        except:
            continue
        success = True

    proxyList = bsData.contents[0].split('\n')[1:top + 1]
    return proxyList


class Proxy:
    def __init__(self, SNP_fileName, outcomeGWAS_fileName, top=10):
        self.SNP_fileName = SNP_fileName
        self.outcomeGWAS_fileName = outcomeGWAS_fileName
        self.top = top

    def checkWithOutcome(self):
        SNP_File = open(SNP_fileName, 'r')
        outcomeGWAS = pd.read_csv(outcomeGWAS_fileName, sep='\t')
        res = []
        for SNP in SNP_File.readlines():
            SNP = SNP.strip()
            print("********** Working on " + SNP + " **********")
            proxyList = loadProxy(SNP=SNP, top=self.top)
            for proxy in proxyList:
                ind = proxy.strip().split('\t')
                Proxy_SNP = ind[0]
                chr = ind[1].split(':')[0][3:5]
                pos = ind[1].split(':')[1]
                MAF = float(ind[3])
                Dprime = ind[5]
                R2 = ind[6]
                EA = ind[2].split('/')[0][1:]
                OA = ind[2].split('/')[1][0]
                if (MAF >= 0.42):
                    continue
                exist = outcomeGWAS.loc[(outcomeGWAS['chromosome'] == int(chr)) & (outcomeGWAS['position'] == int(pos))]
                if len(exist) == 0:
                    continue
                else:
                    res.append([SNP, Proxy_SNP, chr, pos, EA, OA, Dprime, R2])
                    break
        print('Finished!!')
        return res

    def saveResult(self, outDir):
        res = self.checkWithOutcome()
        fileWithoutExt = os.path.splitext(self.SNP_fileName)[0]
        ProxySNP = open(f'{outDir}/ProxySNP_{fileWithoutExt}.txt', 'w')
        ProxySNP.writelines('\t'.join(['SNP', 'ProxySNP', 'Chromosome', 'Position', 'EA', 'OA', 'DPrime', 'R2']) + '\n')

        ProxySNP.writelines('\t'.join(i) + '\n' for i in res)
        ProxySNP.close()


if __name__ == "__main__":
    os.chdir("D:/A_SAUVER/python_project/dbSNP/example/proxy")

    outcomeGWAS_fileName = 'meta_EUR_FE.out'
    SNP_fileName = 'snplist.txt'

    test = Proxy(SNP_fileName=SNP_fileName, outcomeGWAS_fileName=outcomeGWAS_fileName, top=10)
    test.saveResult(outDir=os.getcwd())

