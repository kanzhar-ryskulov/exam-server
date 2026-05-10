from http_fw import Controller
from db.flowers_db import FlowerDatabase

class BouquetController(Controller):
    def home(self):
        flower_id = self.request.query_params.get("id")
        flower_type = self.request.query_params.get("type")
        flower_db = FlowerDatabase()

        if flower_id:
            bouquet = flower_db.detail(int(flower_id))
            if bouquet:
                body = f'''<h1>Title : {bouquet['title']}</h1>
                        <p>{bouquet['price']}</p>
                        <img style="width: 50px; height: 50px;" src="{bouquet["img"]}">'''
                for link in bouquet['type']:
                        body += f'<a href="/?type={link}">({link})</a> '
                body += f'''<p>Description : {bouquet['description']}</p>
                        <a href="/">← Back to shop</a>'''
            else:
                body = '<h1>Post not found</h1><a href="/posts">← Back to posts</a>'

        elif flower_type:
            body = f'<h1 class="title">Bouquet types: {flower_type}</h1>'
            bouquets = flower_db.type_to_find(flower_type)
            if bouquets:
                for bouquet in bouquets:
                    body += f'''<div>
                    <img style="width: 50px; height: 50px;" src="{bouquet['img']}">
                    <a href="/?id={bouquet['id']}">{bouquet['title']}</a>
                    <p>Цена: {bouquet['price']}</p>
                    <p>'''
                    for link in bouquet['type']:
                        body += f'<a href="/?type={link}">({link})</a> '
                    body += '</p></div>'
                    body += '<a href="/bouquet/new">Place new bouquet</a>'
            else:
                body += '<p>Not found bouquets </p>'
            body += '<a href="/">← Back to main page</a>'
        else:
            body = '<h1 class="title">Bouquet</h1>'
            body += '<a href="/cart">Cart</a>'
            for bouquet in flower_db.list():
                body += f'''<div>
                <img style="width: 50px; height: 50px;" src="{bouquet['img']}">
                <a href="/?id={bouquet['id']}">{bouquet['title']}</a>
                <p>'''

                for link in bouquet['type']:
                    body += f'<a href="/?type={link}">({link})</a> '
                body += f'<p>Price:{bouquet['price']}</p>'

                body += '</p></div>'
                body += f'<a href="/cart/add?id={bouquet["id"]}">Add to cart</a>'
                body += '<hr>'

            body += '<a href="/bouquet/new">Place new bouquet</a>'
            

        self.response.add_header('Content-Type', 'text/html; charset=utf-8')
        self.response.set_body(body)

    def new(self):
        form = self.get_form()
        self.response.add_header('Content-Type', 'text/html; charset=utf-8')
        self.response.set_body(form)

    def create(self):
        self.response.add_header('Content-Type', 'text/html; charset=utf-8')
        type = self.request.body.get('type')
        img = self.request.body.get('img')
        title = self.request.body.get("title")
        description = self.request.body.get("description")
        price = self.request.body.get("price")

        if title and description and price :
            new_bouquet = {
                'type': type,
                "price" : price[0],
                'img': img[0],
                "description": description[0],
                "title": title[0]
            }
            bouquet_db = FlowerDatabase()
            bouquet_db.add(new_bouquet)
            self.response.add_header("Location", "/")
            self.response.set_status(self.response.HTTP_FOUND)
        else:
            error = "<p style='color: red;'>Все поля обязательны к заполнению</p>"
            form_errors = self.get_form(error)
            self.response.set_body(form_errors)
            self.response.set_status(self.response.HTTP_BAD_REQUEST)

    @staticmethod
    def get_form(errors=""):
        types = ['for a date', 'wedding', 'present', 'birthday']
        form = '''
            <div>
                <h1>Place new bouquet!</h1>
                <form action="/bouquet" method="POST" style="gap:10px; align-items:center;">
                
                <div class="form-example">
                    <label for="name">Title: </label>
                    <input type="text" name="title" id="title" required />
                </div>
                <div class="form-example">
                    <label for="name">Price: </label>
                    <input type="number" name="price" id="price" required />
                </div>
                <div class="form-example">
                    <label for="name">Image: </label>
                    <input type="url" name="img" id="img" required />
                </div>
                <div>
                    <label for="name">Description:</label>
                    <textarea id="description" name="description" rows="5" cols="33">
                    It was a dark and stormy night...
                    </textarea>
                </div>
                <div>
                    <label for="name">Select type(s): </label>
                    '''
        for type in types:
            form += f'''<input type="checkbox" id="{type}" name="type" value="{type}"></input>'''
            form += f'<label for="{type}">{type} </label>'
        form += '''

                </div>
                <input type="submit" value="Create!"/><br/>

                <a href="/">Return to main page</a>
                </form>
            </div>
        '''
        return form + errors
    

    def link_for_types(self):
        bouquet_type = self.request.body.get("type")
        flower_db = FlowerDatabase
        bouquet = flower_db.type_to_find((bouquet_type))
        if bouquet_type:
            body = f'''<h1>{bouquet['title']}</h1>
                    <img src="{bouquet["img"]}">'''
            for link in bouquet['type']:
                    body += f'<a href="/?type={bouquet["type"]}">({link})</a>'
                    f'''
                    <p>{bouquet['price']}</p>
                    <a href="/">← Back to shop</a>'''
