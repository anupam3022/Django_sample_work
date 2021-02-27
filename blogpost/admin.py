from django.contrib import admin
from .models import Post,Comment,Tag,UserProfile,Text
# Register your models here.


class PostAdmin(admin.ModelAdmin):
	list_display =('title','date_posted','author')
	# prepopulated_fields = {'slug': ('title',)}
		


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(UserProfile)
admin.site.register(Text)