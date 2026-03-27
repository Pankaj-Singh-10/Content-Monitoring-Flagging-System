from monitor.services.content_fetcher import ContentFetcher
from monitor.services.matching_service import MatchingService
from monitor.models import Flag, ContentItem


class ScanService:
    """
    Orchestrates the content scanning process.
    """
    
    def __init__(self, source='mock'):
        self.fetcher = ContentFetcher(source)
        self.matcher = MatchingService()
    
    def run_scan(self):
        """
        Execute a complete scan:
        1. Fetch content from source
        2. Save content items
        3. Match against keywords
        4. Create/update flags
        """
        # Fetch content
        items = self.fetcher.fetch()
        
        # Save content items
        content_items = self.fetcher.save_content_items(items)
        
        # Scan each content item
        all_flags = []
        for content_item in content_items:
            flags = self.matcher.scan_all_keywords(content_item)
            all_flags.extend(flags)
        
        return {
            'content_items_processed': len(content_items),
            'flags_created': len(all_flags),
            'flags': all_flags
        }
    
    def rescan_content_item(self, content_item_id):
        """
        Rescan a specific content item.
        Useful when content has been updated.
        """
        try:
            content_item = ContentItem.objects.get(id=content_item_id)
            flags = self.matcher.scan_all_keywords(content_item)
            return {
                'content_item_id': content_item_id,
                'flags_processed': len(flags),
                'flags': flags
            }
        except ContentItem.DoesNotExist:
            return None
        
        