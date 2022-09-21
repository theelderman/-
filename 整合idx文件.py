
import pandas as pd
import os
from os import path

def scaner_file(url):
    file = os.listdir(url)
    for f in file:
        real_url = path.join(url, f)
        if path.isfile(real_url):
            print(path.abspath(real_url))
            Str= str(path.abspath(real_url))
            if "._" not in Str:
                list_url.append(Str)
            # 如果是文件，则以绝度路径的方式输出
        elif path.isdir(real_url):
            # 如果是目录，则是地柜调研自定义函数 scaner_file (url)进行多次
            scaner_file(real_url)
        else:
            print("其他情况")
            pass
        #print(real_url)


#scan all the file download

#storge_url
list_url=[]
scaner_file("/Volumes/12321/Data10K/company_name")#下载好的文件储存的地方.idx




df = pd.DataFrame()
for item in list_url:
    df_small = pd.read_csv(item, sep=r"edgar/data", skiprows=10, header=None, engine="python",encoding_errors='ignore')
    df_small.columns=['All','Name']
    df_small['Form'] = df_small['All'].map(lambda x: str(x)[-36:-24].strip())
    df_small['CIK'] = df_small['All'].map(lambda x: str(x)[-24:-12].strip())
    df_small['Filed_Time'] = df_small['All'].map(lambda x: str(x)[-12:-1].strip())
    df = pd.concat([df_small, df], axis=0, ignore_index=False)
    print(item+" complete")

df = df.reset_index()


df_10k = df[(df['Form'] == '10-K')]
df_10Q = df[(df['Form'] == '10-Q')]
df_8K = df[(df['Form'] == '8-K')]


df_8K.to_csv('/Volumes/12321/Data10K/master8K.csv',sep=',')
