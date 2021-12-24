from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post,  Donation ,Stock ,Comment , Wishlist, Predictor
from django.views.generic import (ListView, DetailView, CreateView,UpdateView, DeleteView)
from .forms import PostForm, Form , StockForm ,PortfolioForm ,CommentForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
import sqlalchemy
import json
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent  


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def predict(request):
    return render(request, 'blog/predictor.html')

def result(request):
    stock=request.GET['Stock']
    predictor=Predictor()
    dataset=predictor.readsql(stock.title())
    dataset=predictor.get_live_data(stock,dataset)
    predicted_df=predictor.predict(dataset,stock)
    historic_plot=predictor.show_historic(dataset,stock)
    predicted_plot=predictor.show_prediction(predicted_df,stock)
    predicted_df.index=predicted_df.index.strftime('%Y-%m-%d')
    predicted_json = predicted_df.reset_index().to_json(orient ='records') 
    prediction = [] 
    prediction = json.loads(predicted_json) 
    context = {'prediction': prediction,'predicted_plot':predicted_plot,'historic_plot': historic_plot } 
    return render(request,'blog/result.html',context)

    # stock=request.GET['Stock']
    # predictor=Predictor()
    # dataset=predictor.readsql(stock.title())
    # dataset=predictor.get_live_data(stock,dataset)
    # predicted_df=predictor.predict(dataset,stock)
    # historic_plot=predictor.show_historic(dataset,stock)
    # predicted_plot=predictor.show_prediction(predicted_df,stock)
    # predicted_df.index=predicted_df.index.strftime('%Y-%m-%d')
    # predicted_json = predicted_df.reset_index().to_json(orient ='records') 
    # prediction = [] 
    # prediction = json.loads(predicted_json) 
    # context = {'prediction': prediction,'predicted_plot':predicted_plot,'historic_plot': historic_plot } 
    # return render(request,'blog/result.html',context)



# def DonateView(request):
#     if request.method == 'POST':
#         form = Form(request.POST)
#         if form.is_valid():
#             form.save()
#             model = Donation()
#             model.donor = self.request.user
#             messages.success(request, f'Thankyou!')
#             return redirect('dashboard')
#     else:
#         form = Form()
#     return render(request, 'blog/donate.html', {'form': form})

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post

# class PostDetailView(DetailView):
#     # form = ""
#     # if request.method== 'POST':
#     #     form=Form(request.POST)
#     #     if form.is_valid():
#     #         print(type(request.user))
#     #         form.save()
#     #         donation =Donation()
#     #         post = get_object_or_404(Post, pk=pk)
#     #         qty=form.cleaned_data.get('quantity')
#     #         donation.quantity=qty
#     #         donation.receiver= post.author
#     #         donation.donor= request.user
#     #         donation.category= post.category
#     #         donation.save()
#     #         send_mail('Corona Rangers has some great news for you',f' {donation.donor} ({request.user.email}) wants to donate  {qty} { donation.category}',settings.EMAIL_HOST_USER,[f'{post.author.email}'],fail_silently=False)
#     #         messages.success(request, f'We have notified the NGO, thankyou for the donation.The NGO will contact you')
#     #         return redirect('dashboard')
#     #     else:
#     #         pass
#     # else:
#     #     form=Form()
#     #     context = {
#     #         "form": form,
#     #         "post": get_object_or_404(Post, pk=pk),
#     #     }
#     #     return render(request,'blog/post_detail.html',{
#     #             "form": form,
#     #             "post": get_object_or_404(Post, pk=pk),
#     #         })
#     model: Post
 

def DashboardView(request):
    donations = Donation.objects.filter(donor=request.user)
    recieved = Donation.objects.filter(receiver=request.user)
    context = {
        'donations': donations,
        'recieved': recieved
    }
    return render(request, 'blog/dashboard.html', context)
    
# class DonateView(DetailView):
#     model=Donation
#     form_class = Form
#     template_name = 'blog/donate.html'

#     def form_valid(self, form):
#         form.instance.donor = self.request.user
#         return super().form_valid(form)


# def Donate(request,pk):
#     if request.method== 'POST':
#         forms=Form(request.POST)
#         if form.is_valid():
#             user=form.save()
#             donation =Donation()
#             post =Post()
#             qty=form.clean_data.get('quantity')
#             donation.quantity=qty
#             donation.receiver= post.author
#             donation.donor= self.request.user
#             donation.categories= post.categories
#             donation.save()
#             messages.success(request, f'Thankyou for donating!')
#             return redirect('dashboard')
#     else:
#         form=Form()
#         post = Post.objects.filter(id=pk)
#         context = {
#             "form": form,
#             "post": post
#         }
#     return render(request,'blog/post_detail.html',context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# class AddCategoryView(CreateView):
#     model = Post
#     template_name = 'blog/add_category.html'
#     fields = '__all__'

# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = Post
#     fields = ['title', 'content','category']

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blogs/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'posts': Post.objects.all()})
    
def mainhome(request):
    return render(request, 'blog/index.html')

def news(request):
    return render(request, 'blog/news.html')

# def CategoryView(request, cats):
#     category_posts = Post.objects.filter(category=cats)
#     return render(request, 'blog/categories.html', {'cats': cats, 'category_posts': category_posts})

def dashboard(request):
    import requests
    import json

    if request.method == 'POST':
        form =StockForm(request.POST or None)

        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            messages.success(request,("Stock has been Added!"))
            return redirect('dashboard')
        else:
            pass  
    else:  
        ticker =Wishlist.objects.filter(owner=request.user)
        ticker1 =Stock.objects.filter(owner=request.user)
        out =[]
        output =[]
        form =StockForm()
        
        # pform = PortfolioForm()

        for ticker_item in ticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_873df7d7e66c4c1fac2b36e03ab53d51")
            try:
                api =json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."
        # print(output)
        for ticker_item in ticker1:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_873df7d7e66c4c1fac2b36e03ab53d51")
            try:
                api =json.loads(api_request.content) 
                out.append(api)
                # print(output)
            except Exception as e:
                api = "Error..."
        
        return render(request, 'blog/dashboard.html',{'form':form,'ticker':ticker,'output': output,'out':out,'ticker1':ticker1})
# def dashboard(request):
#     import requests
#     import json

#     if request.method == 'POST':
#         form =StockForm(request.POST or None)

#         if form.is_valid():
#             form.instance.owner = request.user
#             form.save()
#             messages.success(request,("Stock has been Added!"))
#             return redirect('dashboard')
        
#     else:  
#         ticker =Stock.objects.filter(owner=request.user)
#         output =[]
#         for ticker_item in ticker:
#             api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_873df7d7e66c4c1fac2b36e03ab53d51")

#             try:
#                 api =json.loads(api_request.content)
#                 output.append(api)
#             except Exception as e:
#                 api = "Error..."
#         return render(request, 'blog/dashboard.html',{'ticker':ticker,'output': output})

# def dashboard(request):
#     import requests
#     import json

#     if request.method == 'POST':
#         form =StockForm(request.POST or None)

#         if form.is_valid():
#             form.instance.owner = request.user
#             form.save()
#             messages.success(request,("Stock has been Added!"))
#             return redirect('dashboard')
        
#     else:  
#         ticker =Wishlist.objects.filter(owner=request.user)
#         output =[]
#         for ticker_item in ticker:
#             api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_873df7d7e66c4c1fac2b36e03ab53d51")

#             try:
#                 print(api_request.content)
#                 api =json.loads(api_request.content)
#                 output.append(api)
#             except Exception as e:
#                 api = "Error..."
#         return render(request, 'blog/dashboard.html',{'ticker':ticker,'output': output})

def portfolio(request):
    import requests
    import json

    if request.method == 'POST':
        form =PortfolioForm(request.POST or None)

        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            # ticker=form.cleaned_data.get('ticker')
            # price=form.cleaned_data.get('price')
            # quantity=form.cleaned_data.get('quantity')
            # print(quantity)
            # stock = Stock()
            # stock.save()
            messages.success(request,("Stock has been Added!"))
            return redirect('portfolio')
        
    else:  
        ticker =Stock.objects.filter(owner=request.user)
        out =[]
        pform =PortfolioForm()
        for ticker_item in ticker:
            
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_873df7d7e66c4c1fac2b36e03ab53d51")

            try:
                api =json.loads(api_request.content)
                out.append(api)
            except Exception as e:
                api = "Error..."
       
        return render(request, 'blog/portfolio.html',{'pform':pform,'ticker':ticker,'out': out})



def delete(request, stock_id):
    item= Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request,("Stock has been deleted"))
    return redirect(dashboard)

def deletestock(request, stock_id):
    item= Wishlist.objects.get(pk=stock_id)
    item.delete()
    messages.success(request,("Stock has been deleted"))
    return redirect(dashboard)



class AddCommentView(CreateView):
    model = Comment
    form_class =CommentForm
    template_name= 'blog/add_comment.html'
    # fields ='__all__'
    def form_valid(self,form):
        form.instance.name =self.request.user
        form.instance.post_id=self.kwargs['pk']
        return super().form_valid(form)

    success_url =reverse_lazy('blog-home')