from app import app, db, Product, Location, ProductMovement
from datetime import datetime, timedelta
import random

def create_sample_data():
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Clear existing data
        ProductMovement.query.delete()
        Product.query.delete()
        Location.query.delete()
        db.session.commit()
        
        # Create Products
        products = [
            Product(product_id='PROD001', name='Laptop Dell XPS 13', description='High-performance ultrabook with 13-inch display'),
            Product(product_id='PROD002', name='iPhone 15 Pro', description='Latest Apple smartphone with advanced camera system'),
            Product(product_id='PROD003', name='Samsung Galaxy Tab S9', description='Premium Android tablet with S Pen'),
            Product(product_id='PROD004', name='Sony WH-1000XM5', description='Wireless noise-canceling headphones')
        ]
        
        for product in products:
            db.session.add(product)
        
        # Create Locations
        locations = [
            Location(location_id='WH001', name='Main Warehouse', address='123 Industrial Ave, Tech City, TC 12345'),
            Location(location_id='STORE01', name='Downtown Store', address='456 Main St, Downtown, TC 67890'),
            Location(location_id='STORE02', name='Mall Store', address='789 Shopping Center Blvd, Mall District, TC 54321'),
            Location(location_id='WH002', name='Secondary Warehouse', address='321 Storage Rd, Warehouse District, TC 98765')
        ]
        
        for location in locations:
            db.session.add(location)
        
        db.session.commit()
        
        # Create ProductMovements (20+ movements as requested)
        movements = []
        movement_counter = 1
        
        # Initial stock arrivals (receiving inventory)
        base_date = datetime.now() - timedelta(days=30)
        
        for i, product in enumerate(products):
            # Stock arrival to main warehouse
            movement = ProductMovement(
                movement_id=f'MOV{movement_counter:03d}',
                timestamp=base_date + timedelta(days=i),
                from_location=None,  # External source
                to_location='WH001',
                product_id=product.product_id,
                qty=random.randint(50, 100),
                notes='Initial stock arrival'
            )
            movements.append(movement)
            movement_counter += 1
        
        # Transfers from main warehouse to stores
        for i, product in enumerate(products):
            # Transfer to Store 1
            movement = ProductMovement(
                movement_id=f'MOV{movement_counter:03d}',
                timestamp=base_date + timedelta(days=5 + i),
                from_location='WH001',
                to_location='STORE01',
                product_id=product.product_id,
                qty=random.randint(10, 25),
                notes='Store restocking'
            )
            movements.append(movement)
            movement_counter += 1
            
            # Transfer to Store 2
            movement = ProductMovement(
                movement_id=f'MOV{movement_counter:03d}',
                timestamp=base_date + timedelta(days=6 + i),
                from_location='WH001',
                to_location='STORE02',
                product_id=product.product_id,
                qty=random.randint(10, 25),
                notes='Store restocking'
            )
            movements.append(movement)
            movement_counter += 1
        
        # Inter-store transfers
        movement = ProductMovement(
            movement_id=f'MOV{movement_counter:03d}',
            timestamp=base_date + timedelta(days=10),
            from_location='STORE01',
            to_location='STORE02',
            product_id='PROD001',
            qty=5,
            notes='Inter-store transfer due to high demand'
        )
        movements.append(movement)
        movement_counter += 1
        
        movement = ProductMovement(
            movement_id=f'MOV{movement_counter:03d}',
            timestamp=base_date + timedelta(days=12),
            from_location='STORE02',
            to_location='STORE01',
            product_id='PROD002',
            qty=3,
            notes='Balancing inventory levels'
        )
        movements.append(movement)
        movement_counter += 1
        
        # Sales (outgoing movements)
        for i in range(6):
            product_id = random.choice(['PROD001', 'PROD002', 'PROD003', 'PROD004'])
            store = random.choice(['STORE01', 'STORE02'])
            movement = ProductMovement(
                movement_id=f'MOV{movement_counter:03d}',
                timestamp=base_date + timedelta(days=15 + i),
                from_location=store,
                to_location=None,  # External destination (sale)
                product_id=product_id,
                qty=random.randint(1, 5),
                notes='Customer sale'
            )
            movements.append(movement)
            movement_counter += 1
        
        # Additional warehouse operations
        movement = ProductMovement(
            movement_id=f'MOV{movement_counter:03d}',
            timestamp=base_date + timedelta(days=20),
            from_location='WH001',
            to_location='WH002',
            product_id='PROD003',
            qty=15,
            notes='Moving to secondary warehouse for overflow'
        )
        movements.append(movement)
        movement_counter += 1
        
        movement = ProductMovement(
            movement_id=f'MOV{movement_counter:03d}',
            timestamp=base_date + timedelta(days=22),
            from_location='WH002',
            to_location='STORE01',
            product_id='PROD003',
            qty=8,
            notes='Fulfilling store request from secondary warehouse'
        )
        movements.append(movement)
        movement_counter += 1
        
        # Recent restocking
        movement = ProductMovement(
            movement_id=f'MOV{movement_counter:03d}',
            timestamp=datetime.now() - timedelta(days=2),
            from_location=None,
            to_location='WH001',
            product_id='PROD004',
            qty=30,
            notes='Emergency restocking due to high demand'
        )
        movements.append(movement)
        movement_counter += 1
        
        # Add all movements to database
        for movement in movements:
            db.session.add(movement)
        
        db.session.commit()
        
        print(f"Sample data created successfully!")
        print(f"- {len(products)} products")
        print(f"- {len(locations)} locations") 
        print(f"- {len(movements)} movements")
        
        return True

if __name__ == '__main__':
    create_sample_data()
