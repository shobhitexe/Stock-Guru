# from blog.api import urls as api_url
from django.urls import path, include
from .views import (PostListView, PostDetailView, PostCreateView,PostUpdateView, PostDeleteView,AddCommentView)
from . import views

urlpatterns = [
    
    path('', views.mainhome, name='main-home'),
    path('blogs/', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('news/', views.news, name='news'),
    # path('category/<str:cats>/', CategoryView, name='category'),
    # path('donate/', views.DonateView, name='donate'),
    # path('dashboard/', views.DashboardView, name='dashboard'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('dashboard/portfolio',views.portfolio, name='portfolio'),
    path('delete/<stock_id>',views.delete,name='delete'),
    path('deletestock/<stock_id>',views.deletestock, name='deletestock'),
    path('post/<int:pk>/comment/',AddCommentView.as_view(), name='add_comment'),
    path('predict/', views.predict, name='predict'),
    path('predict/result', views.result, name='result')
    # path('api/', include(api_url)),
]