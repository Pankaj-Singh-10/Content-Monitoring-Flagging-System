from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django.http import JsonResponse
from .models import Keyword, Flag
from .serializers import KeywordSerializer, FlagSerializer, FlagUpdateSerializer
from .services.scan_service import ScanService


# Add this root_view function at the very top after imports
def root_view(request):
    """Root endpoint showing available API endpoints"""
    endpoints = {
        "api": {
            "keywords": {
                "list": "GET /api/keywords/",
                "create": "POST /api/keywords/",
                "detail": "GET /api/keywords/{id}/",
                "update": "PUT/PATCH /api/keywords/{id}/",
                "delete": "DELETE /api/keywords/{id}/"
            },
            "scan": {
                "trigger": "POST /api/scan/",
                "rescan": "POST /api/rescan/{content_item_id}/"
            },
            "flags": {
                "list": "GET /api/flags/",
                "update": "PATCH /api/flags/{id}/"
            },
            "filters": {
                "by_status": "GET /api/flags/?status=pending",
                "by_keyword": "GET /api/flags/?keyword_id=1"
            }
        },
        "admin": "http://127.0.0.1:8000/admin/",
        "documentation": "See README.md for detailed documentation"
    }
    return JsonResponse(endpoints, safe=False, json_dumps_params={'indent': 2})


class KeywordListCreateView(generics.ListCreateAPIView):
    """
    List all keywords or create a new keyword.
    """
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer


class KeywordDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a keyword.
    """
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer


class ScanTriggerView(APIView):
    """
    Trigger a content scan.
    """
    
    def post(self, request):
        source = request.data.get('source', 'mock')
        
        try:
            scan_service = ScanService(source)
            result = scan_service.run_scan()
            
            return Response({
                'message': 'Scan completed successfully',
                'content_items_processed': result['content_items_processed'],
                'flags_created': result['flags_created']
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': f'Scan failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FlagListView(generics.ListAPIView):
    """
    List all flags with filtering options.
    """
    serializer_class = FlagSerializer
    
    def get_queryset(self):
        queryset = Flag.objects.all()
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by keyword
        keyword_id = self.request.query_params.get('keyword_id')
        if keyword_id:
            queryset = queryset.filter(keyword_id=keyword_id)
        
        # Filter by content item
        content_item_id = self.request.query_params.get('content_item_id')
        if content_item_id:
            queryset = queryset.filter(content_item_id=content_item_id)
        
        return queryset


class FlagUpdateView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update flag status (review workflow).
    """
    queryset = Flag.objects.all()
    serializer_class = FlagUpdateSerializer
    
    def perform_update(self, serializer):
        with transaction.atomic():
            flag = self.get_object()
            new_status = serializer.validated_data['status']
            
            # If marking as irrelevant, record suppression time
            if new_status == 'irrelevant' and flag.status != 'irrelevant':
                flag.status = new_status
                flag.last_suppressed_at = timezone.now()
                flag.save()
            else:
                serializer.save()


class RescanContentItemView(APIView):
    """
    Rescan a specific content item.
    """
    
    def post(self, request, content_item_id):
        scan_service = ScanService()
        result = scan_service.rescan_content_item(content_item_id)
        
        if result is None:
            return Response({
                'error': 'Content item not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'message': 'Rescan completed',
            'content_item_id': result['content_item_id'],
            'flags_processed': len(result['flags'])
        }, status=status.HTTP_200_OK)
    


