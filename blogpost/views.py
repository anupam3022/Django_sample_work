from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login as auth_login
from django.http import HttpResponse
from django.contrib.auth.models import User
from .filters import TitleFilter
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Post,Comment,Tag,UserProfile
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from blogpost.forms import UserCreateForm
from django.contrib import messages 
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView
# Create your views here.

def index(request):
	return render(request,'blog/index.html')

def register(request):

    if request.method == 'POST':
        #import pdb;pdb.set_trace()
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            messages.success(request, "user registration succesfull")
            # login(request)
            return redirect('blog:home')
        else:
            print(form.errors)      
            return render(request,'blog/register.html',{'form' : form})
    else:            
        form = UserCreateForm()
        return render(request,'blog/register.html',{'form' : form})
        
def login(request):
    
    #import pdb;pdb.set_trace()
    if request.method == 'POST':
        form = AuthenticationForm(request,request.POST)
       
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            messages.success(request,"Welcome {}".format(username))
            return redirect("blog:home")
            
        else:
            messages.error(request,"Invalid username or password")
            return render(request,'blog/login.html',{'form' : form})
    else:
        form =AuthenticationForm()
        return render(request,'blog/login.html',{'form' : form})
	

def logout_request(request):
    logout(request)
    messages.info(request,"succesfully Logged OUT !!!!!!!")
    return redirect("blog:index")

def home(request):
    post = Post.objects.order_by('-date_posted')
    return render(request,'blog/home.html',{'Post':post})

def user_profile(request,author_id):
    #import pdb;pdb.set_trace()
    author = User.objects.get(id = author_id)
    post = Post.objects.filter(author__id = author_id )
    return render(request, 'blog/user_profile.html',{'Post':post, 'author':author})

def tag_profile(request,id):

    #import pdb;pdb.set_trace()
    instance = get_object_or_404(Tag, id=id)
    #tag = Tag.objects.get(id = tag_id)
    ins = instance.post_set.all()
    context = {"instance": ins}
    return render(request,'blog/tag_profile.html',context)


def search_filter(request):

    search = Post.objects.all()
    # import pdb;pdb.set_trace()
    title_contains_query = request.POST.get('title_contains')

    if title_contains_query != " " and title_contains_query is not None:
        search = search.filter(title__contains = title_contains_query)

    return render(request,'blog/search.html',{'Search':search, 'title':'Search by contains filter'})


def search_filter_exact(request):
    # import pdb;pdb.set_trace()
    search = Post.objects.all()
    import pdb;pdb.set_trace()
    title_contains_query = request.POST.get('title_contains')

    if title_contains_query != " " and title_contains_query is not None:
        search = search.filter(title__iexact = title_contains_query)

    return render(request,'blog/search.html',{'Search':search, 'title':'Search by exact filter'})
    #search = Post.objects.filter(title__contains = 'g')
    # search = Post.objects.all()
    # title_contains_query = request.GET.get('title_contains')
    # author_contains_query = request.GET.get('author_contains')
    # tag_contains_query = request.GET.get('tag_contains')

    # if title_contains_query != " " and title_contains_query is not None:
    #     search = search.filter(title__icontains = title_contains_query)


class PostListView(ListView):
    model = Post
    template_name ="blog/home.html"  #<app>/<model>_<viewtype>.html
    context_object_name = "Post"
    ordering = ['-date_posted']   # as compared to (post = Post.objects.order_by('-date_posted')) in function view

class PostDetailView(DetailView):
    model = Post
    template_name ="blog/post_detail.html"  #<app>/<model>_<viewtype>.html
    context_object_name = "post"

class PostCreateView(CreateView):
    model = Post
    fields = ["title","content","tag"]
    template_name ="blog/post_form.html"

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    fields = ["title","content"]
    template_name ="blog/post_form.html"

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # def test_funct(self):
    #     Post = self.get_object()
    #     if self.request.user == Post.author:
    #         return True
    #     return False



class PostDeleteView(DeleteView):
    model = Post
    success_url = '/home'
    template_name ="blog/post_confirm_delete.html"