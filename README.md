# dbSNP_crawling

Created by: Seehyun Park

Creation date: 08 Feb 2023  

https://cesp.inserm.fr/en/equipe/exposome-and-heredity  


## Notes
- **crawling.py** is a python code to retrieve the chromosome & postioin of the SNP (rsID) from https://www.ncbi.nlm.nih.gov/ or vice versa.  
- **Proxy.py** is a python code to retrieve the proxy SNP of your SNP of interest from LDlink (https://ldlink.nci.nih.gov/?tab=ldproxy).

# How to use
## 1) crawling.py
### To get the chromosome and position given SNP
It needs 4 arguments to be passed on the Crawling()
- **fileName:** The name of the file
- **SNP:** SNP (rsID) column name
- **GRCh:** Users can define which GRCh encoder they want to use (can be GRCh37 / GRCh38).
- **sep:** Delimiter in input file

```c
if __name__ == "__main__":
    test = Crawling(fileName='SNP_test100.txt', SNP='MarkerName', GRCh='GRCh37', sep=',')
    test.saveResult(outDir=os.getcwd())
```

### To get the SNP given chromosome and position 
It needs 5 arguments to be passed on the Crawling()
- **fileName:** The name of the file
- **Chr:** Chromosome column name 
- **Pos:** Position column name
- **GRCh:** Users can define which GRCh encoder they want to use (can be GRCh37 / GRCh38).
- **sep:** Delimiter in input file

```c
if __name__ == "__main__":
    test = Crawling(fileName='ChrPos_test100.txt', Chr='Chromosome', Pos='Position', GRCh='GRCh37', sep='\t')
    test.saveResult(outDir=os.getcwd())
```

## 2) Proxy.py
It will extrat proxy SNPs from LDlinks that are present in both the exposure and outcome GWAS datasets.  It needs 3 arguments to be passed on the Proxy()
- **SNP_fileName:** The name of text file that contains the list of SNP.
- **exposureGWAS_fileName:** The name of exposure GWAS
- **outcomeGWAS_fileName:** The name of outcome GWAS
```c
if __name__ == "__main__":
    os.chdir("D:/A_SAUVER/python_project/dbSNP/example/proxy")

    outcomeGWAS_fileName = 'outcomeGWAS.out'
    exposureGWAS_fileName = 'dbSNP_GRCh37_menarche.txt'
    SNP_fileName = 'menarche_snplist.txt'

    test = Proxy(SNP_fileName=SNP_fileName, exposureGWAS_fileName=exposureGWAS_fileName, outcomeGWAS_fileName=outcomeGWAS_fileName)
    test.saveResult(outDir=os.getcwd())
```

### For instance
Let's say the SNPs below are not present in your outcome GWAS
```c
rs1254337
rs7258722
rs2274465
rs2836950
rs4735765
```
Then by running Proxy(), you will have the below output which are present in both exposure and outcome GWAS with D' and R2 value
```c
SNP	ProxySNP	Chromosome	Position	EA	OA	DPrime	R2
rs1254337	rs1254331	14	60916237	A	G	1.0	1.0
rs7258722	rs10221489	19	18826975	C	T	0.8649	0.5694
rs2274465	rs660899	1	44117006	G	T	1.0	0.991
rs2836950	rs2836961	21	40627020	A	C	0.9957	0.9281
rs4735765	rs4735770	8	78148158	T	C	0.9815	0.8672
```
