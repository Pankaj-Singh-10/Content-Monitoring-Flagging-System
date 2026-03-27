import re
from monitor.models import Keyword, Flag, ContentItem


class MatchingService:
    """
    Service for matching keywords against content items.
    """
    
    def __init__(self):
        self.matching_rules = [
            (self._exact_title_match, 100),
            (self._partial_title_match, 70),
            (self._body_match, 40),
        ]
    
    def match_keyword_with_content(self, keyword, content_item):
        """
        Match a single keyword with a content item.
        Returns score if match found, None otherwise.
        """
        # Check if there's an existing irrelevant flag that should be suppressed
        existing_flag = Flag.objects.filter(
            keyword=keyword,
            content_item=content_item,
            status='irrelevant'
        ).first()
        
        if existing_flag and not content_item.has_changed_since(existing_flag.last_suppressed_at):
            return None, "Suppressed - content unchanged"
        
        for rule, score in self.matching_rules:
            if rule(keyword.name, content_item):
                return score, "Matched"
        
        return None, "No match"
    
    def _exact_title_match(self, keyword, content_item):
        """Check for exact keyword match in title."""
        title_lower = content_item.title.lower()
        keyword_lower = keyword.lower()
        return keyword_lower in re.findall(r'\b' + re.escape(keyword_lower) + r'\b', title_lower)
    
    def _partial_title_match(self, keyword, content_item):
        """Check for partial keyword match in title."""
        title_lower = content_item.title.lower()
        keyword_lower = keyword.lower()
        return keyword_lower in title_lower
    
    def _body_match(self, keyword, content_item):
        """Check for keyword match in body."""
        body_lower = content_item.body.lower()
        keyword_lower = keyword.lower()
        return keyword_lower in body_lower
    
    def scan_all_keywords(self, content_item):
        """
        Scan a content item against all keywords and create flags.
        Returns list of created flags.
        """
        created_flags = []
        keywords = Keyword.objects.all()
        
        for keyword in keywords:
            score, reason = self.match_keyword_with_content(keyword, content_item)
            
            if score is not None:
                # Check for existing flags
                existing_flag = Flag.objects.filter(
                    keyword=keyword,
                    content_item=content_item
                ).first()
                
                if existing_flag:
                    # If flag exists and is not irrelevant, update score
                    if existing_flag.status != 'irrelevant':
                        existing_flag.score = score
                        existing_flag.save()
                        created_flags.append(existing_flag)
                else:
                    # Create new flag
                    flag = Flag.objects.create(
                        keyword=keyword,
                        content_item=content_item,
                        score=score,
                        status='pending'
                    )
                    created_flags.append(flag)
        
        return created_flags
    
    