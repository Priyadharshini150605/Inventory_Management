# Inventory Management System

A modern, professional web application built with Flask for managing inventory across multiple locations. This system provides comprehensive tracking of products, warehouses, and inventory movements with an intuitive user interface.

## Features

### Core Functionality
- **Product Management**: Add, edit, and view products with detailed information
- **Location Management**: Manage multiple warehouses and store locations
- **Movement Tracking**: Record and monitor inventory transfers, sales, and restocking
- **Balance Reports**: Real-time inventory balance across all locations with filtering and export capabilities

### Advanced Features
- **Interactive Dashboard**: Overview statistics and quick actions
- **Modern UI**: Responsive Bootstrap 5 design with gradient themes
- **Search & Filter**: Advanced filtering options for all data views
- **Export Functionality**: CSV export for balance reports
- **Stock Status Indicators**: Visual indicators for stock levels (In Stock, Low Stock, Critical, etc.)
- **Cross-Referenced Navigation**: Easy navigation between related products, locations, and movements

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Icons**: Bootstrap Icons
- **Forms**: Flask-WTF for form handling and validation

## Database Schema

### Tables
1. **Product**
   - `product_id` (Primary Key, VARCHAR)
   - `name` (VARCHAR, NOT NULL)
   - `description` (TEXT)
   - `created_at` (DATETIME)

2. **Location**
   - `location_id` (Primary Key, VARCHAR)
   - `name` (VARCHAR, NOT NULL)
   - `address` (TEXT)
   - `created_at` (DATETIME)

3. **ProductMovement**
   - `movement_id` (Primary Key, VARCHAR)
   - `timestamp` (DATETIME, NOT NULL)
   - `from_location` (VARCHAR, Foreign Key - can be NULL)
   - `to_location` (VARCHAR, Foreign Key - can be NULL)
   - `product_id` (VARCHAR, Foreign Key, NOT NULL)
   - `qty` (INTEGER, NOT NULL)
   - `notes` (TEXT)

##  Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone or download the project**
   ```bash
   cd "c:\Aerele task\task2"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database with sample data**
   ```bash
   python create_sample_data.py
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your web browser and navigate to: `http://127.0.0.1:5000`

##  Sample Data

The system comes pre-loaded with sample data including:

### Products (4 items)
- **PROD001**: Laptop Dell XPS 13
- **PROD002**: iPhone 15 Pro
- **PROD003**: Samsung Galaxy Tab S9
- **PROD004**: Sony WH-1000XM5 Headphones

### Locations (4 warehouses/stores)
- **WH001**: Main Warehouse
- **STORE01**: Downtown Store
- **STORE02**: Mall Store
- **WH002**: Secondary Warehouse

### Movements (23+ transactions)
- Initial stock arrivals
- Inter-location transfers
- Store restocking operations
- Customer sales
- Emergency restocking

## 🎯 Use Cases Demonstrated

The sample data demonstrates all requested use cases:

1. ✅ **Move Product A to Location X**: Multiple products moved to various locations
2. ✅ **Move Product B to Location X**: Different products to same locations
3. ✅ **Move Product A from Location X to Location Y**: Inter-location transfers
4. ✅ **20+ Movements**: 23 diverse movement transactions included

## 📱 User Interface

### Dashboard
- Statistics overview (total products, locations, movements)
- Quick action buttons
- Modern card-based layout

### Product Management
- List view with search and pagination
- Detailed product pages with movement history
- Add/Edit forms with validation

### Location Management
- Warehouse and store management
- Incoming/outgoing movement tracking
- Location-specific inventory views

### Movement Tracking
- Comprehensive movement logging
- Support for stock-in, stock-out, and transfers
- Movement type visualization

### Balance Report
- Real-time inventory calculations
- Interactive filtering and sorting
- Export to CSV functionality
- Stock status indicators

##  Configuration

### Database Configuration
The application uses SQLite by default. The database file (`inventory.db`) is created automatically in the `instance/` directory.

### Application Settings
Key settings in `app.py`:
- `SECRET_KEY`: Used for session management and CSRF protection
- `SQLALCHEMY_DATABASE_URI`: Database connection string
- `SQLALCHEMY_TRACK_MODIFICATIONS`: Disabled for performance

## Project Structure

```
inventory-management/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── create_sample_data.py  # Sample data generator
├── test_app.py           # Application testing script
├── README.md             # This file
├── instance/
│   └── inventory.db      # SQLite database (auto-generated)
└── templates/
    ├── base.html         # Base template with navigation
    ├── index.html        # Dashboard
    ├── products.html     # Product listing
    ├── add_product.html  # Add product form
    ├── edit_product.html # Edit product form
    ├── view_product.html # Product details
    ├── locations.html    # Location listing
    ├── add_location.html # Add location form
    ├── edit_location.html# Edit location form
    ├── view_location.html# Location details
    ├── movements.html    # Movement listing
    ├── add_movement.html # Add movement form
    ├── edit_movement.html# Edit movement form
    ├── view_movement.html# Movement details
    └── balance_report.html# Inventory balance report
```

## 🔍 API Endpoints

### Web Routes
- `GET /` - Dashboard
- `GET /products` - Product listing
- `GET /products/add` - Add product form
- `POST /products/add` - Create product
- `GET /products/edit/<id>` - Edit product form
- `POST /products/edit/<id>` - Update product
- `GET /products/view/<id>` - Product details
- `GET /locations` - Location listing
- `GET /locations/add` - Add location form
- `POST /locations/add` - Create location
- `GET /locations/edit/<id>` - Edit location form
- `POST /locations/edit/<id>` - Update location
- `GET /locations/view/<id>` - Location details
- `GET /movements` - Movement listing
- `GET /movements/add` - Add movement form
- `POST /movements/add` - Create movement
- `GET /movements/edit/<id>` - Edit movement form
- `POST /movements/edit/<id>` - Update movement
- `GET /movements/view/<id>` - Movement details
- `GET /balance` - Balance report

### API Routes
- `GET /api/balance` - JSON balance data

## 🧪 Testing

Run the test script to verify the application:
```bash
python test_app.py
```

## 🚀 Deployment

For production deployment:

1. **Set environment variables**:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secret-key-here
   ```

2. **Use a production WSGI server** (e.g., Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```


