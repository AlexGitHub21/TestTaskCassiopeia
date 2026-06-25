from datetime import datetime
from feed_task import build_yml, PRODUCTS, CATEGORIES
from django.http import HttpResponse

def yml_feed():
    result = build_yml(
           products=PRODUCTS,
           categories=CATEGORIES,
           generated_at=datetime(2026, 6, 18, 12, 0),
       )

    return HttpResponse(result, content_type="application/xml")