from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, HousePrice, FlatPrice, PlotPrice
import numpy as np
import pickle
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = '3a30940de5abdb36a69244f86b06ce81'

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
    return render_template('home.html')


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

    df = pd.read_csv("https://raw.githubusercontent.com/shravankumargottala/Hyderabad_House_Price_Prediction/master/Hyd_House_Vill_Price.csv")
    
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
        if form.validate() == False :
            return render_template('houseprice.html', form=form)
        else:
            no_of_bed = request.form['No_of_Bedrooms']
            no_of_bath = request.form['No_of_Bathrooms']
            no_of_bolc = request.form['No_of_Balconies']
            no_of_pooja = request.form['No_of_Poojarooms']
            sup_area = request.form['Supr_Area']
            car_area = request.form['Carp_Area']
            furn_status = request.form['Furn_status']
            house_facing = request.form['Fac_status']
            house_addres = request.form['Addrss']
            int_features =[no_of_bed,no_of_bath,no_of_bolc,no_of_pooja,sup_area,car_area,
                           house_furn_stat_dict[furn_status],house_fac_dict[house_facing],
                           house_addr_dict[house_addres]]
            final_features = [np.array(int_features)]
            prediction = model.predict(final_features)
            output = round(np.expm1(prediction[0]),2)

            return render_template('house_result.html', 
                                   prediction_text='{} House Price for the below Specifications will be ₹ {}/- Lacs'.format(house_addres,output),
                                   no_of_bed_rooms='House type : {} BHK '.format(no_of_bed),
                                   sup_area='Super Area : {} sqft'.format(sup_area),
                                   car_area='Carpet Area : {} sqft'.format(car_area),
                                   house_facing='House Facing : {}'.format(house_facing),
                                   furn_status='Furnishing status: {}.'.format(furn_status),
                                   house_addres='House Address : {}, Hyderabad'.format(house_addres))

@app.route("/flatprice", methods=['GET', 'POST'])
def flatprice():
    form = FlatPrice()
    return render_template('flatprice.html', title='Submit', form=form)

@app.route("/flat_predict", methods=['GET', 'POST'])
def flat_predict():
    form = FlatPrice()
    model = pickle.load(open('hyd_flat_model.pkl', 'rb'))

    df_flat = pd.read_csv("https://raw.githubusercontent.com/shravankumargottala/Hyderabad_House_Price_Prediction/master/Hyd_Flat_Apartment_House_Price.csv")
    Flat_Furn_Uniq = df_flat['Furnished_status'].unique()
    for j in range(len(Flat_Furn_Uniq)):
        flat_furn_stat_dict[Flat_Furn_Uniq[j]] = j

    Flat_Fac_Uniq = df_flat['Facing'].unique()
    
    for k in range(len(Flat_Fac_Uniq)):
        flat_fac_dict[Flat_Fac_Uniq[k]] = k  

    Flat_addr_Uniq = df_flat['Address'].unique()
    for l in range(len(Flat_addr_Uniq)):
        flat_addr_dict[Flat_addr_Uniq[l]] = l
  
    if request.method == 'POST':
        if form.validate() == False :
            return render_template('flatprice.html', form=form)
        else:

            no_of_bed = request.form['No_of_Bedrooms']
            no_of_bath = request.form['No_of_Bathrooms']
            no_of_bolc = request.form['No_of_Balconies']
            no_of_pooja = request.form['No_of_Poojarooms']
            sup_area = request.form['Supr_Area']
            car_area = request.form['Carp_Area']
            flr_no = request.form['Floor_No']
            total_flrs = request.form['Total_Floors']
            furn_status = request.form['Furn_status']
            house_facing = request.form['Fac_status']
            house_addres = request.form['Addrss']
            int_features =[no_of_bed,no_of_bath,no_of_bolc,no_of_pooja,sup_area,car_area,
                           flr_no,total_flrs,flat_furn_stat_dict[furn_status],
                           flat_fac_dict[house_facing],flat_addr_dict[house_addres]]
            final_features = [np.array(int_features)]
            prediction = model.predict(final_features)
            output = round(np.expm1(prediction[0]),2)

            return render_template('flat_result.html', prediction_text='{} Flat Price for the below Specifications will be ₹ {}/- Lacs'.format(house_addres,output),
                                   no_of_bed_rooms='Flat type : {} BHK '.format(no_of_bed),
                                   sup_area='Super Area : {} sqft'.format(sup_area),
                                   car_area='Carpet Area : {} sqft'.format(car_area),
                                   house_facing='Flat Facing : {}'.format(house_facing),
                                   furn_status='Furnishing status: {}.'.format(furn_status),
                                   house_addres='Flat Address : {}, Hyderabad'.format(house_addres))
        

@app.route("/plotprice", methods=['GET', 'POST'])
def plotprice():
    form = PlotPrice()
    return render_template('plotprice.html', title='Submit', form=form)

Plot_Transaction_Dict = {}
Plot_Project_Dict = {}
Plt_Addr_Dict = {}
@app.route("/plot_predict", methods=['GET', 'POST'])
def plot_predict():
    form = PlotPrice() 
    
    df = pd.read_csv("https://raw.githubusercontent.com/shravankumargottala/Hyderabad_House_Price_Prediction/master/Hyd_Plot_Price.csv")
    
    Plot_Project_Unq = df.Project_Name.unique()
    for i in range(len(Plot_Project_Unq)):
        Plot_Project_Dict[Plot_Project_Unq[i]] = i
        
    
    Plot_Transaction_Unq = df.Transaction_Type.unique()
    for i in range(len(Plot_Transaction_Unq)):
        Plot_Transaction_Dict[Plot_Transaction_Unq[i]] = i
    


    Plot_Address_Unq = df.Address.unique()
    for i in range(len(Plot_Address_Unq)):
        Plt_Addr_Dict[Plot_Address_Unq[i]] = i
    
    model = pickle.load(open('Plot_model.pkl', 'rb'))
    if request.method == 'POST':
        if form.validate() == False :
            return render_template('plotprice.html', form=form)
        else:
            prj_name = request.form['Soci_Name']
            plt_area = request.form.get('Plt_Area')
            trn_type = request.form['Trans_Type']
            addre = request.form['Addrss']
            int_features =[Plot_Project_Dict[prj_name],plt_area,Plot_Transaction_Dict[trn_type],Plt_Addr_Dict[addre]]
            final_features = [np.array(int_features)]
            prediction = model.predict(final_features)

            output = round(np.expm1(prediction[0]),2)
	   
	   
        return render_template('plot_result.html', prediction_text='{} Plot Price for the below Specifications will be ₹ {}/- Lacs'.format(addre,output),proj_name='Project Name : {}.'.format(prj_name),plot_area='Plot Area : {} sqr-yards '.format(plt_area),trans_type='Transaction Type : {}.'.format(trn_type),plot_addres='Plot Address : {}, Hyderabad.'.format(addre))
        
        
if __name__ == '__main__':
    app.run(debug=True)
