from datetime import datetime
import xml.etree.ElementTree as ET

CATEGORIES = [
   {
       "id": 1,
       "name": "Чай",
       "is_active": True,
   },
   {
       "id": 2,
       "name": "Посуда",
       "is_active": True,
   },
   {
       "id": 3,
       "name": "Подарочные наборы",
       "is_active": False,
   },
]


PRODUCTS = [
   {
       "id": 101,
       "name": 'Чай "Лес & травы" <сбор №1>',
       "slug": "les-i-travy",
       "category_id": 1,
       "price": "490.00",
       "old_price": "590.00",
       "stock": 12,
       "description": "Вкус: мята & чабрец > классический чай",
       "image_url": "https://example.test/media/tea-101.jpg",
       "is_active": True,
   },
   {
       "id": 102,
       "name": "Чайник стеклянный",
       "slug": "glass-teapot",
       "category_id": 2,
       "price": "1500.00",
       "old_price": "1400.00",
       "stock": 0,
       "description": "Стеклянный чайник объёмом 800 мл",
       "image_url": "https://example.test/media/teapot-102.jpg",
       "is_active": True,
   },
   {
       "id": 103,
       "name": "Скрытый товар",
       "slug": "hidden-product",
       "category_id": 1,
       "price": "350.00",
       "old_price": None,
       "stock": 5,
       "description": "Товар отключён администратором",
       "image_url": "https://example.test/media/product-103.jpg",
       "is_active": False,
   },
   {
       "id": 104,
       "name": "Пробник чая",
       "slug": "tea-sample",
       "category_id": 1,
       "price": "0.00",
       "old_price": None,
       "stock": 30,
       "description": "Бесплатный пробник",
       "image_url": "https://example.test/media/product-104.jpg",
       "is_active": True,
   },
   {
       "id": 105,
       "name": "Чашка фарфоровая",
       "slug": "porcelain-cup",
       "category_id": 2,
       "price": "700.00",
       "old_price": "900.00",
       "stock": 4,
       "description": "Фарфоровая чашка",
       "image_url": None,
       "is_active": True,
   },
   {
       "id": 106,
       "name": "Подарочный набор",
       "slug": "gift-set",
       "category_id": 3,
       "price": "2500.00",
       "old_price": "3000.00",
       "stock": 2,
       "description": "Товар находится в неактивной категории",
       "image_url": "https://example.test/media/product-106.jpg",
       "is_active": True,
   },
   {
       "id": 107,
       "name": "Чай улун молочный",
       "slug": "milk-oolong",
       "category_id": 1,
       "price": "700.50",
       "old_price": None,
       "stock": 3,
       "description": "",
       "image_url": "https://example.test/media/product-107.jpg",
       "is_active": True,
   },
]


def build_yml(products, categories, generated_at):
    if isinstance(generated_at, datetime):
        generated_at = generated_at.strftime("%Y-%m-%d %H:%M")
    root = ET.Element("yml_catalog", {"date": generated_at})

    shop = ET.SubElement(root, "shop")
    ET.SubElement(shop, "name").text = "Test Shop"
    ET.SubElement(shop, "company").text = "Test Company"
    ET.SubElement(shop, "url").text = "https://example.test"

    currencies = ET.SubElement(shop, "currencies")
    ET.SubElement(currencies, "currency", {"id":"RUB", "rate":"1"})


    products = sorted(products, key=lambda p: p["id"])

    categories = sorted(categories, key=lambda c: c["id"])

    valid_products = []
    for product in products:
       image_url = product["image_url"]

       if (product["is_active"]
               and product["name"]
               and float(product["price"]) > 0
               and image_url
               and image_url.startswith(("http://", "https://"))
       ):
           category = next(
               (
                   category for category in categories
                   if category["id"] == product["category_id"]
                    and category["is_active"]
                ), None,
           )
           if category:
               valid_products.append(product)

    valid_category_ids = {
      product["category_id"]
       for product in valid_products
    }

    categories_el = ET.SubElement(shop, "categories")
    for category in categories:
       if category["id"] in valid_category_ids:
           cat = ET.SubElement(categories_el, "category", {"id": str(category["id"])})
           cat.text = category["name"]

    offers_el = ET.SubElement(shop, "offers")


    for product in valid_products:
        available = "true" if product["stock"] > 0 else "false"
        offer = ET.SubElement(offers_el, "offer", {"id": str(product["id"]), "available": available})

        ET.SubElement(offer, "url").text = f'https://example.test/products/{product["slug"]}/'

        ET.SubElement(offer, "price").text = f'{float(product["price"]):.2f}'

        if (product["old_price"]
               and float(product["old_price"]) > 0
               and float(product["old_price"]) > float(product["price"])):

            ET.SubElement(offer, "oldprice").text = f'{float(product["old_price"]):.2f}'

        ET.SubElement(offer, "currencyId").text = "RUB"
        ET.SubElement(offer, "categoryId").text = str(product["category_id"])
        ET.SubElement(offer, "picture").text = product["image_url"]
        ET.SubElement(offer, "name").text = product["name"]

        if product["description"]:
            ET.SubElement(offer, "description").text = product["description"]

    return ET.tostring(
        root,
        encoding="utf-8",
        xml_declaration=True,
    ).decode("utf-8")


if __name__ == "__main__":

   result = build_yml(
       products=PRODUCTS,
       categories=CATEGORIES,
       generated_at=datetime(2026, 6, 18, 12, 0),
   )

   print(result)
