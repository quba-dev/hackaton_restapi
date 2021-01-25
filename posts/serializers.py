from rest_framework import serializers
from .models import Post, Vote, Comment
from category.serializers import CategorySerializer


# class CommentsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comments
#         fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    reply_count = serializers.SerializerMethodField()

    # commentor = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('content', 'parent', 'reply_count', 'post')
        # fields = '__all__'

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

    # def get_commentor(self, obj):
    #     return obj.commentor.email


class PostSerializer(serializers.ModelSerializer):
    poster = serializers.ReadOnlyField(source='poster.email')
    poster_id = serializers.ReadOnlyField(source='poster.id')
    votes = serializers.SerializerMethodField()

    # category = CategorySerializer(many=False, write_only=True)

    class Meta:
        model = Post
        fields = ['id', 'category', 'title', 'video_url', 'body', 'poster', 'poster_id', 'created', 'votes',
                  'post_comments', 'image', 'video']

    def get_votes(self, post):
        return Vote.objects.filter(post=post).count()

    def to_representation(self, instance):
        user = self.context['request'].user
        representation = super().to_representation(instance)
        representation['category'] = instance.category.name
        representation['post_comments'] = CommentSerializer(instance.post_comments.all(), many=True).data
        # representation['is_favorite'] = user in instance.favorite_users.all()
        return representation


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        # fields = ['id']
        fields = '__all__'