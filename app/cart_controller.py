
import json
from pathlib import Path

from http_fw import Controller
from db.flowers_db import FlowerDatabase


class CartController(Controller):
    cart_items = []

    def cart(self):
        with open('id_json.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        flower_db = FlowerDatabase()
        body = '<h1>Cart</h1>'

        if not data:
            body += '<p>Cart is empty</p>'
        else:
            total = 0
            for item_id in data:
                item = flower_db.detail(item_id)
                if item:
                    body += f'''<div>
                        <p><b>Title:</b> {item['title']}</p>
                        <p><b>Description:</b> {item['description']}</p>
                        <p><b>Price:</b> {item['price']}</p>
                        <a href="/cart/remove?id={item['id']}">Remove</a>
                        <hr>
                    </div>'''
                    total += int(item['price'])
            body += f'<h2>Total: {total}</h2>'

        body += '<a href="/">← Back to shop</a>'
        self.response.add_header('Content-Type', 'text/html; charset=utf-8')
        self.response.set_body(body)

    def add_to_cart(self):
        flower_id = self.request.query_params.get('id')
        CartController.cart_items.append(int(flower_id))
        self.response.add_header('Location', '/')
        self.response.set_status(self.response.HTTP_FOUND)
        self.response.add_header('Content-Type', 'text/html; charset=utf-8')

    def remove_from_cart(self):
        flower_id = self.request.query_params.get('id')

        if flower_id:
            CartController.cart_items.remove(int(flower_id))
            

        self.response.add_header('Location', '/cart')
        self.response.set_status(self.response.HTTP_FOUND)

    def save_to_json(self):
        flower_id = int(self.request.query_params.get('id'))

        path = Path("id_json.json")

        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = []

        data.append(flower_id)
        
        with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        
        self.response.add_header('Location', '/')
        self.response.set_status(self.response.HTTP_FOUND)
        self.response.add_header('Content-Type', 'text/html; charset=utf-8')
    
    def remove_from_json(self):
        flower_id = int(self.request.query_params.get('id'))

        path = Path('id_json.json')

        if path.exists():
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)

                if flower_id in data:
                    data.remove(flower_id)
                    

                    with open(path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)

                    print("Успешно удалено!")
                
        
        self.response.add_header('Location', '/cart')
        self.response.set_status(self.response.HTTP_FOUND)
        
        
        
        





