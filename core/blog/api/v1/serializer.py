from blog.models import Category, Post
from account.models import Profile
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        category = CategorySerializer()
        fields = ('id','author','image', 'title', 'snippet','content', 'category', 'status', 'create_date', 'update_date', 'pub_date')
        read_only_fields = ('author', 'snippet')

    def create(self, validated_data):
        validated_data['author'] = Profile.objects.get(user__id = self.context.get('request').user.id)
        return super().create(validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        representation = super().to_representation(instance)
        if request.parser_context.get('kwargs').get('pk'):
            representation.pop('snippet')
        else:
            representation.pop('content')
        representation['category'] = CategorySerializer(instance.category,context = {'request': request}).data
        return representation