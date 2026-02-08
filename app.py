from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'amazon_clone_secret_key' # Cart functionality ke liye zaroori hai

# 1. Product Categories Configuration
CATEGORIES = {
    'Electronics': {'img': 'electronics.jpg', 'prefix': 'Smart'},
    'Fashion': {'img': 'fashion.jpg', 'prefix': 'Premium'},
    'Grocery': {'img': 'grocery.jpg', 'prefix': 'Organic'},
    'Home Decor': {'img': 'decor.jpg', 'prefix': 'Modern'},
    'Beauty': {'img': 'beauty.jpg', 'prefix': 'Luxury'}
}

# 2. 1000 Products Automated Generation
all_products = []
for i in range(1, 1001):
    category_name = random.choice(list(CATEGORIES.keys()))
    config = CATEGORIES[category_name]
    
    all_products.append({
        'id': i,
        'name': f"{config['prefix']} {category_name} Item #{i}",
        'price': random.randint(99, 9999),
        'category': category_name,
        'image': config['img'],
        'rating': random.randint(3, 5)
    })

@app.route('/')
def index():
    query = request.args.get('search', '').lower()
    cat_filter = request.args.get('category', '')

    # Filtering Logic
    display_products = all_products
    if query:
        display_products = [p for p in display_products if query in p['name'].lower()]
    if cat_filter:
        display_products = [p for p in display_products if p['category'] == cat_filter]

    cart_count = len(session.get('cart', []))
    return render_template('index.html', 
                           products=display_products, 
                           categories=CATEGORIES.keys(), 
                           cart_count=cart_count)

@app.route('/add-to-cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    
    product = next((p for p in all_products if p['id'] == product_id), None)
    if product:
        # Session list ko update karne ka tareeka
        temp_cart = session['cart']
        temp_cart.append(product)
        session['cart'] = temp_cart
        session.modified = True
        
    return redirect(url_for('index'))

@app.route('/cart')
def view_cart():
    cart_items = session.get('cart', [])
    total_bill = sum(item['price'] for item in cart_items)
    return render_template('cart.html', items=cart_items, total=total_bill)

@app.route('/remove/<int:index>')
def remove_item(index):
    temp_cart = session.get('cart', [])
    if 0 <= index < len(temp_cart):
        temp_cart.pop(index)
        session['cart'] = temp_cart
        session.modified = True
    return redirect(url_for('view_cart'))

if __name__ == '__main__':
    app.run(debug=True)