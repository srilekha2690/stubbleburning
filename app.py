from asyncio.windows_events import NULL
from pyparsing import null_debug_action
import pyrebase
from firebase import firebase
from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np
import pandas as pd
from joblib import load

firebaseConfig = {
  "apiKey": "AIzaSyAFsp5wFnuF0R_URada7GTaWflHKO9VuU8",
  "authDomain": "stubble-burning.firebaseapp.com",
  "databaseURL": "https://stubbleprice-default-rtdb.firebaseio.com/",
  "projectId": "stubble-burning",
  "storageBucket": "stubble-burning.appspot.com",
  "messagingSenderId": "737770959427",
  "appId": "1:737770959427:web:5a083fbe7e7130ce4e1af6",
  "measurementId": "G-FR7EM1PW98"
}

FBConn = firebase.FirebaseApplication("https://stubbleprice-default-rtdb.firebaseio.com/", None)
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()


app = Flask(__name__)
app.secret_key = "hello"


@app.route("/", methods=['GET', 'POST'])
def price_prediction():
    request_type_str = request.method
    if request_type_str == 'GET':
        return render_template('predictor.html')
    else:
         fertilizer = request.form.get('fertilizer')
         crop_type = request.form.get('crop_type')
         soil_type = request.form.get('soil_type')
         month = request.form.get('month')
         removal_type = request.form.get('removal_type')
         state = request.form.get('state')

         if fertilizer.lower() == "yes":
                fertilizer = 1
         else:
                fertilizer = 0              
         if crop_type.lower() == "rice":
                Rice = 1
         if soil_type.lower() == "black":
                Black = 1
                Red = 0
         else:
                Red=1
                Black=0
         if month.lower() == "oct-dec":
                Oct = 1
                May = 0
         else:
                May = 1
                Oct = 0
         if removal_type.lower() == "machine":
                Machine = 1
                Labour = 0
         else:
                Labour = 1
                Machine = 0
         if state.lower() == "maharashtra":
                Maharashtra = 1
                Andhra = 0
         else:
                Andhra = 1
                Maharashtra = 0
       
         features = ['FERTILIZER','Rice','Black','Red','May','Oct','Labour','Machine','Andhra','Maharastra']
         stubble = [fertilizer, Rice, Black, Red, May, Oct, Labour, Machine, Andhra, Maharashtra]
         features_value = [np.array(stubble)]
         df = pd.DataFrame(features_value, columns=features)
         model = load('model.joblib')
         preds = model.predict(df)
         preds_as_str = str(preds).strip('[]')
         return render_template('predictor.html', prediction = preds_as_str)


@app.route('/home', methods=["GET", "POST"])
def home_page():
       return render_template('index_2.html')  

@app.route('/freg', methods=["GET", "POST"])
def farmreg():
       return render_template('freg.html')  


@app.route('/custreg',methods=['GET','POST'])
def customer_reg():
	if request.method == 'POST':
			print("hello")
			name = request.form['name']
			number = request.form['number']
			email = request.form['email']
			address = request.form['address']
			password = request.form['pass']
			customer = "customer"
			data_to_upload = {
				'Name': name,
				'Phone Number': number,
				'Email id': email,
				'Address' : address,
				'Password': password,
                 'type' : customer,
			}
			print(data_to_upload)
			result = FBConn.post('/user_data/', data_to_upload)
			print(result)
			return redirect(url_for('login'))
	return render_template('index.html')

	
# @app.route("/predictor", methods=['GET', 'POST'])
# def price_prediction():
#     request_type_str = request.method
#     if request_type_str == 'GET':
#         return render_template('predictor.html')
#     else:
#          fertilizer = request.form.get('fertilizer')
#          crop_type = request.form.get('crop_type')
#          soil_type = request.form.get('soil_type')
#          month = request.form.get('month')
#          removal_type = request.form.get('removal_type')
#          state = request.form.get('state')

#          if fertilizer.lower() == "yes":
#                 fertilizer = 1
#          else:
#                 fertilizer = 0              
#          if crop_type.lower() == "rice":
#                 Rice = 1
#          if soil_type.lower() == "black":
#                 Black = 1
#                 Red = 0
#          else:
#                 Red=1
#                 Black=0
#          if month.lower() == "oct-dec":
#                 Oct = 1
#                 May = 0
#          else:
#                 May = 1
#                 Oct = 0
#          if removal_type.lower() == "machine":
#                 Machine = 1
#                 Labour = 0
#          else:
#                 Labour = 1
#                 Machine = 0
#          if state.lower() == "maharashtra":
#                 Maharashtra = 1
#                 Andhra = 0
#          else:
#                 Andhra = 1
#                 Maharashtra = 0
       
#          features = ['FERTILIZER','Rice','Black','Red','May','Oct','Labour','Machine','Andhra','Maharastra']
#          stubble = [fertilizer, Rice, Black, Red, May, Oct, Labour, Machine, Andhra, Maharashtra]
#          features_value = [np.array(stubble)]
#          df = pd.DataFrame(features_value)
#          model = load('model.joblib')
#          preds = model.predict(df)
#          preds_as_str = str(preds).strip('[]')
#     return render_template('predictor.html', prediction = preds_as_str)




@app.route('/customerfeed', methods=["GET", "POST"])
def customerfeed():
       return render_template('shop.html')

@app.route('/login', methods=["GET", "POST"])
def login():
	result = FBConn.get('/user_data/',None)
	print(result)
	if request.method == 'POST':
		# if request.form['submit'] == 'submit':
			number1 = request.form['number']
			session["user"] = number1
			password1 = request.form['pass']
			#cust = request.form.get('cust')
			print("hello")
			for i in result:
				a = result[i]['Phone Number']
				b = result[i]['Password']
				if number1 == a and password1 == result[i]['Password']:
					c = result[i]['type']
					if c == "farmer":
						return redirect(url_for('farmerfeed'))
					elif c == "customer":
						return redirect(url_for('card'))
	return render_template('login.html')


# @app.route('/try',methods=['GET','POST'])
# def try1():
# 	name1 = []
# 	tel = []       
# 	email1 = []
# 	if request.method == 'POST':
# 			print("hello")
# 			name1.append(request.form['name'])
# 			tel.append(request.form['tel'])
# 			email1.append(request.form['email'])
# 	return render_template('card.html', total_details=zip(name1,tel,email1))       




#### farmer dashboard ####

@app.route('/ffeed',methods=['GET', 'POST'])
def ffeed():
	return render_template('farmer-dashboard.html')


##### new farmer upload details #####
@app.route('/fupload',methods=['GET','POST'])
def upload():
	if request.method == 'POST':
			print("hello")
			name1 = request.form['name']
			tel = request.form['tel']
			price = request.form['price']
			quantity = request.form['quantity']
			loc = request.form['location']
			type1 = request.form['type']
			data_to_upload = {
				'Name': name1,
				'Phone Number': tel,
				'price': price,
				'quantity': quantity,
				'location': loc,
				'type1' : type1,
			}
			print(data_to_upload)
			result = FBConn.post('/stubble_data/', data_to_upload)
			print(result)
			# return redirect(url_for('login'))
	return render_template('farm-upload.html')        





# @app.route('/card', methods=['GET','POST'])
# def card():

#        return render_template('card.html')


@app.route('/shop',methods=['POST','GET'])
def shop():
	if request.method == 'POST':
			print("hello")
			stubble = request.form['type']
			price = request.form['price']
			data_to_upload = {
				'stubble': stubble,
				'price': price,
			}
			print(data_to_upload)
			result = FBConn.post('/transaction_data/', data_to_upload)
			print(result)

	# if request.method == 'POST':
	# 	stubble = request.form['type']
	# 	price = request.form['price']
	# 	data_to_upload = {
	# 		'Customer name' : name,
	# 		'stubble' : stubble,
	# 		'price' : price,
	# 		}
	# 	result = FBConn.post('/transaction_data/', data_to_upload)
	# 	print(result)
	# 	return redirect(url_for('shop'))       
	
	name_user=[]
	price=[]
	Tele=[]
	type1=[]
	Quantity=[]
	Location=[]
    
	stubble_data = FBConn.get('/stubble_data/',None)
	
	for i in stubble_data:
			name_user.append(stubble_data[i]['Name'])
			price.append(stubble_data[i]['price'])
			Tele.append(stubble_data[i]['Phone Number'])
			Quantity.append(stubble_data[i]['quantity'])
			type1.append(stubble_data[i]['type1'])
			Location.append(stubble_data[i]['location'])

	# if request.form['Quantity'] != "0" and request.method == 'POST':
		
	return render_template('shop.html',total_details=zip(type1,price,Quantity,name_user,Tele,Location))


@app.route('/cart',methods=['GET','POST'])
def cart():
	
	
	user_data = FBConn.get('/user_data/',None)
	email_id=""
	name=""

	if "user" in session:
		email_id = session["user"]

	for i in user_data:
		if email_id == user_data[i]['Phone Number']:	
			name = user_data[i]['Name']
			#emails = user_data[i]['Email id']
	for j in user_data:
		#phones = user_data[j]['Phone Number']
		types = user_data[j]['type']
       
	price=[]
	stubble=[]
       
	# transaction_data = FBConn.get('/transaction_data/',None)
	# for i in transaction_data:
	# 	if name == transaction_data[i]['Customer name']:
	# 		stubble.append(transaction_data[i]['stubble'])
	# 		price.append(transaction_data[i]['price'])
	# 		print("hello")

	return render_template('cart.html')
	# return render_template('cart.html',total_details=zip(stubble,price))





########### old #################


@app.route('/card',methods=['GET','POST'])
def card():
	user_data = FBConn.get('/user_data/',None)
	email_id=""
	name=""

	if "user" in session:
		email_id = session["user"]

	for i in user_data:
		if email_id == user_data[i]['Phone Number']:	
			name = user_data[i]['Name']
			#emails = user_data[i]['Email id']
	for j in user_data:
		#phones = user_data[j]['Phone Number']
		types = user_data[j]['type']

	if request.method == 'POST':
		print('hello')
		stubble = request.form['type']
		price = request.form['price']
		data_to_upload = {
			'Customer name' : name,
			'stubble' : stubble,
			'price' : price,
			}
		result = FBConn.post('/transaction_data/', data_to_upload)
		print(result)
		return redirect(url_for('card'))
	
       
	
	name_user=[]
	price=[]
	Tele=[]
	type1=[]
	Quantity=[]
	Location=[]
    
	stubble_data = FBConn.get('/stubble_data/',None)
	
	for i in stubble_data:
			name_user.append(stubble_data[i]['Name'])
			price.append(stubble_data[i]['price'])
			Tele.append(stubble_data[i]['Phone Number'])
			Quantity.append(stubble_data[i]['quantity'])
			type1.append(stubble_data[i]['type1'])
			Location.append(stubble_data[i]['location'])

	# if request.form['Quantity'] != "0" and request.method == 'POST':
		
	return render_template('card.html',total_details=zip(type1,price,Quantity,name_user,Tele,Location))


@app.route('/cart1',methods=['GET','POST'])
def cart1():
	
	
	user_data = FBConn.get('/user_data/',None)
	email_id=""
	name=""

	if "user" in session:
		email_id = session["user"]

	for i in user_data:
		if email_id == user_data[i]['Phone Number']:	
			name = user_data[i]['Name']
			#emails = user_data[i]['Email id']
	for j in user_data:
		#phones = user_data[j]['Phone Number']
		types = user_data[j]['type']
       
	price=[]
	stubble=[]
       
	# transaction_data = FBConn.get('/transaction_data/',None)
	# for i in transaction_data:
	# 	if name == transaction_data[i]['Customer name']:
	# 		stubble.append(transaction_data[i]['stubble'])
	# 		price.append(transaction_data[i]['price'])
	# 		print("hello")

	return render_template('cart1.html')
	# return render_template('cart.html',total_details=zip(stubble,price))


####################

	# for i in stubble_data:
	# 		name2 = stubble_data[i]['Name']
	# 		Email2 = stubble_data[i]['Email id']
	# 		Tele2 = stubble_data[i]['Phone Number']
	# 		Quantity = request.form['Quantity']
	# 		if request.method == 'POST' and Quantity != NULL:
	# 			data_to_upload = {
	# 				'Name': name2,
	# 				'Phone Number': Tele2,
	# 				'Email id': Email2,
	# 				'Quantity': Quantity,
	# 			}
	# 			print(data_to_upload)
	# 			result = FBConn.post('/cart_data/', data_to_upload)
	# 			print(result)


############




	# user_data = FBConn.get('/user_data/',None)

	# if "user" in session:
	# 	email_id = session["user"]
	# 	print(email_id)
	
	


if __name__ == '__main__':
	app.run(debug=True)
