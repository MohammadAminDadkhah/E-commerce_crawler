import requests

# ---------------------------------- #

def select_sort_digikala():  # Determine Digikala sort
    print(""" 
        1. Default
        2. Most viewed
        3. Newest
        4. Best-selling
        5. Cheapest
        6. Most expensive
        7. Customer offers
    """)
    
    sort = int(input("Select Sort: "))

    while sort < 1 or sort > 7:
        print("Invalid Sort")
        sort = int(input("Select Sort: "))

    final_sort = 22
    match sort:
        case 1: final_sort = 22
        case 2: final_sort = 4
        case 3: final_sort = 1
        case 4: final_sort = 7
        case 5: final_sort = 20
        case 6: final_sort = 21
        case 7: final_sort = 27

    return final_sort

# ---------------------------------- #

def get_price_chart_digikala(product_id): # Getting price chart for each item in Digikala
    chart_url = f"https://api.digikala.com/v1/product/{product_id}/price-chart/"   

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,fa-IR;q=0.8,fa;q=0.7,en-US;q=0.6",
        "Origin": "https://www.digikala.com",
        "Referer": "https://www.digikala.com/",
        "Sec-Ch-Ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Priority": "u=1, i",
        "X-Web-Client": "desktop",
        "X-Web-Optimize-Response": "1",
    }

    try:
        response = requests.get(chart_url, headers=headers)
        json = response.json()
        data = json.get("data", {}).get("price_chart")[0].get("history", [])

        chart = []
        for idx, item in enumerate(data, 1):
            chart.append({
                "price": item.get("rrp_price"),
                "day": item.get("day"),
            })
        return chart
    except Exception as e:
        print(f"Error on getting price Chart: {e}")
        return []

# ---------------------------------- #

def digikala_crawler(keyword, sort, max_results=5): # Searching for keyword in Digikala
    base_url = "https://api.digikala.com/v1/search/"

    params = {
        "q": keyword,
        "page": 1,
        "sort": sort
    }

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-GB,en;q=0.9,fa-IR;q=0.8,fa;q=0.7,en-US;q=0.6",
        "Origin": "https://www.digikala.com",
        "Referer": "https://www.digikala.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "X-Web-Client": "desktop",
        "X-Web-Optimize-Response": "1",
    }

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"API call failed with status: {response.status_code}")
        return []

    data = response.json()
    products = data.get("data", {}).get("products", [])

    results = []
    for product in products[:max_results]:
        title = product.get("title_fa", "بدون عنوان")
        id = product.get("id")
        link = f"https://www.digikala.com/product/dkp-{id}"
        price = product.get("default_variant", {}).get("price", {}).get("selling_price", 0) // 10
        special_sale = product.get("default_variant", {}).get("price", {}).get("badge", {}).get("title") == "فروش ویژه"
        discount_percent = product.get("default_variant", {}).get("price", {}).get("discount_percent")
        rating_info = product.get("rating", {})
        warranty = product.get("default_variant", {}).get("warranty", {})
        price_chart = get_price_chart_digikala(id)

        results.append(
            {
                "title": title,
                "price": f"{price:,} تومان",
                "link": link,
                "special_sale": special_sale,
                "discount_percent": discount_percent,
                "rating_info": rating_info,
                "warranty": warranty,
                "price_chart": price_chart,
            }
        )

    return {"digikala": results}
