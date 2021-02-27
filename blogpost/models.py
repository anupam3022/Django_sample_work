from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save, pre_save
from django.template.defaultfilters import slugify

# Create your models here.
class Tag(models.Model):
	category_type = models.CharField(max_length = 100)

	def __str__(self):
		return self.category_type


class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	tag = models.ManyToManyField(Tag)
	slug =models.SlugField(null=False, unique=True, blank =True )

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:post-detail', kwargs={'slug': self.slug})

	# def save(self, *args, **kwargs):
	# 	if not self.slug:
	# 		self.slug = create_slug(self.title)
	# 	return super(Post, self).save(*args, **kwargs)
		
def new_slug(instance, new_slug=None, **kwargs):

	# import pdb; pdb.set_trace()
	slug = slugify(instance.title)
	class_exist = Post.objects.filter(slug = slug).exists()
	# latest_pk = 1
	if class_exist:
		latest_pk = Post.objects.latest('pk').id
		latest_pk +=1

		slug = "{}-{}".format(slug, latest_pk)
	
	instance.slug = slug

pre_save.connect(new_slug, sender = Post)

#(not working)-
# def udpate_slug(sender,**kwargs):
# 	if kwargs['created']:
# 		updateslug =Post.objects.update(slug = kwargs['instance'])

# post_save.connect(udpate_slug, sender = Post)

class UserProfile(models.Model):
	author = models.OneToOneField(User,on_delete=models.CASCADE)
	
	def __str__(self):
		return self.author.username

def CreateProfile(sender, **kwargs):
	if kwargs['created']:
		user_profile = UserProfile.objects.create(author=kwargs['instance'])

post_save.connect(CreateProfile, sender = User)

# @receiver(post_save, sender=User)    -- USING THE @receiver decorators
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
# #         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

class Comment(models.Model):
	post = models.ForeignKey(Post,on_delete =models.CASCADE)
	author = models.ForeignKey(User,on_delete = models.CASCADE)
	Pub_date = models.DateTimeField(default =timezone.now)
	contex = models.TextField()

	def __str__(self):
		return self.contex

class Text(models.Model):
	content = models.TextField()

	def __str__(self):
		return self.content

def postalert(sender,instance,**kwargs):
	alert = Text.objects.create(content='New post created {}'.format(instance.title))

post_save.connect(postalert, sender = Post)



# If you want to register the receiver function to several signals you may do it like this:
# @receiver([post_save, post_delete], sender=User)