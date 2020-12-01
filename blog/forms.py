from django import forms
from .models import Post,Donation ,Stock ,Wishlist ,Comment

# choices = Category.objects.all().values_list('name','name')

# choice_list =[]

# for item in choices:
#     choice_list.append(item)

class PostForm(forms.ModelForm):
    class Meta:
        model= Post
        fields=('title','content')

        widgets = {

            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control'})
        
        }

class Form(forms.ModelForm):
    quantity= forms.IntegerField()
    class Meta:
        model= Donation
        fields=('quantity',)

class StockForm(forms.ModelForm):
    ticker = forms.CharField()
    class Meta:
        model= Wishlist
        fields= ('ticker',)

class PortfolioForm(forms.ModelForm):
    ticker = forms.CharField()
    price= forms.IntegerField()
    quantity= forms.FloatField()
    class Meta:
        model= Stock
        fields= ('ticker','price','quantity',)
        

class CommentForm(forms.ModelForm):
    class Meta:
        model  = Comment
        fields =('body',)

        widgets= {
            'body' : forms.Textarea(attrs={'class':'form-control'}),

        }
    