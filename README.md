# Content-Monitoring-Flagging-System
A Django-based backend system that ingests external content, identifies keyword-based matches, and supports a human review workflow with suppression rules.

## 📋 Requirements

This implementation fulfills all functional requirements:

- ✅ **Data Models**: Keyword, ContentItem, Flag with proper relationships
- ✅ **Keyword Management**: Create keywords via API endpoint
- ✅ **Content Import**: Mock dataset integration (configurable for NewsAPI)
- ✅ **Matching Logic**: Score-based matching (100/70/40)
- ✅ **Review Workflow**: Update flag status (pending/relevant/irrelevant)
- ✅ **Suppression Logic**: Irrelevant flags don't reappear unless content changes

## 🛠 Tech Stack

- Django 4.2.7
- Django REST Framework 3.14.0
- SQLite
- Python 3.8+

## 🚀 Quick Start

### 1. Clone & Setup
in ```bash

git clone https://github.com/yourusername/content-monitoring-system.git
cd content-monitoring-system
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate


### 2. Install Dependencies
in ```bash

pip install -r requirements.txt

### 3. Database Setup
in ```bash

cd content_monitor
python manage.py migrate
python manage.py createsuperuser  # Optional: for admin access

### 4. Run Server
in ```bash

python manage.py runserver

Visit: http://127.0.0.1:8000/

## Data Models

### Keyword Model
class Keyword:
    name: str              # Keyword to monitor (unique)
    created_at: datetime
    updated_at: datetime

### ContentItem Model  
class ContentItem:
    title: str             # Content title
    body: str              # Content body/text
    source: str            # Source (mock/newsapi/rss)
    last_updated: datetime # Signal for content changes
    external_id: str       # Optional external identifier

### Flag Model
class Flag:
    keyword: FK            # Reference to Keyword
    content_item: FK       # Reference to ContentItem
    score: int             # 100/70/40 based on match type
    status: str            # pending/relevant/irrelevant
    last_suppressed_at: datetime  # When marked irrelevant


## API Endpoints

Method	  Endpoint	      Description
POST	 /api/keywords/	  Create a keyword
GET	   /api/keywords/	  List all keywords
POST	  /api/scan/	    Trigger content scan
GET	    /api/flags/	    List flags (filter with ?status=pending)
PATCH	/api/flags/{id}/	Update flag status (review workflow)

## Sample API Calls

in ```bash

### 1. Create keywords
curl -X POST http://127.0.0.1:8000/api/keywords/ \
  -H "Content-Type: application/json" \
  -d '{"name": "python"}'

### 2. Trigger scan (mock data)
curl -X POST http://127.0.0.1:8000/api/scan/ \
  -H "Content-Type: application/json" \
  -d '{"source": "mock"}'

### 3. List all flags
curl http://127.0.0.1:8000/api/flags/

### 4. Update flag status (review)
curl -X PATCH http://127.0.0.1:8000/api/flags/1/ \
  -H "Content-Type: application/json" \
  -d '{"status": "relevant"}'

### 5. Filter pending flags
curl "http://127.0.0.1:8000/api/flags/?status=pending"

## Matching Logic

Match Condition	                 Score
Exact keyword match in title	    100
Partial keyword match in title	   70
Keyword appears in body only	     40

## Suppression Test

### Mark flag as irrelevant
curl -X PATCH http://127.0.0.1:8000/api/flags/2/ \
  -H "Content-Type: application/json" \
  -d '{"status": "irrelevant"}'

### Run scan again
curl -X POST http://127.0.0.1:8000/api/scan/ \
  -H "Content-Type: application/json" \
  -d '{"source": "mock"}'

### Verify flag remains irrelevant
curl http://127.0.0.1:8000/api/flags/2/

## Content Source

### Mock dataset (default in settings.py):

[
  {
    "title": "Learn Django Fast",
    "body": "Django is a powerful Python framework",
    "source": "Blog A",
    "last_updated": "2026-03-20T10:00:00Z"
  },
  {
    "title": "Python Automation Guide",
    "body": "Automate workflows with Python scripts",
    "source": "Blog A",
    "last_updated": "2026-03-20T10:00:00Z"
  }
]
