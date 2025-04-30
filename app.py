from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Set up database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'orders.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(100))
    order_id = db.Column(db.String(50))
    product = db.Column(db.String(100))
    status = db.Column(db.String(50))

# Home route
@app.route('/')
def home():
    orders = Order.query.all()
    return render_template('home.html', orders=orders)

# Add order route
@app.route('/add', methods=['POST'])
def add_order():
    new_order = Order(
        customer=request.form['customer'],
        order_id=request.form['order_id'],
        product=request.form['product'],
        status=request.form['status']
    )
    db.session.add(new_order)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_order(id):
    order = Order.query.get_or_404(id)
    if request.method == 'POST':
        order.customer = request.form['customer']
        order.order_id = request.form['order_id']
        order.product = request.form['product']
        order.status = request.form['status']
        db.session.commit()
        return redirect('/')
    return render_template('edit.html', order=order)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
