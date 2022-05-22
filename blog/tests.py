from django.test import TestCase, Client
from bs4 import BeautifulSoup as bs
from .models import Post, Category, Tag, Comment
from django.utils import timezone
from django.contrib.auth.models import User

# Create your tests here.

def create_category(name='Life', description=''):
    category, is_created = Category.objects.get_or_create(
        name = name,
        description = description,
    )
## get_or_create() : 인수를 만족시키는게 있으면 겟하고.. 없으면 만들어라..

    category.slug = category.name.replace(' ', '-').replace('/', '')
    category.save()

    return category

def create_tag(name='Yoon-A'):
    tag, is_created = Tag.objects.get_or_create(
        name=name
    )
    tag.slug = tag.name.replace(' ', '-').replace('/', '')
    tag.save()
    return tag

def create_comment(post, text='some comment', author=None):
    if author is None:
        author, is_created = User.objects.get_or_create(
            username='guest',
            password='guestpassword'
        )
    comment = Comment.objects.create(
        post=post,
        text=text,
        author=author
    )
    return comment

def create_post(title, content, author, category=None):
    blog_post = Post.objects.create(
        title=title,
        content=content,
        created=timezone.now(),
        author=author,
        category=category,
    )
    return blog_post

class TestModel(TestCase):
    def setUp(self):
        self.client = Client()  # 테스트를 수행할 클라이언트 생성
        self.author_000 = User.objects.create(username = "Yoon-Ji", password='nopassword')

    def test_category(self):
        category = create_category()
        post_000 = create_post(
            title='The 1st post',
            content='Hello World',
            author=self.author_000,
            category=category,
        )
        self.assertEqual(category.post_set.count(), 1)

    def test_tag(self):
        tag_000 = create_tag(name='bad_guy')
        tag_001 = create_tag(name='korea')

        post_000 = create_post(
            title='The 1st post',
            content='Hello World',
            author=self.author_000,
        )
        post_000.tags.add(tag_000)
        post_000.tags.add(tag_001)
        post_000.save()

        post_001 = create_post(
            title='The 2nd post',
            content='Hello World2',
            author=self.author_000,
        )
        post_001.tags.add(tag_001)
        post_001.save()

        # post는 두개 이상 태그를 가질 수 있다.
        self.assertEqual(post_000.tags.count(), 2)
        # 하나의 태그는 두개 이상의 post에 붙을 수 있다.
        self.assertEqual(tag_001.post_set.count(), 2)
        # 하나의 태그는 자신을 가진 post들을 불러올 수 있다.
        self.assertEqual(tag_001.post_set.first(), post_001)
        self.assertEqual(tag_001.post_set.last(), post_000)


    def test_post(self):
        category = create_category()
        post_000 = create_post(
            title = 'The 1st post',
            content = 'Hello World',
            author = self.author_000,
            category = category,
        )

    def test_comment(self):     # comment 모델 테스트
        post_000 = create_post(
            title='The 1st post',
            content='Hello World',
            author=self.author_000,
        )
        self.assertEqual(Comment.objects.count(), 0)
        comment_000 = create_comment(
            post=post_000
        )
        comment_001 = create_comment(
            post=post_000,
            text="second comment"
        )
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(post_000.comment_set.count(), 2)


class TestView(TestCase):
    def setUp(self):
        self.client = Client()  # 테스트를 수행할 클라이언트 생성
        self.author_000 = User.objects.create_user(username = "Yoon-Ji", password='nopassword')
        self.user_001 = User.objects.create_user(username = "Yoon-A", password='nopassword')


    def check_navbar(self, soup):
        navbar = soup.find('nav', id='nav_area')
        self.assertIn('Home', navbar.text)  # navbar에 Home란 글자가 있는지 여부

    def check_right_side(self, soup):
        category_card = soup.find('div', id='category-card')
        ## 미분류(1) 있어야 함
        self.assertIn('미분류 (1)', category_card.text)
        ### 정치/사회 (1) 있어야 함
        self.assertIn('정치/사회 (1)', category_card.text)

    def test_post_list(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)  # 페이지가 있는지 여부

        soup = bs(response.content, 'html.parser')
        title = soup.title

        self.assertIn('My Blog', title.text)

        self.check_navbar(soup)

        # navbar = soup.find('nav', id='nav_area')
        # self.assertIn('My Blog', navbar.text)  # navbar에 My Blog란 글자가 있는지 여부
        # self.assertIn('Features', navbar.text) # navbar에 Features란 글자가 있는지 여부

        self.assertEqual(Post.objects.count(), 0)  # 게시물이 하나도 없다면...
        self.assertIn("아직 게시물이 없습니다.", soup.body.text)

    def test_post_list_with_post(self):
        tag_korea = create_tag(name='korea')

        post_000 = create_post(
            title='The 1st post',
            content='Hello World',
            author=self.author_000
        )
        post_000.tags.add(tag_korea)
        post_000.save()
        # print(post_000.title, post_000.author, post_000.content, post_000.tags)

        post_001 = create_post(
            title='The 2nd post',
            content='Hello World2',
            author=self.author_000,
            category=create_category('정치/사회')
        )
        post_001.tags.add(tag_korea)
        post_001.save()
        # print(post_001.title, post_001.author, post_001.content, post_001.tags)

        self.assertGreater(Post.objects.count(), 0)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)  # 페이지가 있는지 여부

        soup = bs(response.content, 'html.parser')
        body = soup.body
        self.assertNotIn("아직 게시물이 없습니다.", body.text)
        self.assertIn(post_000.title, body.text)

        ## readmore 버튼 활성화
        post_000_read_more_btn = body.find('a', id='read-more-post-{0}'.format(post_000.pk))
        # print(post_000_read_more_btn['href'])
        self.assertEqual(post_000_read_more_btn['href'], post_000.get_absolute_url())

        # category card에서
        self.check_right_side(soup)
        #### main div에는 '정치/사회' 있어야 함
        main_div = soup.find('div', id='main-div')
        self.assertIn('정치/사회', main_div.text)
        ##### main div에는 '미분류' 있어야 함
        self.assertIn('미분류', main_div.text)

        # Tag관련
        post_card_000 = main_div.find('div', id='post-card-{}'.format(post_000.pk))
        self.assertIn('#korea', post_card_000.text)  # tag가 해당 post의 card마다 있다.

    def test_pagenation(self):
        # 포스트가 적은 경우
        for i in range(0,3):
            post = create_post(
                title='Post No. {0}'.format(i),
                content='{0}번째 포스트 입니다.'.format(i),
                author=self.author_000
            )
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)  # 페이지가 있는지 여부
        soup = bs(response.content, 'html.parser')

        self.assertNotIn('Older', soup.body.text)
        self.assertNotIn('Newer', soup.body.text)


        for i in range(3,10):
            post = create_post(
                title='Post No. {0}'.format(i),
                content='{0}번째 포스트 입니다.'.format(i),
                author=self.author_000
            )
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)  # 페이지가 있는지 여부
        soup = bs(response.content, 'html.parser')

        self.assertIn('Older', soup.body.text)
        self.assertIn('Newer', soup.body.text)



    def test_post_detail(self):
        category_politics = create_category('정치/사회')
        post_000 = create_post(
            title='The 1st post',
            content='Hello World',
            author=self.author_000,
            category=category_politics
        )

        comment_000 = create_comment(post_000, text='test comment', author=self.user_001)
        comment_001 = create_comment(post_000, text='test comment', author=self.author_000)


        tag_korea = create_tag(name='korea')
        post_000.tags.add(tag_korea)
        post_000.save()
        # print(post_000.title, post_000.author, post_000.content, post_000.tags)

        post_001 = create_post(
            title='The 2nd post',
            content='Hello World2',
            author=self.author_000,
        )

        self.assertGreater(Post.objects.count(), 0)
        post_000_url = post_000.get_absolute_url()
        self.assertEqual(post_000_url, '/blog/{0}/'.format(post_000.pk))

        response = self.client.get(post_000_url)
        self.assertEqual(response.status_code, 200)

        soup = bs(response.content, 'html.parser')
        title = soup.title

        self.assertEqual(title.text, '{0} - My Blog'.format(post_000.title))
        self.check_navbar(soup)

        body = soup.body
        main_div = body.find('div', id='main-div')
        self.assertIn(post_000.title, main_div.text)
        self.assertIn(post_000.author.username, main_div.text)
        self.assertIn(post_000.content, main_div.text)

        # category card에서
        self.check_right_side(soup)

        # comment 관련 테스트
        comment_div = main_div.find('div', id='comment-list')
        self.assertIn(comment_000.author.username, comment_div.text)
        self.assertIn(comment_000.text, comment_div.text)

        # Tag관련 테스트
        self.assertIn('#korea', main_div.text)

        # category가 main-div에 있다.
        self.assertIn(category_politics.name, main_div.text)
        # EDIT 버튼이 로근인 하지 않은 경우 보이지 않는다.
        self.assertNotIn('EDIT', main_div.text)
        # 로그인을 한 경우에는
        login_success = self.client.login(username = "Yoon-Ji", password='nopassword')
        self.assertTrue(login_success)
        response = self.client.get(post_000_url)  # 로그인후 리프레쉬
        self.assertEqual(response.status_code, 200)   # 로그인후 리프레쉬
        soup = bs(response.content, 'html.parser')   # 로그인후 리프레쉬
        body = soup.body
        main_div = body.find('div', id='main-div')

        # post.author랑 login 한 사람이 같으면
        self.assertEqual(post_000.author, self.author_000)
        # EDIT 버튼이 있다.
        self.assertIn("EDIT", main_div.text)

        # 그렇지 않은 경우에는 없다. (다른 사람으로 로그인 하는 경우)
        login_success = self.client.login(username="Yoon-A", password='nopassword')
        self.assertTrue(login_success)
        response = self.client.get(post_000_url)  # 로그인후 리프레쉬
        self.assertEqual(response.status_code, 200)  # 로그인후 리프레쉬
        soup = bs(response.content, 'html.parser')  # 로그인후 리프레쉬
        body = soup.body
        main_div = body.find('div', id='main-div')

        # post.author랑 login 한 사람이 같으면
        self.assertEqual(post_000.author, self.author_000)
        # EDIT 버튼이 있다.
        self.assertNotIn("EDIT", main_div.text)

        comments_div=main_div.find('div', id="comment-list")
        comment_000_div=comments_div.find('div', id="comment-id-{0}".format(comment_000.pk))
        self.assertIn('edit', comment_000_div.text)
        self.assertIn('edit', comment_000_div.text)

        comment_001_div=comments_div.find('div', id="comment-id-{0}".format(comment_001.pk))
        self.assertNotIn('edit', comment_001_div.text)
        self.assertNotIn('edit', comment_001_div.text)

    def test_post_list_by_category(self):
        category_politics = create_category(name="정치/사회")

        post_000 = create_post(
            title='The 1st post',
            content='Hello World',
            author=self.author_000
        )
        post_001 = create_post(
            title='The 2nd post',
            content='Hello World2',
            author=self.author_000,
            category=category_politics
        )
        response = self.client.get(category_politics.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = bs(response.content, 'html.parser')
        # self.assertEqual('My Blog - {0}'.format(category_politics.name), soup.title.text)

        main_div = soup.find('div', id='main-div')
        self.assertNotIn('미분류', main_div.text)
        self.assertIn(category_politics.name, main_div.text)

    def test_post_list_no_category(self):
        category_politics = create_category(name="정치/사회")

        post_000 = create_post(
            title='The 1st post',
            content='Hello World',
            author=self.author_000
        )

        post_001 = create_post(
            title='The 2nd post',
            content='Hello World2',
            author=self.author_000,
            category=category_politics
        )

        response = self.client.get('/blog/category/_none/')
        self.assertEqual(response.status_code, 200)

        soup = bs(response.content, 'html.parser')
        # self.assertEqual('My Blog - {0}'.format(category_politics.name), soup.title.text)

        main_div = soup.find('div', id='main-div')
        self.assertIn('미분류', main_div.text)
        self.assertNotIn(category_politics.name, main_div.text)

    def test_tag_page(self):
        tag_000 = create_tag(name='bad_guy')
        tag_001 = create_tag(name='korea')

        post_000 = create_post(
            title='The 1st post',
            content='Hello World',
            author=self.author_000,
        )
        post_000.tags.add(tag_000)
        post_000.tags.add(tag_001)
        post_000.save()

        post_001 = create_post(
            title='The 2nd post',
            content='Hello World2',
            author=self.author_000,
        )
        post_001.tags.add(tag_001)
        post_001.save()

        response = self.client.get(tag_000.get_absolute_url())
        self.assertEqual(response.status_code, 200)  # 페이지가 있는지 여부
        soup = bs(response.content, 'html.parser')
        main_div = soup.find('div', id='main-div')
        nav_title = soup.find('span', id='nav-title')
        # main_div 텍스트에 샵이 붙은 태그 네임이 있어야 한다.
        self.assertIn('#{}'.format(tag_000.name), nav_title.text)
        self.assertIn(post_000.title, main_div.text)
        self.assertNotIn(post_001.title, main_div.text)

    def test_post_create(self):
        response = self.client.get('/blog/create/')
        self.assertNotEqual(response.status_code, 200)

        self.client.login(username = "Yoon-Ji", password='nopassword')
        response = self.client.get('/blog/create/')
        self.assertEqual(response.status_code, 200)

        soup = bs(response.content, 'html.parser')
        main_div = soup.find('div', id="main-div")

    def test_post_update(self):
        post_000 = create_post(
            title='The 1st post',
            content='Hello World',
            author=self.author_000,
        )

        self.assertEqual(post_000.get_update_url(), post_000.get_absolute_url() + 'update/')
        response = self.client.get(post_000.get_update_url())
        self.assertEqual(response.status_code, 200)  # 페이지가 있는지 여부
        soup = bs(response.content, 'html.parser')
        main_div = soup.find('div', id="main-div")

        self.assertNotIn("Created", main_div.text)
        self.assertNotIn("Author", main_div.text)

    def test_new_comment(self):
        post_000 = create_post(
            title='The 1st post',
            content='Hello World',
            author=self.author_000,
        )
        login_success = self.client.login(username = "Yoon-Ji", password='nopassword')
        self.assertTrue(login_success)
        response= self.client.post(
            post_000.get_absolute_url()+'new_comment/', {'text':'A test comment for the first comment'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        soup = bs(response.content, 'html.parser')
        main_div = soup.find('div', id="main-div")
        self.assertIn(post_000.title, main_div.text)
        self.assertIn('A test comment', main_div.text)

    def test_delete_comment(self):
        post_000 = create_post(
            title='The 1st post',
            content='Hello World',
            author=self.author_000,
        )
        comment_000 = create_comment(post_000, text='test comment', author=self.user_001)
        comment_001 = create_comment(post_000, text='test comment', author=self.author_000)

        self.assertEqual(Comment.objects.count(),2)
        self.assertEqual(post_000.comment_set.count(), 2)

        login_success = self.client.login(username="Yoon-Ji", password='nopassword')
        self.assertTrue(login_success)
        # 다른 사람이 댓글 삭제 시도
        with self.assertRaises(PermissionError):
            response = self.client.get('/blog/delete_comment/{0}/'.format(comment_000.pk), follow=True) #댓글지우기
            self.assertEqual(Comment.objects.count(), 2)
            self.assertEqual(post_000.comment_set.count(), 2)

        login_success = self.client.login(username="Yoon-A", password='nopassword')
        response = self.client.get('/blog/delete_comment/{0}/'.format(comment_000.pk), follow=True) #댓글지우기
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(post_000.comment_set.count(), 1)

        soup = bs(response.content, 'html.parser')
        main_div = soup.find('div', id="main-div")

        self.assertNotIn('Yoon-A', main_div.text)

    def test_edit_comment(self):
        post_000 = create_post(
            title='The 1st post',
            content='Hello World',
            author=self.author_000,
        )
        comment_000 = create_comment(post_000, text='I am Yoon-Ji', author=self.user_001)
        comment_001 = create_comment(post_000, text='test comment', author=self.author_000)

        # without login
        with self.assertRaises(PermissionError):
            self.client.get('/blog/edit_comment/{}/'.format(comment_000.pk))
        # login as Yoon-Ji
        login_success = self.client.login(username='Yoon-Ji', password='nopassword')
        self.assertTrue(login_success)
        with self.assertRaises(PermissionError):
            self.client.get('/blog/edit_comment/{}/'.format(comment_000.pk))
        # login as Yoon-A
        login_success = self.client.login(username='Yoon-A', password='nopassword')
        response = self.client.get('/blog/edit_comment/{}/'.format(comment_000.pk))
        self.assertEqual(response.status_code, 200)

        soup = bs(response.content, 'html.parser')
        self.assertIn('Edit Comment: ', soup.body.h3)

        response = self.client.post('/blog/edit_comment/{}/'.format(comment_000.pk),
                                    {'text': "I am a Doctor"}, follow=True)

        self.assertEqual(response.status_code, 200)
        soup = bs(response.content, 'html.parser')
        self.assertIn("Doctor", soup.body.text)
        self.assertNotIn("I am Yoon-Ji", soup.body.text)

    def test_search(self):
        post_000 = create_post(
            title='Stay Foolish, Stay Hungry',
            content = "Steve Job's Life",
            author = self.author_000
        )
        post_001 = create_post(
            title='Trump says',
            content="USA strategy",
            author=self.author_000
        )

        response = self.client.get('/blog/search/Stay Fool/')
        self.assertEqual(response.status_code, 200)
        soup = bs(response.content, 'html.parser')
        self.assertIn(post_000.title, soup.body.text)
        self.assertNotIn(post_001.title, soup.body.text)

        response = self.client.get('/blog/search/strategy/')
        self.assertEqual(response.status_code, 200)
        soup = bs(response.content, 'html.parser')
        self.assertIn(post_001.title, soup.body.text)
        self.assertNotIn(post_000.title, soup.body.text)










