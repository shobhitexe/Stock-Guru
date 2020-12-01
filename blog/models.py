from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib.request
from pprint import pprint
from html_table_parser import HTMLTableParser
import warnings
import sqlalchemy
import pymysql
import cufflinks as cf
import chart_studio.plotly as ply
import plotly.express as px
import holidays
import datetime
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
import plotly.graph_objects as go
import tensorflow
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
  

class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

class Donation(models.Model):
    receiver = models.CharField(max_length = 100)
    donor = models.CharField(max_length = 100)
    quantity = models.IntegerField(default = 1)
    category = models.CharField(max_length = 100)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.donor
    
class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 0)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return self.ticker 

class Wishlist(models.Model):
    ticker = models.CharField(max_length=10)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.ticker 

class Comment(models.Model):
    post = models.ForeignKey(Post,related_name="comments",on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s -%s' %(self.post.title,self.name)


class Predictor(models.Model):
    window=60
    def writetosql(self,stock,dataset,con):
        dataset.to_sql(stock,con,index=False,if_exists='replace')

    def readsql(self,stock,con):
        query='SELECT Date,Close FROM '+stock
        dataset=pd.read_sql(query,con)
        return dataset

    def isWeekend(self,date):
        weekno=date.weekday()
        if weekno<5:
            return False
        return True
    
    def isHoliday(self,date):
        india_holidays=holidays.India(years=datetime.datetime.now().year)
        return (date in india_holidays)

    def get_contents(self,url):
        req=urllib.request.Request(url)
        sock=urllib.request.urlopen(req)
        return sock.read()

    def get_live_data(self,stock):
        url='https://in.finance.yahoo.com/quote/' + stock + '.NS/history/'
        html=self.get_contents(url).decode('utf-8')
        parser=HTMLTableParser()
        parser.feed(html)
        livedata=pd.DataFrame(parser.tables[0],columns=parser.tables[0][0])[['Date','Close*']].rename(columns={'Close*':'Close'})
        livedata.drop(livedata.index[[0,-1]],inplace=True)
        livedata['Date']=pd.to_datetime(livedata['Date']).dt.date
        livedata=livedata.reindex(index=livedata.index[::-1])
        livedata.dropna(inplace=True)
        return livedata

    def mergedata(self,dataset,livedata):
        dataset=pd.concat([dataset,livedata]).drop_duplicates('Date',keep='last').reset_index(drop=True)
        dataset=dataset[dataset.Close!='-']
        dataset['Close']=dataset['Close'].astype(str).apply(lambda x: float(x.split()[0].replace(',','')))
        return dataset 
    
    def predict(self,dataset,stock):
        length=len(dataset.index)
        scaler=MinMaxScaler(feature_range=(0,1))
        training=pd.DataFrame(dataset['Close'])
        testing=training[-self.window:]
        testing['Scaled']=scaler.fit_transform(testing)
        testing.index=pd.to_datetime(dataset['Date'][-self.window:])
        model=load_model('blog/trainedmodels/'+stock+'.h5')
        for i in range (30):
            x_test=[]
            x_test.append(testing['Scaled'][-self.window:])
            x_test=np.array(x_test)
            x_test=np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
            scaled_pred=model.predict(x_test)
            pred=scaler.inverse_transform(scaled_pred)
            next_date=testing.index[-1]+datetime.timedelta(days=1)
            while self.isWeekend(next_date) or self.isHoliday(next_date):
                next_date+=datetime.timedelta(days=1)
            testing=testing.append(pd.Series([pred[0][0],scaled_pred[0][0]],name=next_date,index=testing.columns),ignore_index=False)
        prediction=testing[self.window:]
        prediction.drop(['Scaled'],axis=1,inplace=True)
        return prediction

    def show_prediction(self,prediction,stock):
        fig=go.Figure()
        scatter=go.Scatter(x=prediction.index,y=prediction.Close,mode='lines')
        fig.add_trace(scatter)
        fig.update_layout(title=stock+' Closing Price Prediction For The Next 30 Days',xaxis_title='Date',yaxis_title='Close')
        plot_div=plot(fig, output_type='div',include_plotlyjs=False)
        return plot_div

    def show_historic(self,dataset,stock):
        fig=go.Figure()
        scatter=go.Scatter(x=dataset.Date,y=dataset.Close,mode='lines')
        fig.add_trace(scatter)
        fig.update_layout(title=stock+' Historical Closing Price',xaxis_title='Date',yaxis_title='Close')
        plot_div=plot(fig, output_type='div',include_plotlyjs=False)
        return plot_div
    
    
