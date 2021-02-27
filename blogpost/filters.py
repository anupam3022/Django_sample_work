from django.contrib.auth.models import User
from .models import Post
import django_filters

class TitleFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ['title', ]