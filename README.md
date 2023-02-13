# dbSNP_crawling

Created by: Seehyun Park

Creation date: 08 Feb 2023  

https://cesp.inserm.fr/en/equipe/exposome-and-heredity  


## Notes
This is **Crawling** python code to retrieve the chromosome & postioin of the SNP (rsID) from https://www.ncbi.nlm.nih.gov/ or vice versa.  

# How to use
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
It needs 4 arguments to be passed on the Crawling()
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
