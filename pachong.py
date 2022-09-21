from sec_edgar_downloader import Downloader
import pandas as pd
from pandarallel import pandarallel
import os
from os import path
from bs4 import BeautifulSoup
from selectolax.parser import HTMLParser
import re

pandarallel.initialize(progress_bar=True)
data = pd.read_csv('/Volumes/12321/Data10K1/SP100_Name.csv')

def myfunc(x):
    try:
        from sec_edgar_downloader import Downloader
        dl = Downloader("/Volumes/12321/Data10K1")  # set storage address
        dl.get("10-Q", x,amount=1)  # get the rencent 10 10-k file."10-k can be change to 10-Q etc.)
        return("True")#download correctly
    except:
        return("False")#download mistake

#data['trade_code'].apply(myfunc)

data["download"]=data['trade_code'].parallel_apply(myfunc)

Url_list = []

#scan all the file download and delete txt
def scaner_file(url):
    file = os.listdir(url)
    for f in file:
        real_url = path.join(url, f)
        if path.isfile(real_url):
            print(path.abspath(real_url))
            Str = str(path.abspath(real_url))
            if Str[-3:]=="txt":
                Url_list.append(Str)
            else:
                Str = '0'
            # 如果是文件，则以绝度路径的方式输出
        elif path.isdir(real_url):
            # 如果是目录，则是地柜调研自定义函数 scaner_file (url)进行多次
            scaner_file(real_url)
        else:
            print("其他情况")
            pass
        #print(real_url)



scaner_file("/Volumes/12321/Data10K1/sec-edgar-filings")


from selectolax.parser import HTMLParser
text = HTMLParser('/Volumes/12321/Data10K的副本/sec-edgar-filings/XOM/10-K/0000034088-13-000011/filing-details.html').text()
tree = BeautifulSoup('/Volumes/12321/Data10K的副本/sec-edgar-filings/XOM/10-K/0000034088-13-000011/filing-details.html', 'lxml')

"/Volumes/12321/Data10K/sec-edgar-filings/AAPL/10-K/0001193125-14-383437/full-submission.txt"

fp=open('/Volumes/12321/Data10K/sec-edgar-filings/AAPL/10-K/0000320193-20-000096/full-submission.txt','r'
        ,encoding='utf-8')
soup = BeautifulSoup(fp,'lxml')

soup.SEC

with open("/Volumes/12321/Data10K/sec-edgar-filings/ADBE/10-K/0000796343-21-000004/full-submission.txt",
          "r", encoding='utf-8') as f:  #打开文本
    data = f.read()   #读取文本
raw_10k = data
# Regex to find <DOCUMENT> tags
doc_start_pattern = re.compile(r'<DOCUMENT>')
doc_end_pattern = re.compile(r'</DOCUMENT>')
# Regex to find <TYPE> tag prceeding any characters, terminating at new line
type_pattern = re.compile(r'<TYPE>[^\n]+')

# Create 3 lists with the span idices for each regex

### There are many <Document> Tags in this text file, each as specific exhibit like 10-K, EX-10.17 etc
### First filter will give us document tag start <end> and document tag end's <start>
### We will use this to later grab content in between these tags
doc_start_is = [x.end() for x in doc_start_pattern.finditer(raw_10k)]
doc_end_is = [x.start() for x in doc_end_pattern.finditer(raw_10k)]

### Type filter is interesting, it looks for <TYPE> with Not flag as new line, ie terminare there, with + sign
### to look for any char afterwards until new line \n. This will give us <TYPE> followed Section Name like '10-K'
### Once we have have this, it returns String Array, below line will with find content after <TYPE> ie, '10-K'
### as section names
doc_types = [x[len('<TYPE>'):] for x in type_pattern.findall(raw_10k)]


document = {}

# Create a loop to go through each section type and save only the 10-K section in the dictionary
for doc_type, doc_start, doc_end in zip(doc_types, doc_start_is, doc_end_is):
    if doc_type == '10-K':
        document[doc_type] = raw_10k[doc_start:doc_end]

# Write the regex
regex = re.compile(r'(Item(\s*)(1A|1B|7A|7|8)\.?)|(ITEM\s(1A|1B|7A|7|8))')
regex = re.compile(r'(>Item(\s|&#160;|&nbsp;)(1A|1B|7A|7|8)\.{0,1})|(ITEM\s(1A|1B|7A|7|8))')

# Use finditer to math the regex
matches = regex.finditer(document['10-K'])

# Write a for loop to print the matches
for match in matches:
    print(match)

# Matches
matches = regex.finditer(document['10-K'])

# Create the dataframe
test_df = pd.DataFrame([(x.group(), x.start(), x.end()) for x in matches])

test_df.columns = ['item', 'start', 'end']
test_df['item'] = test_df.item.str.lower()

# Display the dataframe
test_df.head()

# Get rid of unnesesary charcters from the dataframe
test_df.replace('&#160;',' ',regex=True,inplace=True)
test_df.replace('&nbsp;',' ',regex=True,inplace=True)
test_df.replace(' ','',regex=True,inplace=True)
test_df.replace('\.','',regex=True,inplace=True)
test_df.replace('>','',regex=True,inplace=True)

# display the dataframe
test_df.head()

# Drop duplicates
pos_dat = test_df.sort_values('start', ascending=True).drop_duplicates(subset=['item'], keep='last')

# Display the dataframe
pos_dat

# Set item as the dataframe index
pos_dat.set_index('item', inplace=True)

# display the dataframe
pos_dat

# Get Item 1a
item_1a_raw = document['10-K'][pos_dat['start'].loc['item1a']:pos_dat['start'].loc['item1b']]

# Get Item 7
item_7_raw = document['10-K'][pos_dat['start'].loc['item7']:pos_dat['start'].loc['item7a']]

# Get Item 7a
item_7a_raw = document['10-K'][pos_dat['start'].loc['item7a']:pos_dat['start'].loc['item8']]

### First convert the raw text we have to exrtacted to BeautifulSoup object
item_1a_content = BeautifulSoup(item_1a_raw, 'lxml')

print(item_1a_content.get_text("\n\n")[0:1500])

#######################
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define URL for the specific 10K filing
URL_text = r'https://www.sec.gov/Archives/edgar/data/1318605/000156459020004475/0001564590-20-004475.txt'  # Tesla 10K Dec 2019

# Grab the response
response = requests.get(URL_text)

# Parse the response (the XML flag works better than HTML for 10Ks)
soup = BeautifulSoup(response.content, 'lxml')

fp=open('/Volumes/12321/Data10K/sec-edgar-filings/AAPL/10-K/0000320193-20-000096/full-submission.txt','r'
        ,encoding='utf-8')
soup = BeautifulSoup(fp,'lxml')
for filing_document in soup.find_all('document'):  # The document tags contain the various components of the total 10K filing pack

    # The 'type' tag contains the document type
    document_type = filing_document.type.find(text=True, recursive=False).strip()

    if document_type == "10-K":  # Once the 10K text body is found

        # Grab and store the 10K text body
        global TenKtext
        TenKtext = filing_document.find('text').extract().text

        # Set up the regex pattern
        matches = re.compile(r'(item\s(7[\.\s]|8[\.\s])|'
                             'discussion\sand\sanalysis\sof\s(consolidated\sfinancial|financial)\scondition|'
                             '(consolidated\sfinancial|financial)\sstatements\sand\ssupplementary\sdata)',
                             re.IGNORECASE)

        matches_array = pd.DataFrame([(match.group(), match.start()) for match in matches.finditer(TenKtext)])

        # Set columns in the dataframe
        matches_array.columns = ['SearchTerm', 'Start']

        # Get the number of rows in the dataframe
        Rows = matches_array['SearchTerm'].count()

        # Create a new column in 'matches_array' called 'Selection' and add adjacent 'SearchTerm' (i and i+1 rows) text concatenated
        count = 0  # Counter to help with row location and iteration
        while count < (Rows - 1):  # Can only iterate to the second last row
            matches_array.at[count, 'Selection'] = (matches_array.iloc[count, 0] + matches_array.iloc[
                count + 1, 0]).lower()  # Convert to lower case
            count += 1

        # Set up 'Item 7/8 Search Pattern' regex patterns
        matches_item7 = re.compile(r'(item\s7\.discussion\s[a-z]*)')
        matches_item8 = re.compile(r'(item\s8\.(consolidated\sfinancial|financial)\s[a-z]*)')

        # Lists to store the locations of Item 7/8 Search Pattern matches
        Start_Loc = []
        End_Loc = []

        # Find and store the locations of Item 7/8 Search Pattern matches
        count = 0  # Set up counter

        while count < (Rows - 1):  # Can only iterate to the second last row

            # Match Item 7 Search Pattern
            if re.match(matches_item7, matches_array.at[count, 'Selection']):
                # Column 1 = 'Start' columnn in 'matches_array'
                Start_Loc.append(matches_array.iloc[count, 1])  # Store in list => Item 7 will be the starting location (column '1' = 'Start' column)

            # Match Item 8 Search Pattern
            if re.match(matches_item8, matches_array.at[count, 'Selection']):
                End_Loc.append(matches_array.iloc[count, 1])

            count += 1

        # Extract section of text and store in 'TenKItem7'
        TenKItem7 = TenKtext[Start_Loc[1]:End_Loc[1]]

        # Clean newly extracted text
        TenKItem7 = TenKItem7.strip()  # Remove starting/ending white spaces
        TenKItem7 = TenKItem7.replace('\n', ' ')  # Replace \n (new line) with space
        TenKItem7 = TenKItem7.replace('\r', '')  # Replace \r (carriage returns-if you're on windows) with space
        TenKItem7 = TenKItem7.replace(' ', ' ')  # Replace " " (a special character for space in HTML) with space
        TenKItem7 = TenKItem7.replace(' ', ' ')  # Replace " " (a special character for space in HTML) with space
        while '  ' in TenKItem7:
            TenKItem7 = TenKItem7.replace('  ', ' ')  # Remove extra spaces

        # Print first 500 characters of newly extracted text
        print(TenKItem7[:500])



df=pd.read_csv("/Users/taihanrui/Downloads/company.txt",sep=r"\s{4,}",skiprows=10,header=None,engine="python")
