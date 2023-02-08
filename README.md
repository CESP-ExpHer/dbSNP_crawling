# dbSNP_crawling

Created by: Seehyun Park

Creation date: 08 Feb 2023  

https://cesp.inserm.fr/en/equipe/exposome-and-heredity  


## Notes
This is **Crawling** python code to extract the chromosome & postioin of the SNP (rsID) from https://www.ncbi.nlm.nih.gov/.  

### How to use
It needs 4 arguments to be passed on the Crawling()
- **fileName:** The name of the file
- **SNP:** SNP (rsID) column name of the input file.
- **GRCh:** Users can define which GRCh encoder they want to use (can be GRCh37 / GRCh38).
- **sep:** Delimiter in input file

```c
if __name__ == "__main__":
    test = Crawling(fileName='test100.txt', SNP='MarkerName', GRCh='GRCh37', sep=',')
    test.saveResult(outDir=os.getcwd())
```
