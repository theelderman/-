# -
这是一个自然语言处理分析公司金融风险的项目 还在ing
主要包括 sec 原始数据下载 数据清洗 以及项目提取 和分析

#step 1 creat master file from sec
in this step we first download the data to creat the completely master file.
The data we download is from SEC web to get all the contains of the filling after 1993. The link is https://www.sec.gov/Archives/edgar/full-index/
we storge this data in the "sJ:\Projects\Company_textual_analysis\step 1 creat master file from sec\data". all are idx file
in the step 1 code
1.scaner_file. scan all the idx file in the "step 1...\\ data" and creat a list. upload the idx data one file by one file
2.in each idx file. get the "Form" "CIK""filed_time" variables
3. output the compiled data frame to "step 1...\\data" the name is master.csv
4. sperately select the 10-K 10-Q 8-K in the variable "Form" and output the master10K.csv master10Q.csv and master8k.csv in "step 1...\\data"


#step 1.1 get map data from api
in this step we need to get all the map data from map api
in map api we need to give api a cik and it will response the related data with this api. In this CIK api require parameters, it will response all the CIK
data contains the number you give.(e.g if you write CIK:"1", it will respon all the CIK that have "1" such as 1000,10235 and so on)
I just run a loop to search for the numver 0 to 9, combine all the data and delete the same CIKs and only keep unique CIKs.
Take tesla as example, map api give such information
        "name": "Tesla Inc",
        "ticker": "TSLA",
        "cik": "1318605",
        "cusip": "88160R101",
        "exchange": "NASDAQ",
        "isDelisted": false,
        "category": "Domestic Common Stock",
        "sector": "Consumer Cyclical",
        "industry": "Auto Manufacturers",
        "sic": "3711",
        "sicSector": "Manufacturing",
        "sicIndustry": "Motor Vehicles & Passenger Car Bodies",
        "famaSector": "",
        "famaIndustry": "Automobiles and Trucks",
        "currency": "USD",
        "location": "California; U.S.A",
        "id": "e27d6e9606f216c569e46abf407685f3"
Output the csv file to the J:\Projects\Company_textual_analysis\step 1.1 get map data from api\data

#step 1.2 get Executive Compensation Data and #step 1.3 get insider trade data
these two are run in same logic
these two api are requested by company ticker. Use the data from step1.1 "step 1.1....\data" to get the list of the CIK.
request the api one ticker by one ticker and combine all these requests
output the file to the sperately \data forders.


#step 2 creat url  file from master file
in this step we need to get urls information and other information from Query API. take 10k as example and the same to 10q and 8k
1.load the master file from step 1's data(master10K.csv).
2.do dupiluate to keep the only unique CIK.
3.Use the CIK to download urls data an combine all these url data. in this step as the api's instruction said, the response can only give 200 urls
at one request. So write a loop to get all the url data to one CIK.
for Num in range(0,9800,200):
    query = {
          "query": {
           "query_string": {
           "query": query1
           }
           },
           "from": Num,
           }
    response = queryApi.get_filings(query)#get url data
    if len(response["filings"])==0:
    break
 4. output the combined data to "J:\Projects\Company_textual_analysis\step 2 creat url  file from master file\data" as master10K_url.csv
     
 
 #step 3 get item from url file
 in this step we use extractor api to get the items. also take 10K as example same to 10Q and 8K
 1.def function.
 we first define two function. one is "extract_items_10k"(get txt of item) the other is "extract_items_10k_html"(get html of item).
 in the function, we give a url address and items name, it will return the  data to this url 's specific item.
 And when considering the request false happenning. in the function it will request up to 50 times until get the data, this avoid the request problem as
 much as possible.
 
 def extract_items_10k_html(filing_url,ITEM):
     item = ITEM
     section_text = "false"
     while section_text == "false":
          n = 0
          try:
              section_text = extractorApi.get_section(filing_url=filing_url,section=item,return_type="html")
          except:
              section_text = "false"
          n = n + 1
          if n > 50:  # in case the death loop, if run 50 times just break
          break
      return (section_text)
2.upload the master10K_url.csv. up load the file in "step 2...\data". we get the data one item by item for all the urls(e.g first item 1 and the 
item 1a .....). 
3.use the url of html version to get the txt item(first use txt url version is also ok). and then use the url of html version to get the html item
it will be blank in the dataframe cell if successfully request but response nothing. We select the rows have these blank item. In the next we 
use the url of txt version(or use the html url version) to this blank cell.
4.double check download "false". If there are still "false"in the item columns, select these rows and output the data in "step 3...\\data" name is
"flase_apiitem xx.csv" if download 50times still false we can check later in people.
5.double duplicate. use year cik and url address to double check the duplicate in case for the same rows.
6. output the file to "step 3....\\data" name is "apiitem xx.csv"









