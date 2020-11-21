from django.contrib import admin
from Eshop_Blog.models import BlogModel, LikePost, ViewPost, Comment, CommentReply, Report_All_Comment


class BlogAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'writer', 'jtimeStamp']

admin.site.register(BlogModel, BlogAdmin)
admin.site.register(LikePost)
admin.site.register(ViewPost)
admin.site.register(Comment)
admin.site.register(CommentReply)
admin.site.register(Report_All_Comment)
