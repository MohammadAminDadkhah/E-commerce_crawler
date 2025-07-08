import requests
import urllib.parse

def buskool_crawler(keyword):
    url = "https://www.buskool.com/user/get_product_list"

    encoded_keyword = urllib.parse.quote_plus(keyword)

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://www.buskool.com",
        "Referer": f"https://www.buskool.com/product-list?s={encoded_keyword}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "X-CSRF-TOKEN": "n6hf9g5PIKnE7glPnTLbE2vWmorxxIskLZegXF4w",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": "laravel_session=2e63eH4hBmuiCQrAKQoVdkwpzGKzMueKylXOCPEI"
    }

    payload = {
        "client": "web",
        "from_record_number": 0,
        "search_text": keyword,
        "sort_by": "BM",
        "to_record_number": 16
    }

    response = requests.post(url, headers=headers, json=payload)

    data = response.json()
    products = data.get("products", {})

    results = []

    for product in products:
        title = product.get("main").get("product_name")
        city_name = product.get("main").get("city_name")
        is_old = product.get("main").get("is_old")
        min_sale_price = product.get("main").get("min_sale_price")
        min_sale_amount = product.get("main").get("min_sale_amount")
        is_verfied = product.get("user_info").get("is_verified") == 1
    
        results.append(
            {
                "title": title,
                "city_name": city_name,
                "is_old": is_old,
                "min_sale_price": min_sale_price,
                "min_sale_amount": min_sale_amount,
                "is_verfied": is_verfied,
            }
        )

    return {"buskool": results}
