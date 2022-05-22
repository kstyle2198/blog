from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)  # 동일 이름이 두개가 되지 않도록
    description = models.TextField(blank=True)  # 공란일 수도 있다.

    slug = models.SlugField(unique=True, allow_unicode=True)
    # pk를 키값으로 안쓰고 slug를 대신 사용하려고..예컨데..127.0.0.1:8000/blog/1/ 이런 식이 아니라
    # 127.0.0.1:8000/blog/정치사회/ 이런식이 되게 하려고고, 유니코드는 한글 사용 때문에

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/blog/category/{0}/'.format(self.slug)

    class Meta:
        verbose_name_plural = 'category'


class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/blog/tag/{0}/'.format(self.slug)

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = MarkdownxField()

    head_image = models.ImageField(upload_to= 'blog/%Y/%m/%d/', blank=True)   # 공란일 수도 있다.

    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ['-created',]

    def __str__(self):
        return '{0}: {1}'.format(self.title, self.author)


    def get_absolute_url(self):
        return '/blog/{0}/'.format(self.pk)    # view onsite 기능

    def get_update_url(self):
        return self.get_absolute_url() + 'update/'    # view onsite 기능

    def get_markdown_content(self):
        return markdown(self.content)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = MarkdownxField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def get_markdown_content(self):
        return markdown(self.text)

    def get_absolute_url(self):
        return self.post.get_absolute_url() + '#comment-id-{0}'.format(self.pk)

    def __str__(self):
        return '{0}:{1}'.format(self.post,self.text)



