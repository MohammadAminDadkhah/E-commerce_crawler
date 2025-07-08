import requests
import urllib.parse

def select_sort_torob(): 
    print(""" 
        1. Default
        2. Most expensive
        3. Cheapest
        4. Newest
    """)
    
    sort = int(input("Select Sort: "))

    while sort < 1 or sort > 4:
        print("Invalid Sort")
        sort = int(input("Select Sort: "))

    final_sort = None
    match sort:
        case 1:
            final_sort = None
        case 2:
            final_sort = "-price"
        case 3:
            final_sort = "price"
        case 4:
            final_sort = "-date"

    return final_sort

# ---------------------------------- #

def torob_crawler(keyword, sort):
    url = "https://api.torob.com/v4/base-product/search/"
    
    encoded_keyword = urllib.parse.quote(keyword)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Origin": "https://torob.com",
        "Referer": "https://torob.com/",
        "Accept": "*/*",
    }

    params = {
        "query": encoded_keyword,
    }

    if sort:
        params["sort"] = sort

    response = requests.get(url, headers=headers, params=params)
    
    results = []
    if response.status_code == 200:
        data = response.json()
        products = data.get("results", [])

        for product in products:
            title = product.get("name1", "بدون عنوان")
            is_adv = product.get("is_adv") == "true"
            price = product.get("price")
            link = "https://torob.com" + product.get("web_client_absolute_url") 

            results.append(
                {
                    "title": title,
                    "price": price,
                    "is_adv": is_adv,
                    "link": link
                }
            )        

    return {"torob": results}