from django.db import models
from django.template.defaultfilters import slugify
from users.models import Profile
# Create your models here.
class Grade(models.Model):
    name = models.CharField(max_length=75,unique=True)
    slug = models.SlugField(null=True,blank=True)
    description = models.TextField(max_length=500,blank=True)
    def __str__(self):
        return self.name
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)
class Lesson(models.Model):
    lesson_id = models.CharField(max_length=50,unique=True)
    name = models.CharField(max_length=50,)
    slug = models.SlugField(blank=True,null=True)
    grade = models.ForeignKey(Grade,on_delete=models.CASCADE,related_name='lessons')
    image = models.ImageField(upload_to="lessons",blank=True)
    description = models.TextField(max_length=500,blank=True)
    def __str__(self):
        return self.name
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)
class Topics(models.Model):
    topic_id = models.CharField(max_length=100)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    created_by = models.ForeignKey(Profile,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,related_name='topic')
    name = models.CharField(max_length=100)
    chapter = models.PositiveSmallIntegerField(verbose_name="chapter no")
    slug = models.SlugField(blank=True,null=True)
    video = models.FileField(upload_to="topic_lesson",blank=True,null=True,verbose_name='video')
    ppt = models.FileField(upload_to="topic_lesson",blank=True,verbose_name='presentation')
    notes = models.FileField(upload_to="topic_lesson", blank=True, verbose_name='notes')
    class Meta:
        ordering=["chapter"]
    def __str__(self):
        return self.name
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

class Comment(models.Model):
    topic_name = models.ForeignKey(Topics,null=True,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=100,blank=True)
    #reply = models.ForeignKey('Comment',null=True,blank=True,on_delete=models.CASCADE,related_name='replies')
    author = models.ForeignKey(Profile,on_delete=models.CASCADE)
    body = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self,*args,**kwargs):
        self.name=slugify(f"comment by {self.author} {self.created_at}")
        super().save(*args,**kwargs)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["created_at"]

class Reply(models.Model):
    comment_name = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='replies')
    body = models.TextField(max_length=500)
    author = models.ForeignKey(Profile,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"reply to {self.comment_name.name}"
