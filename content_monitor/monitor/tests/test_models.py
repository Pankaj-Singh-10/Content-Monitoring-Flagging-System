from django.test import TestCase
from django.utils import timezone
from monitor.models import Keyword, ContentItem, Flag


class KeywordModelTest(TestCase):
    def test_create_keyword(self):
        keyword = Keyword.objects.create(name='python')
        self.assertEqual(keyword.name, 'python')
        self.assertEqual(str(keyword), 'python')


class ContentItemModelTest(TestCase):
    def test_create_content_item(self):
        content = ContentItem.objects.create(
            title='Test Title',
            body='Test body content',
            source='Test Source',
            last_updated=timezone.now()
        )
        self.assertEqual(content.title, 'Test Title')
    
    def test_has_changed_since(self):
        now = timezone.now()
        earlier = timezone.now() - timezone.timedelta(hours=1)
        
        content = ContentItem.objects.create(
            title='Test',
            body='Test',
            source='Test',
            last_updated=now
        )
        
        self.assertTrue(content.has_changed_since(earlier))
        self.assertFalse(content.has_changed_since(now))

