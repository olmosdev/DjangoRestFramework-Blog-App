from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, APIException
import redis
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from .models import Post, Heading, PostAnalytics
from .serializers import PostListSerializer, PostSerializer, HeadingSerializer, PostView
from .utils import get_client_ip
from .tasks import increment_post_impressions
from core.permissions import HasValidAPIKey
from .tasks import increment_post_views_task

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)

"""class PostListView(ListAPIView):
    queryset = Post.postobjects.all()
    serializer_class = PostListSerializer"""

class PostListView(APIView): # APIWiew allows us to have more control over our views
    permission_classes = [HasValidAPIKey]

    # @method_decorator(cache_page(60 * 1)) Not recommended when you have a complex logic
    def get(self, request, *args, **kwargs):
        try:
            # Checking if the data is in cache
            cached_posts = cache.get("post_list")
            if cached_posts:
                # Increasing impressions in Redis for cached post
                for post in cached_posts:
                    redis_client.incr(f"post:impressions:{post["id"]}")
                return Response(cached_posts)

            # Getting post from database if data is not in cache
            posts = Post.postobjects.all()

            if not posts.exists():
                raise NotFound(detail="No posts found")

            # Serializing data in cache
            serialized_posts = PostListSerializer(posts, many=True).data

            # Saving data in cache
            cache.set("post_list", serialized_posts, timeout=60 * 5)

            # Increasing impressions in Redis
            for post in posts:
                # increment_post_impressions.delay(post.id)
                redis_client.incr(f"post:impressions:{post.id}")

        except Post.DoesNotExist:
            raise NotFound(detail="No posts found")
        except Exception as e:
            raise APIException(detail=f"An unexpected error ocurred: {str(e)}")

        return Response(serialized_posts)

"""class PostDetailView(RetrieveAPIView):
    queryset = Post.postobjects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"""

class PostDetailView(RetrieveAPIView):
    permission_classes = [HasValidAPIKey]

    def get(self, request, slug):
        ip_address = get_client_ip(request)

        try:
            # Checking if the data is in cache
            cached_post = cache.get(f"post_detail:{slug}")
            if cached_post:
                increment_post_views_task.delay(cached_post["slug"], ip_address)
                return Response(cached_post)

            # If data is not in cahce, get data from database
            post = Post.postobjects.get(slug=slug)
            serialized_post = PostSerializer(post).data 

            # Saving data in cache
            cache.set(f"post_detail:{slug}", serialized_post, timeout=60 * 5)

            increment_post_views_task.delay(post.slug, ip_address)

        except Post.DoesNotExist:
            raise NotFound(detail="The requested post does not exist")
        except Exception as e:
            raise APIException(detail=f"An unexpected error ocurred: {str(e)}")

        return Response(serialized_post)

class PostHeadingsView(ListAPIView):
    permission_classes = [HasValidAPIKey]

    serializer_class = HeadingSerializer
    
    def get_queryset(self):
        post_slug = self.kwargs.get("slug")
        return Heading.objects.filter(post__slug=post_slug)

class IncrementPostClickView(APIView):
    permission_classes = [HasValidAPIKey]

    permission_classes = [permissions.AllowAny]
    def post(self, request):
        """Increment the click counter of a post based on a slug"""
        data = request.data
        try:
            post = Post.postobjects.get(slug=data["slug"])
        except Post.DoesNotExist:
            raise NotFound(detail="The requested post does not exist")
        
        try:
            post_analytics, created = PostAnalytics.objects.get_or_create(post=post)
            post_analytics.increment_click()
        except Exception as e:
            raise APIException(detail=f"An error ocurred while updating post analytics")

        return Response({
            "message": "Click incremented successfully",
            "clicks": post_analytics.clicks
        })


