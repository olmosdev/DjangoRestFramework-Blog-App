from django.urls import path

from .views import (
    PostListView, 
    PostDetailView, 
    PostHeadingsView, 
    IncrementPostClickView
)

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    # path("posts/<slug>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/", PostDetailView.as_view(), name="post-detail"),
    # path("post/<slug:slug>/headings/", PostHeadingsView.as_view(), name="post-headings"),
    path("post/headings/", PostHeadingsView.as_view(), name="post-headings"),
    path("post/increment_clicks/", IncrementPostClickView.as_view(), name="increment-post-click"),
]
