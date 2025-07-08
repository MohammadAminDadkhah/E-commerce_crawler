import requests
import json

def divar_crawler(keyword, max_result=10): 
    base_url = "https://api.divar.ir/v8/postlist/w/search"

    headers = {
        "Content-Type": "application/json",
        "Origin": "https://divar.ir",
        "Referer": "https://divar.ir/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "fa-IR,fa;q=0.9,en;q=0.8"
    }

    payload = {
        "city_ids": ["1"],
        "source_view": "SEARCH",
        "disable_recommendation": False,
        "map_state": {
            "camera_info": {
                "bbox": {}
            }
        },
        "search_data": {
            "form_data": {
                "data": {
                    "category": {
                        "str": {
                            "value": "ROOT"
                        }
                    }
                }
            },
            "server_payload": {
                "@type": "type.googleapis.com/widgets.SearchData.ServerPayload",
                "additional_form_data": {
                    "data": {
                        "sort": {
                            "str": {
                                "value": "sort_date"
                            }
                        }
                    }
                }
            },
            "query": keyword
        }
    }

    try:
        response = requests.post(base_url, headers=headers, json=payload, timeout=10)
        
        if response.status_code != 200:
            print(f"API call failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            return []
        
        data = response.json()
        
        results = []
        print(response)
        if 'widgets' in data:
            for widget in data['widgets']:
                if widget.get('widget_type') == 'POST_ROW':
                    post_data = widget.get('data', {})
                    
                    post_info = {
                        'title': post_data.get('title', ''),
                        'price': post_data.get('middle_description_text', ''),
                        'location': post_data.get('top_description_text', ''),
                        'time': post_data.get('bottom_description_text', ''),
                        'token': post_data.get('token', ''),
                        'url': f"https://divar.ir/v/{post_data.get('token', '')}",
                        'image_url': post_data.get('image_url', ''),
                        'has_chat': post_data.get('has_chat', False)
                    }
                    
                    results.append(post_info)
                    
                    if len(results) >= max_result:
                        break
        
        elif 'web_widgets' in data and 'post_list' in data['web_widgets']:
            for post in data['web_widgets']['post_list']:
                post_data = post.get('data', {})
                
                post_info = {
                    'title': post_data.get('title', ''),
                    'price': post_data.get('middle_description_text', ''),
                    'location': post_data.get('top_description_text', ''),
                    'time': post_data.get('bottom_description_text', ''),
                    'token': post_data.get('token', ''),
                    'url': f"https://divar.ir/v/{post_data.get('token', '')}",
                    'image_url': post_data.get('image_url', ''),
                    'has_chat': post_data.get('has_chat', False)
                }
                
                results.append(post_info)
                
                if len(results) >= max_result:
                    break
        
        print(f"تعداد آگهی‌های پیدا شده: {len(results)}")
        print("-" * 60)
        
        for i, post in enumerate(results, 1):
            print(f"\n{i}. {post['title']}")
            print(f"   قیمت: {post['price']}")
            print(f"   محل: {post['location']}")
            print(f"   زمان: {post['time']}")
            print(f"   لینک: {post['url']}")
        
        print("\n" + "="*60)
        print("ساختار کامل پاسخ API:")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:1000] + "...")
        
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"خطا در ارسال درخواست: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"خطا در تجزیه JSON: {e}")
        return []
    except Exception as e:
        print(f"خطای غیرمنتظره: {e}")
        return []

results = divar_crawler("سبد", max_result=5)

if results:
    print(f"\nموفقیت! {len(results)} آگهی پیدا شد.")
else:
    print("هیچ آگهی‌ای پیدا نشد یا خطایی رخ داد.")