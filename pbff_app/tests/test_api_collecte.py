import requests
import json

categories = ['pizza', 'pate a tartiner', 'gateau', 'yaourt', 'bonbon']

results = []

for elt in categories:
    payload = {'action': 'process', 'tagtype_0': 'categories', 'tag_contains_0': 'contains',
            'tag_0': "\'" + elt + "\'", 'sort_by': 'unique_scans_n', 'page_size': '3',
            'axis_x': 'energy', 'axis_y': 'products_n', 'json': '1'}
    req = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?", params=payload)
    data = req.json()
    data_str = json.dumps(data, indent = 2) 
    data_id = data['products'][0]['id']
    data_product_name_fr = data['products'][0]['product_name_fr']
    data_url = data['products'][0]['url']
    data_nova_group = data['products'][0]['nova_group']
    dic_data = {"data_id": data_id,"data_product_name_fr": data_product_name_fr, 
            "data_url": data_url, "data_nova_group": data_nova_group}
    results.append(dic_data)