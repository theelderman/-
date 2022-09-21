from pandarallel import pandarallel
import pandas as pd
import os
from os import path

#whatever part you want to run, this part must run before
def CIK_10num(x):
    X = str(x)
    while len(X)<10:
        X = '0'+X
    return X
def get_filename(x):
    Str = str(x)
    Str = Str[Str.index('/')+1:]
    Str = Str[Str.index('/') + 1:Str.index('.txt')].strip()
    return Str
#the function of Downloading 10K
def myfunc(x):
    X = str(x)
    try:
        from secedgar import CompanyFilings, FilingType
        my_filings = CompanyFilings(cik_lookup=X,
                                    filing_type=FilingType.FILING_10Q,
                                    user_agent='HanruiTai (565758364@qq.com)')
        my_filings.save(Storge_address)
        print(X+"successfully download")
        return("True")
    except:
        print(X + "failed download")
        return("False")#download mistake\#
#scaner_file in storge
def scaner_file(url):
    file = os.listdir(url)
    for f in file:
        real_url = path.join(url, f)
        if path.isfile(real_url):
            print(path.abspath(real_url))
            Str= str(path.abspath(real_url))
            if "._" not in Str:
                if ".txt" in Str:
                    list_url.append(Str)
            # 如果是文件，则以绝度路径的方式输出
        elif path.isdir(real_url):
            # 如果是目录，则是地柜调研自定义函数 scaner_file (url)进行多次
            scaner_file(real_url)
        else:
            print("其他情况")
            pass
        #print(real_url)
#cross check
def Cross_check(x):
    Label1 = "False"
    for item in list_url:
        if x in item:
            Label1 = "True"
            break
    return Label1
pandarallel.initialize(progress_bar=True)
#you should put master10Q.csv etc in this address
Storge_address = "/Volumes/12321/Data10Q1"


#when first run this code use this part to creat a new csv we use to download and cross check
#第一次运行的时候跑这一段获得一个新的csv专门用来下载和cross——check。
data = pd.read_csv(Storge_address+'/master10Q.csv')
data["Label"]= data['CIK'].map(lambda x: "False")
data["File_name"]=data['Name'].map(lambda x: get_filename(x))
data.to_csv(Storge_address+'master10Q_Crosscheck.csv')


#when you have 'master10Q_Crosscheck.csv' in Storge_address, run code from there to download:
data = pd.read_csv(Storge_address+'master10Q_Crosscheck.csv')
data10k = data.drop(data.index[(data['Label'] == 'True')])#delete the file we have correctly downloaded
data10k = data10k.drop_duplicates(subset=['CIK'], keep='first', inplace= False)#delete the same CIK line
data10k['10K-number'] = data10k['CIK'].map(lambda x: CIK_10num(x))#turn the length of CIK into 10 numbers


data10k["download"]=data10k['10K-number'].parallel_apply(myfunc)#download file into Storge_address
#if there is something wrong happened the row of ["download"] will be False otherwise will be true
#if wrong happened about parallel run, can use the code below run.
#data10k["download"]=data10k['10K-number'].apply(myfunc)



#below is cross check part
#storge_url-scan all the file downloaded and create a list of these.
list_url=[]
scaner_file(Storge_address)#下载好的文件储存的地方

data = pd.read_csv(Storge_address+'master10Q_Crosscheck.csv')
#if the file is in the storge address, ["Label"] will be"True". if failed ["Label"] will be"False"
data["Label"]= data['File_name'].map(lambda x: Cross_check(x))
#data["Label"] = data.apply(lambda x: Cross_check(x), axis=1)
data.to_csv(Storge_address+'master10Q_Crosscheck.csv')

number1 = len(data)
data.drop(data.index[(data['Label'] == 'True')],inplace = True)
number2 = len(data)
print("the number of the file we want to download is "+ str(number1)+
      " and the number of the file we actually do not download is "+ str(number2))