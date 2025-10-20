from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'  # Change this in production!

# Use environment variable for secret key in production
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Demo PIN for authentication
DEMO_PIN = '123456'

# Sample data
CUSTOMERS = [
    {'id': 1, 'name': 'John Doe', 'phone': '+1 (555) 123-4567', 'email': 'john@example.com', 'address': '123 Main St, City, State'},
    {'id': 2, 'name': 'Jane Smith', 'phone': '+1 (555) 987-6543', 'email': 'jane@example.com', 'address': '456 Oak Ave, City, State'},
    {'id': 3, 'name': 'Bob Johnson', 'phone': '+1 (555) 456-7890', 'email': 'bob@example.com', 'address': '789 Pine Ln, City, State'},
]

ORDERS = [
    {'id': 'ORD-001', 'customer': 'John Doe', 'total': 234.50, 'status': 'Processing', 'date': '2024-10-19'},
    {'id': 'ORD-002', 'customer': 'Jane Smith', 'total': 156.75, 'status': 'Shipped', 'date': '2024-10-18'},
    {'id': 'ORD-003', 'customer': 'Bob Johnson', 'total': 89.25, 'status': 'Pending', 'date': '2024-10-17'},
]

ITEMS = [
    {'id': 1, 'name': '43 set', 'category': 'RINGS', 'price': 250.00, 'stock': 15},
    {'id': 2, 'name': '43 set', 'category': 'RINGS', 'price': 500.00, 'stock': 15},
    {'id': 3, 'name': '20MM NAGALS', 'category': 'NAGALS', 'price': 300.00, 'stock': 8},
    {'id': 4, 'name': '25MM NAGALS', 'category': 'NAGALS', 'price': 400.00, 'stock': 25},
]

# Create a helper function to generate dashboard data
def get_dashboard_data():
    """Generate dashboard data for all pages"""
    return {
        'today_sales': 2847,
        'active_orders': len([o for o in ORDERS if o['status'] in ['Processing', 'Pending']]),
        'total_items': len(ITEMS),
        'total_customers': len(CUSTOMERS),
        'recent_orders': ORDERS[:3]
    }

@app.route('/')
def login():
    """Login page route"""
    if session.get('authenticated'):
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    """Handle PIN authentication"""
    pin = request.form.get('pin')
    
    if pin == DEMO_PIN:
        session['authenticated'] = True
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid PIN. Please try again.', 'error')
        return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    """Dashboard page - requires authentication"""
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    dashboard_data = get_dashboard_data()
    return render_template('dashboard.html', data=dashboard_data)

@app.route('/customers')
def customers():
    """Customers page"""
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    dashboard_data = get_dashboard_data()
    return render_template('customers.html', customers=CUSTOMERS, data=dashboard_data)

@app.route('/orders')
def orders():
    """Orders page"""
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    dashboard_data = get_dashboard_data()
    return render_template('orders.html', orders=ORDERS, data=dashboard_data)

@app.route('/create-order')
def create_order():
    """Create order page"""
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    dashboard_data = get_dashboard_data()
    return render_template('create_order.html', customers=CUSTOMERS, data=dashboard_data)

@app.route('/items')
def items():
    """Items/Inventory page"""
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    dashboard_data = get_dashboard_data()
    return render_template('items.html', items=ITEMS, data=dashboard_data)

@app.route('/delivery-charges')
def delivery_charges():
    """Delivery charges page"""
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    # Sample delivery data
    delivery_data = [
        {
            'id': 1,
            'loadDate': '18-3-25',
            'vehicleNumber': '3830',
            'totalAmount': 11440.00,
            'description': '',
            'amountDue': 11440.00,
            'payments': []
        },
        {
            'id': 2,
            'loadDate': '22-3-25',
            'vehicleNumber': 'AP16TU1652',
            'totalAmount': 16100.00,
            'description': '',
            'amountDue': 16100.00,
            'payments': []
        },
        {
            'id': 3,
            'loadDate': '22-3-25',
            'vehicleNumber': 'AP20TC0477',
            'totalAmount': 12500.00,
            'description': '',
            'amountDue': 12500.00,
            'payments': []
        },
        {
            'id': 4,
            'loadDate': '22-3-25',
            'vehicleNumber': 'AP26TT1969',
            'totalAmount': 13000.00,
            'description': '',
            'amountDue': 13000.00,
            'payments': []
        },
        {
            'id': 5,
            'loadDate': '24/3/25',
            'vehicleNumber': 'TS02UB3830',
            'totalAmount': 15500.00,
            'description': '',
            'amountDue': 15500.00,
            'payments': []
        }
    ]
    
    payment_history = [
        {
            'paymentDate': '18-3-25',
            'amountPaid': 7200.00,
            'description': 'KANTAS AND KIRAYI PAID',
            'paidBy': 'Manager1',
            'paidTo': 'Driver'
        },
        {
            'paymentDate': '19-3-25',
            'amountPaid': 4240.00,
            'description': 'KANTAS AND KIRAYI PAID',
            'paidBy': 'Manager2',
            'paidTo': 'Mathew'
        },
        {
            'paymentDate': '20-3-25',
            'amountPaid': 11500.00,
            'description': 'KANTAS AND KIRAYI PAID',
            'paidBy': 'Manager1',
            'paidTo': 'DRIVER'
        },
        {
            'paymentDate': '20-3-25',
            'amountPaid': 4600.00,
            'description': 'KANTAS AND KIRAYI PAID',
            'paidBy': 'Manager1',
            'paidTo': 'DRIVER'
        }
    ]
    
    # Calculate stats
    total_pending = sum(delivery['amountDue'] for delivery in delivery_data)
    total_paid = sum(payment['amountPaid'] for payment in payment_history)
    active_deliveries = len([d for d in delivery_data if d['amountDue'] > 0])
    this_month = total_pending + total_paid
    
    stats = {
        'total_pending': total_pending,
        'total_paid': total_paid,
        'active_deliveries': active_deliveries,
        'this_month': this_month
    }
    
    return render_template('delivery_charges.html', 
                         deliveries=delivery_data, 
                         payments=payment_history, 
                         stats=stats)

@app.route('/balance-due') 
def balance_due():
    """Balance due page"""
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    # Mock balance due data
    balance_data = [
        {'customer': 'John Doe', 'amount': 150.50, 'days_overdue': 5},
        {'customer': 'Jane Smith', 'amount': 75.25, 'days_overdue': 12},
    ]
    
    dashboard_data = get_dashboard_data()
    return render_template('balance_due.html', balances=balance_data, data=dashboard_data)

@app.route('/settings')
def settings():
    """Settings page"""
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    return render_template('settings.html')

@app.route('/help')
def help_support():
    """Help & Support page"""
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    return render_template('help.html')

@app.route('/api/customers', methods=['GET', 'POST'])
def api_customers():
    """API endpoint for customers"""
    if not session.get('authenticated'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'POST':
        # Add new customer
        data = request.get_json()
        new_customer = {
            'id': len(CUSTOMERS) + 1,
            'name': data.get('name'),
            'phone': data.get('phone'),
            'email': data.get('email'),
            'address': data.get('address')
        }
        CUSTOMERS.append(new_customer)
        return jsonify(new_customer), 201
    
    return jsonify(CUSTOMERS)

@app.route('/api/deliveries', methods=['GET', 'POST'])
def api_deliveries():
    """API endpoint for deliveries"""
    if not session.get('authenticated'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'POST':
        data = request.get_json()
        # Add new delivery logic here
        return jsonify({'success': True, 'message': 'Delivery added successfully'})
    
    # Return deliveries data
    return jsonify({'deliveries': [], 'payments': []})

@app.route('/api/payments', methods=['POST'])
def api_payments():
    """API endpoint for recording payments"""
    if not session.get('authenticated'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    # Add payment recording logic here
    return jsonify({'success': True, 'message': 'Payment recorded successfully'})

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/order-details')
def order_details():
    """Order details page"""
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    order_id = request.args.get('id', '')
    
    # Find the order by ID
    order = None
    for o in ORDERS:
        if o['id'] == order_id:
            order = o
            break
    
    if not order:
        flash('Order not found', 'error')
        return redirect(url_for('orders'))
    
    return render_template('order_details.html', order=order)

@app.route('/drivers')
def drivers():
    """Driver management page"""
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    # Sample driver data
    drivers_data = [
        {
            'id': 1,
            'name': 'Rajesh Kumar',
            'phone': '+91 9876543210',
            'email': 'rajesh@delivery.com',
            'vehicleNumber': 'DL01AB1234',
            'area': 'Delhi NCR',
            'licenseNumber': 'DL1420110012345',
            'address': '123 Main Road, Delhi, India 110001',
            'status': 'available',
            'joinDate': '2023-01-15',
            'totalDeliveries': 245
        },
        {
            'id': 2,
            'name': 'Amit Singh',
            'phone': '+91 9123456789',
            'email': 'amit@delivery.com',
            'vehicleNumber': 'UP14CD5678',
            'area': 'Gurgaon - Delhi',
            'licenseNumber': 'UP1420110067890',
            'address': '456 Sector 15, Gurgaon, Haryana 122001',
            'status': 'busy',
            'joinDate': '2023-03-20',
            'totalDeliveries': 189
        }
    ]
    
    dashboard_data = get_dashboard_data()
    return render_template('drivers.html', drivers=drivers_data, data=dashboard_data)

@app.route('/expenses')
def expenses():
    """Expense tracker page"""
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    # Sample expense data
    expenses_data = [
        {
            'id': 1,
            'date': '2024-10-19',
            'item': 'Water Can',
            'quantity': 10,
            'unpaidQuantity': 10,
            'payments': []
        },
        {
            'id': 2,
            'date': '2024-10-18',
            'item': 'Tea',
            'quantity': 50,
            'unpaidQuantity': 30,
            'payments': [
                {'date': '2024-10-19', 'quantity': 20}
            ]
        }
    ]
    
    dashboard_data = get_dashboard_data()
    return render_template('expenses.html', expenses=expenses_data, data=dashboard_data)

@app.route('/reminders')
def reminders():
    """Reminders page"""
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    # Sample reminder data
    reminders_data = [
        {
            'id': 1,
            'title': 'Follow up with John Doe',
            'description': 'Customer inquiry about bulk order pricing',
            'due_date': '2024-10-21',
            'due_time': '10:00',
            'status': 'pending',
            'priority': 'high',
            'created_by': 'Admin User',
            'created_date': '2024-10-19'
        },
        {
            'id': 2,
            'title': 'Inventory restock check',
            'description': 'Check stock levels for popular items',
            'due_date': '2024-10-22',
            'due_time': '14:30',
            'status': 'pending',
            'priority': 'medium',
            'created_by': 'Admin User',
            'created_date': '2024-10-19'
        },
        {
            'id': 3,
            'title': 'Driver payment review',
            'description': 'Review pending driver payments for last week',
            'due_date': '2024-10-20',
            'due_time': '09:00',
            'status': 'completed',
            'priority': 'high',
            'created_by': 'Admin User',
            'created_date': '2024-10-18'
        }
    ]
    
    dashboard_data = get_dashboard_data()
    return render_template('reminders.html', reminders=reminders_data, data=dashboard_data)

@app.route('/api/reminders', methods=['GET', 'POST'])
def api_reminders():
    """API endpoint for reminders"""
    if not session.get('authenticated'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'POST':
        data = request.get_json()
        # Add new reminder logic here
        return jsonify({'success': True, 'message': 'Reminder added successfully'})
    
    # Return reminders data
    return jsonify({'reminders': []})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
