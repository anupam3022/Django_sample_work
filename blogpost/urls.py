"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

app_name = 'blog'


urlpatterns = [


    path('',views.index,name ="index"),

    path('register/',views.register,name="register"),

    path('login/',views.login,name="login"),

    path("logout/", views.logout_request, name="logout"),

    path('home/search', views.search_filter,name = "search"),

    path('home/search-exact', views.search_filter_exact,name = "xyz"),

    path('home/<int:author_id>/', views.user_profile, name = "profile"),

    path('home/tag/<int:id>/',views.tag_profile,name="tagprofile"),

    path('home/',PostListView.as_view(),name="home"),

    path('<slug:slug>/',PostDetailView.as_view(),name="post-detail"),

    path('home/new/', PostCreateView.as_view(),name="post-create"),

    path('<slug:slug>/update',PostUpdateView.as_view(),name="post-update"),

    path('<slug:slug>/delete',PostDeleteView.as_view(),name="post-delete"),



]   
