import requests
import json
from datetime import datetime
from django.conf import settings
from monitor.models import ContentItem


class ContentFetcher:
    """
    Service for fetching content from various sources.
    """
    
    def __init__(self, source='mock'):
        self.source = source
    
    def fetch(self):
        """Fetch content from configured source."""
        if self.source == 'mock':
            return self._fetch_mock()
        elif self.source == 'newsapi':
            return self._fetch_newsapi()
        else:
            raise ValueError(f"Unknown source: {self.source}")
    
    def _fetch_mock(self):
        """Return mock content data."""
        mock_data = [
            {
                "title": "Learn Django Fast",
                "body": "Django is a powerful Python framework for web development. It follows the MVT pattern.",
                "source": "Blog A",
                "last_updated": "2026-03-20T10:00:00Z",
                "external_id": "blog_a_1"
            },
            {
                "title": "Python Automation Guide",
                "body": "Automate your workflow with Python scripts and data pipelines.",
                "source": "Blog A",
                "last_updated": "2026-03-20T10:00:00Z",
                "external_id": "blog_a_2"
            },
            {
                "title": "Cooking Tips",
                "body": "Best recipes for beginners. Learn to cook delicious meals.",
                "source": "Blog B",
                "last_updated": "2026-03-20T10:00:00Z",
                "external_id": "blog_b_1"
            },
            {
                "title": "Data Pipeline Best Practices",
                "body": "Building efficient data pipelines with Python and Django.",
                "source": "Blog A",
                "last_updated": "2026-03-20T10:00:00Z",
                "external_id": "blog_a_3"
            }
        ]
        return mock_data
    
    def _fetch_newsapi(self):
        """Fetch from NewsAPI (requires API key)."""
        api_key = settings.NEWS_API_KEY
        if not api_key:
            raise ValueError("NewsAPI key not configured")
        
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': 'python OR django OR automation',
            'apiKey': api_key,
            'pageSize': 20
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for article in data.get('articles', []):
                articles.append({
                    'title': article.get('title', ''),
                    'body': article.get('description', ''),
                    'source': article.get('source', {}).get('name', 'NewsAPI'),
                    'last_updated': article.get('publishedAt', datetime.now().isoformat()),
                    'external_id': article.get('url', ''),
                    'url': article.get('url', '')
                })
            return articles
        except Exception as e:
            print(f"Error fetching from NewsAPI: {e}")
            return []
    
    def save_content_items(self, items):
        """Save fetched content items to database."""
        saved_items = []
        for item in items:
            content_item, created = ContentItem.objects.update_or_create(
                external_id=item.get('external_id'),
                defaults={
                    'title': item['title'],
                    'body': item['body'],
                    'source': item['source'],
                    'last_updated': datetime.fromisoformat(item['last_updated'].replace('Z', '+00:00')),
                    'url': item.get('url', '')
                }
            )
            saved_items.append(content_item)
        return saved_items
    

    