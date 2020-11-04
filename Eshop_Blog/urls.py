from django.urls import path

from .views import Blog_List, Blog_Details, LikeUrl, removeCMT, removeRPL, reportCMT, reportRPL

urlpatterns = [
    path('List', Blog_List.as_view()),
    path('Details/<int:BlogId>/<str:title>', Blog_Details),
    path('Like', LikeUrl, name='like'),
    path('List/comments/remove/<int:cmtId>/<int:BlogId>', removeCMT),
    path('List/comments/replies/remove/<int:cmtId>/<int:BlogId>', removeRPL),
    path('List/comments/report/<int:cmtId>/<int:BlogId>', reportCMT),
    path('List/comments/replies/report/<int:rplId>/<int:BlogId>', reportRPL),

]