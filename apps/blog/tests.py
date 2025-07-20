from django.test import TestCase

from .models import Category, Post, PostAnalytics, Heading

# Create your tests here.
class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Tech",
            title="Technology",
            description="All about technology",
            slug="tech"
        )

    def test_category_creation(self):
        self.assertEqual(str(self.category), "Tech")
        self.assertEqual(self.category.title, "Technology")

class PostModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Tech",
            title="Technology",
            description="All about technology",
            slug="tech"
        )

        self.post = Post.objects.create(
            title="Post 1",
            description="A test post",
            content="Content for the post",
            thumbnail=None,
            keywords="test, post",
            slug="post-1",
            category=self.category,
            status="published"
        )

    def test_post_creation(self):
        self.assertEqual(str(self.post), "Post 1")
        self.assertEqual(self.post.category.name, "Tech")

    def test_post_published_manager(self):
        self.assertTrue(Post.postobjects.filter(status="published").exists())

class PostAnalyticsModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Analytics", slug="analytics")

        self.post = Post.objects.create(
            title="Post 1",
            description="A test post",
            content="Content for the post",
            slug="post-1",
            category=self.category
        )
        self.analytics = PostAnalytics.objects.create(post=self.post)

    def test_click_through_rate_update(self):
        self.analytics.increment_impression()
        self.analytics.increment_click()
        self.analytics.refresh_from_db()
        self.assertEqual(self.analytics.click_through_rate, 100.0)

class HeadingModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Heading", slug="heading")
        self.post = Post.objects.create(
            title="Post with Headings",
            description="Post containing headings",
            content="Content with headings",
            slug="post-with-headings",
            category=self.category
        )

        self.heading = Heading.objects.create(
            post=self.post,
            title="Heading 1",
            slug="heading-1",
            level=1,
            order=1
        )

    def test_heading_creation(self):
        self.assertEqual(self.heading.slug, "heading-1")
        self.assertEqual(self.heading.level, 1)

