from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import pandas as pd
# Create your views here.
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
from .forms import *
from .models import *

def Flipkart(url):
   cust_name = []
   rev_date = []
   ratings = []
   rev_title = []
   rev_content = []
   for page in range(1,10):
    code = requests.get(str(url))
    
    if str(code) == "<Response [200]>":
       soup = BeautifulSoup(code.content,'html.parser')
       names = soup.find_all('p',class_='_2sc7ZR _2V5EHH')
       dates = soup.select('p._2sc7ZR')
       date=[]
       for i,j in enumerate(dates):
        if i%2!=0:
           date.append(j)
       stars = soup.find_all('div',class_='_3LWZlK _1BLPMq')
       titles = soup.select('p._2-N8zT')
       reviews = soup.find_all('div',class_='t-ZTKy')
       for i in range(len(names)):
        cust_name.append(names[i].get_text())
        rev_date.append(date[i].get_text())
        ratings.append(stars[i].get_text())
        rev_title.append(titles[i].get_text())
        rev_content.append(reviews[i].get_text().rstrip("\READ MORE"))
   str(code) == "<Response [200]>"
   print(cust_name)
   df = pd.DataFrame()
   df['Customer Name'] = cust_name
   df['Date'] = rev_date
   df['Ratings'] = ratings
   df['Review Title'] = rev_title
   df['Reviews'] = rev_content
   row,coloumn=df.shape
   l=0
   n=1602
   for i in range(0,row):
     l=l+len((df['Reviews'][i]).split(" "))
   print("Total number of words we extracted:",l)
   print("Actual number of words in reviews:",n)
   print("total accuracy:",((l/n)*100))
   print("")
   
   return df
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
def getdata(url):
    r = requests.get(url, headers=HEADERS)
    return r.text
  
    
def html_code(url):
  
    # pass the url
    # into getdata function
    htmldata = getdata(url)
    soup = BeautifulSoup(htmldata, 'html.parser')
  
    # display html code
    return (soup)
def Amazon(url):
  cust_name=[]
  rev_content=[]
  soup = html_code(url)
  data_str = ""
  for item in soup.find_all("span", class_="a-profile-name"):
    data_str = data_str + item.get_text()
    if data_str not in cust_name:
      cust_name.append(data_str)
    data_str = ""
  data_str = ""
  for item in soup.find_all("div", class_="a-row a-spacing-small review-data"):
    data_str = data_str + item.get_text()
  result = data_str.split("\n")
  for i in result:
    if i == "":
      pass
    else:
      print(i)
      rev_content.append(i)
  df = pd.DataFrame()
  print(cust_name)
  print(rev_content)
  df['Customer Name'] = cust_name
    #df['Date'] = rev_date
    #df['Ratings'] = ratings
    #df['Review Title'] = rev_title
  df['Reviews'] = rev_content
  print(df)
  return df
def polarity_scores_roberta(example):
    MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    encoded_text = tokenizer(example, return_tensors='pt')
    output = model(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    scores_dict = {
        'neg' : scores[0],
        'neu' : scores[1],
        'pos' : scores[2]
    }
    print(scores_dict)
    return scores_dict
def mod(data):
   
   row,column=data.shape
   result=[]
   for i in range(row):
    value=polarity_scores_roberta(str(data['Reviews'][i]))
    result.append(value)
   return result
def Frank(Fsen,Asen):
   n1=0
   p1=0
   n2=0
   p2=0
   for i in Fsen:
    p1=p1+i['pos']
    n1=n1+i['neg']
   for i in Asen:
    p2=p2+i['pos']
    n1=n1+i['neg']
   #pres=0
   #nres=0
   p1=p1/len(Fsen)
   n1=n1/len(Fsen)
   ffinal=p1-n1
   p2=p2/len(Asen)
   n2=n2/len(Asen)
   afinal=p2-n2
   if(ffinal>afinal):
      return ['Flipkart',ffinal,afinal]
   else:
      return ['Amazon',ffinal,afinal]
      
      
def Input(request):
    return render(request,'index.html')

def ranking(request):
    Alink= request.GET['Aurl']
    Flink= request.GET['Furl']
    print(Alink)
    print(Flink)
    Fdf=Flipkart(Flink)
    print(Fdf)
    Adf=Amazon(Alink)
    Fsen=mod(Fdf)
    Asen=mod(Adf)
    res,ffinal,afinal=Frank(Fsen,Asen)
    if(res=='Flipkart'):
       return render(request,'flipkart.html',{'link':Flink,'fscore':ffinal,'Ascore':afinal})
    else:
       return render(request,'amazon.html',{'link':Alink,'fscore':ffinal,'Ascore':afinal})


