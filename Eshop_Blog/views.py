from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView
from .forms import msgForm
from .models import BlogModel, LikePost, ViewPost, Comment, CommentReply, Report_All_Comment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

class Blog_List(ListView):
    template_name = 'bloglist.html'
    paginate_by = 6
    def get_queryset(self):
        return BlogModel.objects.get_active_Blog()

def Blog_Details(request, *args, **kwargs):
    BlogId = kwargs.get('BlogId')
    selected_blog: BlogModel = BlogModel.objects.get(id=BlogId)

    if request.POST:
        if not request.user.is_authenticated:
            messages.info(request, 'برای ارسال دیدگاه باید به سیستم وارد شوید.')
            return redirect(selected_blog.get_absolute_url())
        form = msgForm(request.POST)
        if form.is_valid():
            post_item = form.save(commit=False)
            post_item.save()
            mtCMTT: Comment = Comment.objects.filter(msg__iexact=form.cleaned_data.get('msg')).first()
            mtCMTT.user_id = request.user.id
            mtCMTT.post_id = BlogId
            mtCMTT.save()
            messages.info(request, 'پیام شما ارسال شد.')
    else:
        form = msgForm()

    # Likes
    likes = LikePost.objects.filter(blog_id=BlogId).count()
    # like Image
    bol = LikePost.objects.filter(blog_id=BlogId, user_id=request.user.id).first()

    # Views Post
    if request.user.is_authenticated:
        ExistBlog = ViewPost.objects.filter(user_id=request.user.id, blog_id=BlogId).first()
        if ExistBlog is None:
            selected_blog.viewpost_set.create(user_id=request.user.id)

    # pass View counter
    views = ViewPost.objects.filter(blog_id=BlogId).count()

    # send Comment
    if request.POST:
        if not request.user.is_authenticated:
            messages.info(request, 'برای ارسال دیدگاه باید به سیستم وارد شوید.')
            return redirect('/Auth/Login')

        msgReply = request.POST.get('msgReply')
        idCmt = request.POST.get('idCmt')
        if msgReply:
            CommentReply.objects.create(user_id=request.user.id, comment_id=idCmt, msg=msgReply)
            messages.info(request, 'پاسخ شما با موفقیت ارسال شد.')

    allCmts: Comment = Comment.objects.filter(post_id=selected_blog.id).all().order_by('-id')

    context = {
        'blog': selected_blog,
        'likes': likes,
        'bol': bol,
        'view': views,
        'allCmts': allCmts,
        'form':form,
    }
    return render(request, 'blogdetails.html', context)

@login_required(login_url='/Auth/Login')
def LikeUrl(request):
    if not request.user.is_authenticated:
        messages.info(request, 'برای ارسال دیدگاه باید به سیستم وارد شوید.')
        return redirect('/Auth/Login')
    if request.is_ajax():
        BlogID = request.GET.get('BlogID')
        blog: BlogModel = BlogModel.objects.get(id=BlogID)
        isEx = LikePost.objects.filter(blog_id=BlogID, user_id=request.user.id).first()

        if isEx is None:
            blog.likepost_set.create(user_id=request.user.id)
            count = LikePost.objects.filter(blog_id=BlogID).count()
            return JsonResponse({'like':True, 'count':count})

        if isEx:
            blog.likepost_set.get(user_id=request.user.id).delete()
            count = LikePost.objects.filter(blog_id=BlogID).count()
            return JsonResponse({'like':False, 'count':count})

def removeCMT(request, *args, **kwargs):
    if not request.user.is_superuser:
        return redirect('/Blog/List')

    Comment.objects.get(id=kwargs.get('cmtId')).delete()
    blog = kwargs.get('BlogId')
    blogu: BlogModel = BlogModel.objects.get(id=blog)
    messages.info(request,'پیام با موفقیت حذف شد.')
    return redirect(blogu.get_absolute_url())

def removeRPL(request, *args, **kwargs):
    if not request.user.is_superuser:
        return redirect('/Blog/List')

    CommentReply.objects.get(id=kwargs.get('cmtId')).delete()
    blog = kwargs.get('BlogId')
    blogu: BlogModel = BlogModel.objects.get(id=blog)
    messages.info(request,'پاسخ با موفقیت حذف شد.')
    return redirect(blogu.get_absolute_url())

@login_required(login_url='/Auth/Login')
def reportCMT(request, cmtId, BlogId):
    Report_All_Comment.objects.create(comment_id=cmtId, userReporter_id=request.user.id)
    blogu: BlogModel = BlogModel.objects.get(id=BlogId)
    messages.info(request, 'پیام با موفقیت گزارش شد.')
    return redirect(blogu.get_absolute_url())

@login_required(login_url='/Auth/Login')
def reportRPL(request, rplId, BlogId):
    Report_All_Comment.objects.create(reply_id=rplId, userReporter_id=request.user.id)
    blogu: BlogModel = BlogModel.objects.get(id=BlogId)
    messages.info(request, 'پیام با موفقیت گزارش شد.')
    return redirect(blogu.get_absolute_url())