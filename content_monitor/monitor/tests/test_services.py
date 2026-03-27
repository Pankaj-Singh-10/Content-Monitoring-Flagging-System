from django.test import TestCase
from django.utils import timezone
from monitor.models import Keyword, ContentItem, Flag
from monitor.services.matching_service import MatchingService
from monitor.services.scan_service import ScanService


class MatchingServiceTest(TestCase):
    def setUp(self):
        self.keyword = Keyword.objects.create(name='python')
        self.content = ContentItem.objects.create(
            title='Python Programming',
            body='Learn Python programming language',
            source='Test',
            last_updated=timezone.now()
        )
        self.service = MatchingService()
    
    def test_exact_title_match(self):
        score, reason = self.service.match_keyword_with_content(self.keyword, self.content)
        self.assertEqual(score, 70)  # Partial match in title
    
    def test_body_match(self):
        content = ContentItem.objects.create(
            title='Programming Guide',
            body='Learn Python programming',
            source='Test',
            last_updated=timezone.now()
        )
        score, reason = self.service.match_keyword_with_content(self.keyword, content)
        self.assertEqual(score, 40)
    
    def test_no_match(self):
        content = ContentItem.objects.create(
            title='Cooking Tips',
            body='Delicious recipes',
            source='Test',
            last_updated=timezone.now()
        )
        score, reason = self.service.match_keyword_with_content(self.keyword, content)
        self.assertIsNone(score)


class ScanServiceTest(TestCase):
    def setUp(self):
        self.keyword = Keyword.objects.create(name='python')
        self.service = ScanService(source='mock')
    
    def test_scan_creates_flags(self):
        result = self.service.run_scan()
        self.assertGreater(result['content_items_processed'], 0)
        self.assertGreater(result['flags_created'], 0)

        