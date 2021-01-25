from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from .models import Post, Vote, Comment
from .serializers import PostSerializer, VoteSerializer, CommentSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .paginations import Paginatin

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = Paginatin
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'id', 'body']
    filterset_fields = ['category']

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk):
        instance = self.get_object()
        user = request.user
        is_favorite = request.data.get('favorite', False)
        if is_favorite:
            instance.favorite_users.add(user)
        else:
            instance.favorite_users.remove(user)
        instance.save()
        return Response({'is_favorite': is_favorite})


    # @action(detail=False, methods=['get'])
    # def search(self, request, pk=None):
    #     print(request.query_params)
    #     q = request.query_params.get('q')
    #     queryset = self.get_queryset()
    #     queryset = queryset.filter(Q(title__icontains=q))
    #     serializer = PostSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     search_query = self.request.query_params.get('search')
    #     if search_query:
    #         queryset = queryset.annotate(
    #             similarity = TrigramSimilarity('title', search_query),
    #         ).filter(similarity__gt=0.2).order_by('-similarity')
    #     return queryset


class PostRetrievDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], poster=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('Ты не можешь удалить этот пост, так как он не твой, дядя')

    def patch(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], poster=self.request.user)
        if post.exists():
            return self.partial_update(request, *args, **kwargs)
        else:
            raise ValidationError('Ты не можешь вносить изменения в чужой пост, дядя')

    def put(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], poster=self.request.user)
        if post.exists():
            return self.partial_update(request, *args, **kwargs)
        else:
            raise ValidationError('Ты не можешь обновить полностью то, что не принадлежит тебе')


class VoteCreate(generics.ListCreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('Ты уже проголосовал')
        serializer.save(voter=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('Ты не голосовал здесь')


class CommentCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    #
    # def post(self, request, *args, **kwargs):
    #     post = Post.objects.filter(pk=kwargs['pk'], commentor=self.request.user)
    #     if post.exists():
    #         return self.create(request, *args, **kwargs)
    #     else:
    #         raise ValidationError('Даже не пытайся')

    def delete(self, request, *args, **kwargs):
        # post = Post.objects.filter(pk=kwargs['pk'], commentor=self.request.user)
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('Ты не комментировал здесь')


class FavoritePosts(generics.ListCreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        queryset = Vote.objects.filter(voter=self.request.user)
        serializer = VoteSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)