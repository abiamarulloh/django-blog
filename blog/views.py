from django.shortcuts import render, get_object_or_404
from .models import Post, Comment, Tag
from django.utils import timezone
from django.db.models import Q
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def post_list(request):
    posts = Post.objects.all()

    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')

        if query is not None:
            # Query
            # ,kmmiop,
            results= Post.objects.filter(title__icontains=query).distinct()

            context={'results': results,
                     'submitbutton': submitbutton}

            return render(request, 'blog/post_list.html', context)

        else:
            return render(request, 'blog/post_list.html', {'posts':posts})

    else:
        return render(request, 'blog/post_list.html', {'posts':posts})
        

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    # Jika method nya Post maka simpan
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=True)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            # Jika berhasil tambah data maka arahkan ke detail post
            return redirect('post_detail', pk=post.pk)

    else:
        # Jika tidak maka tampilkan form
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=True)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


# Views Blog, tambah komentar
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Jika form bernilai post 
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    # Jika tidak
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

def tag_post_list(request, pktitle):
    posts = Post.objects.filter(tags__title__startswith=pktitle)
    return render(request, 'blog/post_list.html', {'posts': posts})

