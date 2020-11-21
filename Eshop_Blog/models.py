from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from Extentions.utils import jalali_convertor

class BlogManager(models.Manager):
    def get_active_Blog(self):
        return self.get_queryset().filter(active=True).order_by('-id')

def get_filename_ext_rand(filepath):
    import os
    from random import randint
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    random_id = randint(1000, 9999)
    return name, ext, random_id

def upload_image_path(instance, filename):
    name, ext, rand = get_filename_ext_rand(filename)
    final_name = f"{name}-{rand}{ext}"
    return f"blog-img/{final_name}"

class BlogModel(models.Model):
    title = models.CharField(max_length=120, verbose_name='عنوان')
    image = models.ImageField(upload_to=upload_image_path, verbose_name='تصویر پست', blank=True, null=True)
    writer = models.CharField(max_length=50, verbose_name='نویسنده')
    description = RichTextField(verbose_name='متن پست')
    timeStamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False, verbose_name='فعال / روح')

    objects = BlogManager()

    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return f'/Blog/Details/{self.id}/{self.title.replace(" ","-")}'

    def jtimeStamp(self):
        return jalali_convertor(self.timeStamp)

    def has_next(self):
        Blog_id = self.id
        Blog_id += 1
        exist: BlogModel = BlogModel.objects.filter(id=Blog_id).first()
        if exist is not None:
            return 'not'

    def has_prev(self):
        Blog_id = self.id
        Blog_id -= 1
        exist: BlogModel = BlogModel.objects.filter(id=Blog_id).first()
        if exist is not None:
            return 'not'

    def next_Blog(self):
        Blog_id = self.id
        Blog_id += 1
        exist: BlogModel = BlogModel.objects.filter(id=Blog_id).first()
        if exist is not None:
            return f'/Blog/Details/{exist.id}/{exist.title.replace(" ","-")}'

    def previous_Blog(self):
        Blog_id = self.id
        Blog_id -= 1
        exist: BlogModel = BlogModel.objects.filter(id=Blog_id).first()
        if exist is not None:
            return f'/Blog/Details/{exist.id}/{exist.title.replace(" ","-")}'

    def ViewPost(self):
        return ViewPost.objects.filter(blog_id=self.id).all().count()

    def LikePost(self):
        return LikePost.objects.filter(blog_id=self.id).all().count()

    def commentPost(self):
        cmt = Comment.objects.filter(post_id=self.id).all().count()
        return cmt

class LikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', blank=True, null=True)
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE, verbose_name='پست', blank=True, null=True)

    class Meta:
        verbose_name='لایک پست'
        verbose_name_plural='لایک پست ها'

    def __str__(self):
        return f'{self.user} - {self.blog}'

class ViewPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', blank=True, null=True)
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE, verbose_name='پست', blank=True, null=True)

    class Meta:
        verbose_name = 'بازدید پست'
        verbose_name_plural = 'بازدید پست ها'

    def __str__(self):
        return f'{self.user} - {self.blog}'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='کاربر')
    post = models.ForeignKey(BlogModel, on_delete=models.CASCADE, blank=True, null=True, verbose_name='پست')
    msg = RichTextField(verbose_name='پیام')
    timeStamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'کامنت پست'
        verbose_name_plural = 'کامنت پست ها'

    def __str__(self):
        return f'{self.user.username} - {self.post.title} - {self.timeStamp}'

    def get_replies(self):
        return self.commentreply_set.all()

class CommentReply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='کامنت')
    msg = RichTextField(verbose_name='پیام')
    timeStamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'ریپلای کامنت پست'
        verbose_name_plural = 'ریپلای کامنت پست ها'

    def __str__(self):
        return f'{self.user.username} - {self.comment.post.title} - {self.timeStamp}'

class Report_All_Comment(models.Model):
    comment = models.ForeignKey(Comment, blank=True, null=True, verbose_name='کامنت', on_delete=models.CASCADE)
    reply = models.ForeignKey(CommentReply, blank=True, null=True, verbose_name='ریپلای', on_delete=models.CASCADE)
    userReporter = models.ForeignKey(User, verbose_name='کاربر گزارش دهنده', on_delete=models.CASCADE)
    timeStamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'گزارش پیام'
        verbose_name_plural = 'گزارش های پیام ها'

    def __str__(self):
        return f'CMT: {self.comment} * RPL:{self.reply} * user:{self.userReporter} * time:{self.timeStamp}'