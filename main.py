
import json
from locale import currency
from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
# from flask_sqlalchemy import SQLAlchemy
from pip import main
import razorpay



app = Flask(__name__)
# db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'PAYMENT_APP'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payment.db'

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120) , nullable=False)
    name = db.Column(db.String(120) , nullable=False)
    amount = db.Column(db.String(120) , nullable=False)



@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        amount = request.form.get('amount')
        user = Users(email = email, name=name, amount=amount)
        db.session.add(user)
        db.session.commit()
        print(user)
        return redirect(url_for('pay' , id=user.id))
    return render_template('checkout.html')


@app.route('/pay/<id>', methods=['GET', 'POST'])
def pay(id):
    user = Users.query.filter_by(id=id).first()

    client = razorpay.Client(auth=("rzp_test_L5qGaTFk1cnq1b" , "6yDTuSjGh3jHEd5H3bP0izHE"))
    payment = client.order.create({'amount' : (int(user.amount) * 100), 'currency' : 'INR', 'payment_capture' : '1'})
    return render_template('pay.html', payment = payment)




@app.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('success.html')





if __name__=='__main__':
    app.debug = True
    db.create_all()
    app.run()
    FLASK_APP=main.py