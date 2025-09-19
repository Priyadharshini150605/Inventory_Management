from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Product(db.Model):
    product_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Product {self.product_id}>'

class Location(db.Model):
    location_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Location {self.location_id}>'

class ProductMovement(db.Model):
    movement_id = db.Column(db.String(50), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    from_location = db.Column(db.String(50), db.ForeignKey('location.location_id'), nullable=True)
    to_location = db.Column(db.String(50), db.ForeignKey('location.location_id'), nullable=True)
    product_id = db.Column(db.String(50), db.ForeignKey('product.product_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    
    # Relationships
    product = db.relationship('Product', backref='movements')
    from_loc = db.relationship('Location', foreign_keys=[from_location], backref='outgoing_movements')
    to_loc = db.relationship('Location', foreign_keys=[to_location], backref='incoming_movements')
    
    def __repr__(self):
        return f'<ProductMovement {self.movement_id}>'

# Routes
@app.route('/')
def index():
    # Get statistics for dashboard
    product_count = Product.query.count()
    location_count = Location.query.count()
    movement_count = ProductMovement.query.count()
    
    # Count locations with movements (active locations)
    active_locations = db.session.query(ProductMovement.to_location).distinct().count() + \
                      db.session.query(ProductMovement.from_location).distinct().count()
    
    return render_template('index.html', 
                         product_count=product_count,
                         location_count=location_count, 
                         movement_count=movement_count,
                         active_locations=active_locations)

# Product Routes
@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product = Product(
            product_id=request.form['product_id'],
            name=request.form['name'],
            description=request.form['description']
        )
        try:
            db.session.add(product)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('products'))
        except Exception as e:
            flash('Error adding product. Product ID might already exist.', 'error')
    return render_template('add_product.html')

@app.route('/products/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        try:
            db.session.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('products'))
        except Exception as e:
            flash('Error updating product.', 'error')
    return render_template('edit_product.html', product=product)

@app.route('/products/view/<product_id>')
def view_product(product_id):
    product = Product.query.get_or_404(product_id)
    movements = ProductMovement.query.filter_by(product_id=product_id).order_by(ProductMovement.timestamp.desc()).all()
    return render_template('view_product.html', product=product, movements=movements)

# Location Routes
@app.route('/locations')
def locations():
    locations = Location.query.all()
    return render_template('locations.html', locations=locations)

@app.route('/locations/add', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        location = Location(
            location_id=request.form['location_id'],
            name=request.form['name'],
            address=request.form['address']
        )
        try:
            db.session.add(location)
            db.session.commit()
            flash('Location added successfully!', 'success')
            return redirect(url_for('locations'))
        except Exception as e:
            flash('Error adding location. Location ID might already exist.', 'error')
    return render_template('add_location.html')

@app.route('/locations/edit/<location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    location = Location.query.get_or_404(location_id)
    if request.method == 'POST':
        location.name = request.form['name']
        location.address = request.form['address']
        try:
            db.session.commit()
            flash('Location updated successfully!', 'success')
            return redirect(url_for('locations'))
        except Exception as e:
            flash('Error updating location.', 'error')
    return render_template('edit_location.html', location=location)

@app.route('/locations/view/<location_id>')
def view_location(location_id):
    location = Location.query.get_or_404(location_id)
    incoming = ProductMovement.query.filter_by(to_location=location_id).order_by(ProductMovement.timestamp.desc()).all()
    outgoing = ProductMovement.query.filter_by(from_location=location_id).order_by(ProductMovement.timestamp.desc()).all()
    return render_template('view_location.html', location=location, incoming=incoming, outgoing=outgoing)

# ProductMovement Routes
@app.route('/movements')
def movements():
    movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    return render_template('movements.html', movements=movements)

@app.route('/movements/add', methods=['GET', 'POST'])
def add_movement():
    if request.method == 'POST':
        movement = ProductMovement(
            movement_id=request.form['movement_id'],
            from_location=request.form['from_location'] if request.form['from_location'] else None,
            to_location=request.form['to_location'] if request.form['to_location'] else None,
            product_id=request.form['product_id'],
            qty=int(request.form['qty']),
            notes=request.form['notes']
        )
        try:
            db.session.add(movement)
            db.session.commit()
            flash('Movement added successfully!', 'success')
            return redirect(url_for('movements'))
        except Exception as e:
            flash('Error adding movement. Check that product and locations exist.', 'error')
    
    products = Product.query.all()
    locations = Location.query.all()
    return render_template('add_movement.html', products=products, locations=locations)

@app.route('/movements/edit/<movement_id>', methods=['GET', 'POST'])
def edit_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    if request.method == 'POST':
        movement.from_location = request.form['from_location'] if request.form['from_location'] else None
        movement.to_location = request.form['to_location'] if request.form['to_location'] else None
        movement.product_id = request.form['product_id']
        movement.qty = int(request.form['qty'])
        movement.notes = request.form['notes']
        try:
            db.session.commit()
            flash('Movement updated successfully!', 'success')
            return redirect(url_for('movements'))
        except Exception as e:
            flash('Error updating movement.', 'error')
    
    products = Product.query.all()
    locations = Location.query.all()
    return render_template('edit_movement.html', movement=movement, products=products, locations=locations)

@app.route('/movements/view/<movement_id>')
def view_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    return render_template('view_movement.html', movement=movement)

# Balance Report
@app.route('/balance')
def balance_report():
    # Calculate balance for each product in each location
    balance_data = {}
    
    # Get all movements
    movements = ProductMovement.query.all()
    
    for movement in movements:
        product_id = movement.product_id
        qty = movement.qty
        
        # Initialize product in balance_data if not exists
        if product_id not in balance_data:
            balance_data[product_id] = {}
        
        # Handle incoming movements (to_location)
        if movement.to_location:
            if movement.to_location not in balance_data[product_id]:
                balance_data[product_id][movement.to_location] = 0
            balance_data[product_id][movement.to_location] += qty
        
        # Handle outgoing movements (from_location)
        if movement.from_location:
            if movement.from_location not in balance_data[product_id]:
                balance_data[product_id][movement.from_location] = 0
            balance_data[product_id][movement.from_location] -= qty
    
    # Convert to list format for template
    balance_list = []
    for product_id, locations in balance_data.items():
        product = Product.query.get(product_id)
        for location_id, qty in locations.items():
            if qty != 0:  # Only show non-zero balances
                location = Location.query.get(location_id)
                balance_list.append({
                    'product': product,
                    'location': location,
                    'qty': qty
                })
    
    return render_template('balance_report.html', balance_list=balance_list)

# API endpoint for balance data (for potential future use)
@app.route('/api/balance')
def api_balance():
    balance_data = {}
    movements = ProductMovement.query.all()
    
    for movement in movements:
        product_id = movement.product_id
        qty = movement.qty
        
        if product_id not in balance_data:
            balance_data[product_id] = {}
        
        if movement.to_location:
            if movement.to_location not in balance_data[product_id]:
                balance_data[product_id][movement.to_location] = 0
            balance_data[product_id][movement.to_location] += qty
        
        if movement.from_location:
            if movement.from_location not in balance_data[product_id]:
                balance_data[product_id][movement.from_location] = 0
            balance_data[product_id][movement.from_location] -= qty
    
    return jsonify(balance_data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)
