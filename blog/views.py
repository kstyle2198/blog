from django.shortcuts import render, redirect
from .models import Post, Category, Tag, Comment
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm
from django.db.models import Q


class PostList(ListView):
    model = Post
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(
            category=None).count()
        return context

class PostSearch(PostList):
    def get_queryset(self):
        q = self.kwargs['q']
        object_list = Post.objects.filter(
            Q(title__contains=q) | Q(content__contains=q))   # 타이틀이나 콘텐츠를 대상으로 q를 검색
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostSearch, self).get_context_data()
        context['search_info'] = 'Search: "{}"'.format(self.kwargs['q'])
        return context


#### truncated 된 글의 상세 내용 보는 뷰 ##
class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(
            category=None).count()
        context['comment_form'] = CommentForm()
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = [
        'title', 'content', 'head_image', 'category', 'tags'
    ]

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(type(self), self).form_valid(form)
        else:
            return redirect('/blog/')


class PostUpdate(UpdateView):
    model = Post
    fields = [
        'title', 'content', 'head_image', 'category', 'tags'
    ]


class PostlistByTag(ListView):
    def get_queryset(self):
        tag_slug = self.kwargs['slug']
        tag = Tag.objects.get(slug=tag_slug)

        return tag.post_set.order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(
            category=None).count()
        tag_slug = self.kwargs['slug']
        context['tag'] = Tag.objects.get(slug=tag_slug)

        return context


class PostlistByCategory(ListView):

    def get_queryset(self):
        slug = self.kwargs['slug']

        if slug == '_none':
            category = None
        else:
            category = Category.objects.get(slug=slug)
        return Post.objects.filter(category=category).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(
            category=None).count()

        slug = self.kwargs['slug']
        if slug == '_none':
            context['category'] = "미분류"
        else:
            category = Category.objects.get(slug=slug)
            context['category'] = category

        # context['title'] = 'My Blog - {0}'.format(category.name)
        return context


def new_comment(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect(comment.get_absolute_url())
    else:
        return redirect('/blog/')


class CommentUpdate(UpdateView):
    model = Comment
    form_class = CommentForm

    def get_object(self, queryset=None):  # 남이 url 수집해서 남의 댓글 지우지 못하도록 사용자 체크
        comment = super(CommentUpdate, self).get_object()
        if comment.author != self.request.user:
            raise PermissionError("comment를 수정할 권한이 없습니다.")
        return comment


def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    post = comment.post

    if request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url()+'#comment-list')
    else:
        raise PermissionError("comment를 삭제할 권한이 없습니다.")

# 아래의 class based view 보다 위의 function based view가 더 짧고 간단하기 때문에 최종 위에 걸로 간다.
# class CommentDelete(DeleteView):
#     model = Comment
#
#     def get_object(self, queryset=None):   #남이 url 수집해서 남의 댓글 지우지 못하도록 사용자 체크
#         comment = super(CommentDelete, self).get_object()
#         if comment.author != self.request.user:
#             raise PermissionError
#         return comment
#
#
#     def get_success_url(self):
#         post = self.get_object().post
#         return post.get_absolute_url()+'#comment-list'

# def post_detail(request, pk):
#     blog_post = Post.objects.get(pk=pk)
#     return render(
#         request,
#         'blog/post_detail.html',
#         {
#             'blog_post':blog_post
#         }
#     )
