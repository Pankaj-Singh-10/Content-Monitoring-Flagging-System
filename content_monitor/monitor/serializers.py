from rest_framework import serializers
from .models import Keyword, ContentItem, Flag


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['id', 'name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ContentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentItem
        fields = ['id', 'title', 'body', 'source', 'last_updated', 'external_id', 'url']


class FlagSerializer(serializers.ModelSerializer):
    keyword_name = serializers.ReadOnlyField(source='keyword.name')
    content_title = serializers.ReadOnlyField(source='content_item.title')
    
    class Meta:
        model = Flag
        fields = ['id', 'keyword', 'keyword_name', 'content_item', 'content_title', 
                  'score', 'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'score']


class FlagUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flag
        fields = ['status']
        extra_kwargs = {
            'status': {'required': True}
        }
    
    def validate_status(self, value):
        if value not in dict(Flag.STATUS_CHOICES):
            raise serializers.ValidationError(f"Invalid status. Must be one of: {dict(Flag.STATUS_CHOICES).keys()}")
        return value
    
    