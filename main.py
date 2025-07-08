import json

from sites.digikala import select_sort_digikala, digikala_crawler
from sites.buskool import buskool_crawler
from sites.torob import torob_crawler, select_sort_torob

from mcp.server.fastmcp import FastMCP


# ---------------------------------- #

print(""" 
        1. Digikala
        2. Torob
        3. Buskool
        4. Divar
        """)

site = int(input("select site: "))

while 1 > site > 4:
    print("Invalid number!")
    site = int(input("Enter correct number: "))

keyword = input("Enter search keyword: ").strip()

products = []
match site:
    case 1:
        sort = select_sort_digikala()
        products = digikala_crawler(keyword, sort)

    case 2:
        sort = select_sort_torob()
        products = torob_crawler(keyword, sort)

    case 3: 
        products = buskool_crawler(keyword)

if products:
    with open(f"data/{keyword}.json", "a+", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)
