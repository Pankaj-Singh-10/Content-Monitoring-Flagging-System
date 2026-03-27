from django.db import models
from django.utils import timezone


class Keyword(models.Model):
    """
    Stores keywords that should be monitored in content items.
    """
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class ContentItem(models.Model):
    """
    Stores content items fetched from external sources.
    """
    title = models.CharField(max_length=500)
    body = models.TextField()
    source = models.CharField(max_length=100)
    last_updated = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    external_id = models.CharField(max_length=200, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    
    class Meta:
        ordering = ['-last_updated']
        indexes = [
            models.Index(fields=['last_updated']),
            models.Index(fields=['source']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.source}"
    
    def has_changed_since(self, timestamp):
        """Check if content has been updated after a given timestamp."""
        if not timestamp:
            return True
        return self.last_updated > timestamp


class Flag(models.Model):
    """
    Stores the relationship between a keyword and matched content item,
    along with review status and score.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('relevant', 'Relevant'),
        ('irrelevant', 'Irrelevant'),
    ]
    
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name='flags')
    content_item = models.ForeignKey(ContentItem, on_delete=models.CASCADE, related_name='flags')
    score = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_suppressed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['keyword', 'content_item']  # Prevent duplicate flags
        
    def __str__(self):
        return f"{self.keyword.name} - {self.content_item.title} ({self.score})"
    
    def is_suppressed(self):
        """Check if this flag is currently suppressed."""
        return self.status == 'irrelevant'
    
    def suppress(self):
        """Mark flag as irrelevant and record suppression time."""
        self.status = 'irrelevant'
        self.last_suppressed_at = timezone.now()
        self.save()

        