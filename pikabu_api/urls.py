from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# from posts import views
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from category.views import CategoryListView
from posts.views import PostList, PostRetrievDestroy, VoteCreate, CommentCreate, FavoritePosts
schema_view = get_schema_view(title='Pikabushechka')



# urlpatterns = [
#     path('', include_docs_urls(title='Pikabushechka')),
#     path('admin/', admin.site.urls),
#     path('api/posts/', views.PostList.as_view()),
#     path('api/posts/<int:pk>/', views.PostRetrievDestroy.as_view()),
#     path('api/posts/<int:pk>/vote/', views.VoteCreate.as_view()),
#     path('api/accounts/', include('user.urls')),
#     # path('api/posts/<int:pk>/comment/', views.PostCommentList.as_view()),
#     path('api/posts/<int:pk>/comment', views.Comment.as_view()),
#     path('api/category/<str:slug>/', CategoryListView.as_view()),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)


urlpatterns = [
    path('', include_docs_urls(title='Pikabushechka')),
    path('admin/', admin.site.urls),
    path('api/posts/', PostList.as_view()),
    # path('api/posts/favorite/<int:pk>', PostList.as_view()),
    path('api/posts/<int:pk>/', PostRetrievDestroy.as_view()),
    path('api/posts/<int:pk>/vote/', VoteCreate.as_view()),
    path('api/accounts/', include('user.urls')),
    # path('api/posts/<int:pk>/comment/', views.PostCommentList.as_view()),
    path('api/posts/comment/', CommentCreate.as_view()),
    path('api/posts/comment/<int:pk>/', CommentCreate.as_view()),
    path('api/category/', CategoryListView.as_view()),
    path('api/favorite/', FavoritePosts.as_view()),
]

if settings.DEBUG is True:
    urlpatterns +=static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns +=static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

