from app import app, db, Product, Location, ProductMovement

def test_app():
    with app.app_context():
        try:
            # Test database connection
            product_count = Product.query.count()
            location_count = Location.query.count()
            movement_count = ProductMovement.query.count()
            
            print(f"Database test successful:")
            print(f"Products: {product_count}")
            print(f"Locations: {location_count}")
            print(f"Movements: {movement_count}")
            
            # Test route
            with app.test_client() as client:
                response = client.get('/')
                print(f"Route test - Status: {response.status_code}")
                if response.status_code != 200:
                    print(f"Error: {response.data.decode()}")
                else:
                    print("Homepage loaded successfully")
                    
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_app()
