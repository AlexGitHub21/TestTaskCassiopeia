import xml.etree.ElementTree as ET
from datetime import datetime

from feed_task import build_yml, PRODUCTS, CATEGORIES

def test_xml_is_valid():
    result = build_yml(PRODUCTS, CATEGORIES, datetime(2026, 6, 18, 12, 0),)
    ET.fromstring(result)

def test_generated_at_format():
    result = build_yml(PRODUCTS, CATEGORIES, datetime(2026, 6, 18, 12, 0, 30),)
    root = ET.fromstring(result)

    assert root.attrib["date"] == "2026-06-18 12:00"

def test_valid_product_only():
    result = build_yml(PRODUCTS, CATEGORIES, datetime(2026, 6, 18, 12, 0),)
    root = ET.fromstring(result)

    offers = root.findall(".//offer")

    ids = [
        offer.attrib["id"] for offer in offers
    ]

    assert ids == ["101", "102", "107"]

def test_categories():
    result = build_yml(PRODUCTS, CATEGORIES, datetime(2026, 6, 18, 12, 0),)
    root = ET.fromstring(result)

    categories = root.findall(".//category")

    ids = [
        cat.attrib["id"] for cat in categories
    ]

    assert ids == ["1", "2"]

def test_available_values():
    result = build_yml(PRODUCTS, CATEGORIES, datetime(2026, 6, 18, 12, 0),)
    root = ET.fromstring(result)

    offers = root.findall(".//offer")

    offers = {
        offer.attrib["id"]: offer for offer in offers
    }

    assert offers["101"].attrib["available"] == "true"
    assert offers["102"].attrib["available"] == "false"
    assert offers["107"].attrib["available"] == "true"

def test_price():
    result = build_yml(PRODUCTS, CATEGORIES, datetime(2026, 6, 18, 12, 0),)
    root = ET.fromstring(result)

    offers = root.findall(".//offer")

    offers = {
        offer.attrib["id"]: offer for offer in offers
    }

    assert offers["101"].find("price").text == "490.00"
    assert offers["102"].find("price").text == "1500.00"
    assert offers["107"].find("price").text == "700.50"

def test_oldprice():
    result = build_yml(PRODUCTS, CATEGORIES, datetime(2026, 6, 18, 12, 0),)
    root = ET.fromstring(result)

    offers = root.findall(".//offer")

    offers = {
        offer.attrib["id"]: offer for offer in offers
    }

    assert offers["101"].find("oldprice") is not None
    assert offers["101"].find("oldprice").text == "590.00"
    assert offers["102"].find("oldprice") is None
    assert offers["107"].find("oldprice") is None

def test_name_special_symbols():
    result = build_yml(PRODUCTS, CATEGORIES, datetime(2026, 6, 18, 12, 0),)
    root = ET.fromstring(result)

    offer = root.find(".//offer[@id='101']")

    assert offer.find("name").text == 'Чай "Лес & травы" <сбор №1>'

def test_description():
    result = build_yml(PRODUCTS, CATEGORIES, datetime(2026, 6, 18, 12, 0),)
    root = ET.fromstring(result)

    offers = root.findall(".//offer")

    offers = {
        offer.attrib["id"]: offer for offer in offers
    }

    assert offers["101"].find("description") is not None
    assert offers["102"].find("description") is not None
    assert offers["107"].find("description") is None

def test_picture_url_must_start_http():
    products = PRODUCTS.copy()

    products.append(
        {
            "id": 150,
            "name": "Чайник стеклянный",
            "slug": "glass-teapot",
            "category_id": 2,
            "price": "1500.00",
            "old_price": "1400.00",
            "stock": 0,
            "description": "Стеклянный чайник объёмом 800 мл",
            "image_url": "ftp://example.test/media/teapot-102.jpg",
            "is_active": True,
        },
    )

    result = build_yml(PRODUCTS, CATEGORIES, datetime(2026, 6, 18, 12, 0), )
    root = ET.fromstring(result)

    offers = root.findall(".//offer")

    ids = [
        offer.attrib["id"] for offer in offers
    ]

    assert 200 not in ids