from rest_framework import serializers
from blog.models import Comment, Post

class CommentSerializer(serializers.Serializer):
    email = serializers.CharField()
    content = serializers.CharField(max_length = 200)
    created = serializers.DateTimeField()

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', self.email)
        instance.content = validated_data.get('content', self.content)
        instance.created = validated_data.get('created', self.created)
        instance.save()
        return instance
    
class PostSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        fields = (
            "id",
            "author",
            "title",
            "body",
            "created",
            "status",
            "slug",
        )
        model = Post
