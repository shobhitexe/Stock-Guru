from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cufflinks as cf
import chart_studio.plotly as ply
import plotly.express as px
import holidays
import datetime
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import yfinance as yf
from django.apps import apps
from django_start.base_settings import BASE_DIR
import os

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

    def writetosql(self,stock,dataset):
        model = apps.get_model('blog', stock)
        row_iter = dataset.iterrows()
        objs = [model(close = row['Close'],date  = row['Date'])
        for index, row in row_iter]
        model.objects.bulk_create(objs)

    def readsql(self,stock):
        model = apps.get_model('blog', stock)
        dataset = pd.DataFrame(list(model.objects.all().values()))
        return dataset

    def isWeekend(self,date):
        weekno=date.weekday()
        if weekno<5:
            return False
        return True
    
    def isHoliday(self,date):
        india_holidays=holidays.India(years=datetime.datetime.now().year)
        return (date in india_holidays)

    def get_live_data(self,stock,dataset):
        if dataset.empty or dataset['date'][len(dataset)-1] < datetime.date.today():
            start = None 
            end = datetime.date.today()
            if dataset.empty:
                start = datetime.date(2000,1,1)
            else:
                start=dataset['date'][len(dataset)-1] + datetime.timedelta(days=1)
            try:
                newdf = yf.download(stock+'.NS',start,end)
                newdf = newdf[['Close']]
                newdf['Date']= newdf.index
                newdf.dropna(inplace=True)
                newdf.drop_duplicates(subset=['Date'], keep='last',inplace=True)
                self.writetosql(stock.title(),newdf)
            except:
                pass
        return self.readsql(stock.title())
    
    def predict(self,dataset,stock):
        scaler=MinMaxScaler(feature_range=(0,1))
        training=pd.DataFrame(dataset['close'])
        testing=training[-self.window:]
        testing['Scaled']=scaler.fit_transform(testing)
        testing.index=pd.to_datetime(dataset['date'][-self.window:])
        model_path = os.path.join(BASE_DIR,'blog','trainedmodels',stock+'.h5')
        model=load_model(model_path)
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
        scatter=go.Scatter(x=prediction.index,y=prediction.close,mode='lines')
        fig.add_trace(scatter)
        fig.update_layout(title=stock+' Closing Price Prediction For The Next 30 Days',xaxis_title='Date',yaxis_title='Close')
        plot_div=plot(fig, output_type='div',include_plotlyjs=False)
        return plot_div

    def show_historic(self,dataset,stock):
        fig=go.Figure()
        scatter=go.Scatter(x=dataset.date,y=dataset.close,mode='lines')
        fig.add_trace(scatter)
        fig.update_layout(title=stock+' Historical Closing Price',xaxis_title='Date',yaxis_title='Close')
        plot_div=plot(fig, output_type='div',include_plotlyjs=False)
        return plot_div
    
    

class Adaniports(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='adaniports'


class Asianpaint(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        verbose_name_plural ='asianpaint'


class Axisbank(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='axisbank'


class Bajajfinsv(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='bajajfinsv'


class Bajfinance(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='bajfinance'


class Bhartiartl(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='bhartiartl'


class Bpcl(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='bpcl'


class Britannia(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='britannia'


class Cipla(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='cipla'


class Coalindia(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='coalindia'


class Drreddy(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='drreddy'


class Eichermot(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='eichermot'


class Gail(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='gail'


class Grasim(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='grasim'


class Hcltech(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='hcltech'


class Hdfc(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='hdfc'


class Hdfcbank(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='hdfcbank'


class Heromotoco(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='heromotoco'


class Hindalco(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='hindalco'


class Hindunilvr(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='hindunilvr'


class Icicibank(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='icicibank'


class Indusindbk(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='indusindbk'


class Infratel(models.Model):
    close = models.TextField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.TextField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='infratel'


class Infy(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='infy'


class Ioc(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='ioc'


class Itc(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='itc'


class Jswsteel(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='jswsteel'


class Kotakbank(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='kotakbank'


class Lt(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='lt'


class MM(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='m&m'


class Maruti(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='maruti'


class Nestleind(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='nestleind'


class Ntpc(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='ntpc'


class Ongc(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='ongc'


class Powergrid(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='powergrid'


class Reliance(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='reliance'


class Sbin(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='sbin'


class Shreecem(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='shreecem'


class Sunpharma(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='sunpharma'


class Tatamotors(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='tatamotors'


class Tatasteel(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='tatasteel'


class Tcs(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='tcs'


class Techm(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='techm'


class Titan(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='titan'


class Ultracemco(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='ultracemco'


class Upl(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='upl'


class Vedl(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='vedl'


class Wipro(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='wipro'


class Zeel(models.Model):
    close = models.FloatField(db_column='Close', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=False, null=False, primary_key = True)  # Field name made lowercase.

    class Meta:
        managed = True
        verbose_name_plural ='zeel'
