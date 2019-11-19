from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, HousePrice, FlatPrice
import numpy as np
import pickle
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = '3a30940de5abdb36a69244f86b06ce81'

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

fac_dict = {}
status_dict = {}
Furn_stat_dict = {}
addr_dict = {}
Project = {}
Transaction = {}
Addr = {}
house_furn_stat_dict = {}
house_fac_dict = {}
house_addr_dict = {}
flat_furn_stat_dict = {}
flat_fac_dict = {}
flat_addr_dict = {}

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register")
def register():
    form = RegistarionForm()
    return render_template('register.html', title='Register', form=form)
@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

@app.route("/houseprice", methods=['GET', 'POST'])
def houseprice():
    form = HousePrice()
    return render_template('houseprice.html', title='Submit', form=form)

@app.route("/house_predict", methods=['GET', 'POST'])
def house_predict():
    form = HousePrice()
    model = pickle.load(open('House_Vill_model.pkl', 'rb'))

    df = pd.read_csv("https://raw.githubusercontent.com/shravankumargottala/Hyderabad_House_Price_Prediction/master/Hyd_Flat_Apartment_House_Price.csv")
    
    Furn_Uniq = df['Furnished_status'].unique()
    for j in range(len(Furn_Uniq)):
        house_furn_stat_dict[Furn_Uniq[j]] = j

    Fac_Uniq = df['Facing'].unique()
    
    for k in range(len(Fac_Uniq)):
        house_fac_dict[Fac_Uniq[k]] = k  

    addr_Uniq = df['Address'].unique()
    for l in range(len(addr_Uniq)):
        house_addr_dict[addr_Uniq[l]] = l
  
    if request.method == 'POST':
        no_of_bed = request.form['No_of_Bedrooms']
        no_of_bath = request.form['No_of_Bathrooms']
        no_of_bolc = request.form['No_of_Balconies']
        no_of_pooja = request.form['No_of_Poojarooms']
        sup_area = request.form['Supr_Area']
        car_area = request.form['Carp_Area']
        furn_status = request.form['Furn_status']
        house_facing = request.form['Fac_status']
        house_addres = request.form['Addrss']
        int_features =[no_of_bed,no_of_bath,no_of_bolc,no_of_pooja,sup_area,car_area,house_furn_stat_dict[furn_status],house_fac_dict[house_facing],house_addr_dict[house_addres]]
        final_features = [np.array(int_features)]
        prediction = model.predict(final_features)
        output = round(np.expm1(prediction[0]),2)

        return render_template('house_result.html', prediction_text='{} House Price for the below Specifications will be ₹ {}/- Lacs'.format(house_addres,output),no_of_bed_rooms='Flat type : {} BHK '.format(no_of_bed),sup_area='Super Area : {} sqft'.format(sup_area),car_area='Carpet Area : {} sqft'.format(car_area),house_facing='House Facing : {}'.format(house_facing),furn_status='Furnishing status: {}.'.format(furn_status),house_addres='House Address : {}, Hyderabad'.format(house_addres))
    
@app.route("/flatprice", methods=['GET', 'POST'])
def flatprice():
    form = FlatPrice()
    return render_template('flatprice.html', title='Submit', form=form)

@app.route("/flat_predict", methods=['GET', 'POST'])
def flat_predict():
    form = FlatPrice()
    model = pickle.load(open('hyd_flat_model.pkl', 'rb'))

    df_flat = pd.read_csv("https://raw.githubusercontent.com/shravankumargottala/Hyderabad_House_Price_Prediction/master/Hyd_Flat_Apartment_House_Price.csv")
    print(df_flat.shape)
    Flat_Furn_Uniq = df_flat['Furnished_status'].unique()
    for j in range(len(Flat_Furn_Uniq)):
        flat_furn_stat_dict[Flat_Furn_Uniq[j]] = j

    Flat_Fac_Uniq = df_flat['Facing'].unique()
    
    for k in range(len(Flat_Fac_Uniq)):
        flat_fac_dict[Flat_Fac_Uniq[k]] = k  

    Flat_addr_Uniq = df_flat['Address'].unique()
    for l in range(len(Flat_addr_Uniq)):
        flat_addr_dict[Flat_addr_Uniq[l]] = l
    print("flat_addr_dict is ",flat_addr_dict)
  
    if request.method == 'POST':
        no_of_bed = request.form['No_of_Bedrooms']
        no_of_bath = request.form['No_of_Bathrooms']
        no_of_bolc = request.form['No_of_Balconies']
        no_of_pooja = request.form['No_of_Poojarooms']
        sup_area = request.form['Supr_Area']
        car_area = request.form['Carp_Area']
        flr_no = request.form['Floor_No']
        print("floor number is ",flr_no)
        total_flrs = request.form['Total_Floors']
        print("total_flrs number is ",total_flrs)
        furn_status = request.form['Furn_status']
        print("furn_status number is ",furn_status)
        house_facing = request.form['Fac_status']
        print("house_facing is ",house_facing)
        house_addres = request.form['Addrss']
        print("house_addres is ",house_addres,flat_addr_dict[house_addres])
        int_features =[no_of_bed,no_of_bath,no_of_bolc,no_of_pooja,sup_area,car_area,flr_no,total_flrs,flat_furn_stat_dict[furn_status],flat_fac_dict[house_facing],flat_addr_dict[house_addres]]
        print("int_features is ",int_features)
        final_features = [np.array(int_features)]
        prediction = model.predict(final_features)
        output = round(np.expm1(prediction[0]),2)

        return render_template('flat_result.html', prediction_text='{} House Price for the below Specifications will be ₹ {}/- Lacs'.format(house_addres,output),no_of_bed_rooms='Flat type : {} BHK '.format(no_of_bed),sup_area='Super Area : {} sqft'.format(sup_area),car_area='Carpet Area : {} sqft'.format(car_area),house_facing='House Facing : {}'.format(house_facing),furn_status='Furnishing status: {}.'.format(furn_status),house_addres='House Address : {}, Hyderabad'.format(house_addres))
    
        
if __name__ == '__main__':
    app.run(debug=True)