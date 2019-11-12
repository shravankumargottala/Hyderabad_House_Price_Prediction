import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import pymsgbox

app = Flask(__name__)
alert = ""
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
@app.route('/',methods=['GET','POST'])
def home():
    return render_template('Main_Menu.html')
@app.route('/House',methods=['GET','POST'])
def house():
    if request.method == 'POST':
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
        
        df['Furnished_status'] = df['Furnished_status'].map(house_furn_stat_dict)
        df['Facing'] = df['Facing'].map(house_fac_dict)
        df['Address'] = df['Address'].map(house_addr_dict)
        
        return render_template('House.html',Furn_Uniq=Furn_Uniq,Fac_Uniq=Fac_Uniq,addr_Uniq=addr_Uniq)
@app.route('/Plot',methods=['GET','POST'])
def plot():
    if request.method == 'POST':
        df = pd.read_csv("https://raw.githubusercontent.com/shravankumargottala/Hyderabad_House_Price_Prediction/master/Hyd_Plot_Price.csv")
        
        Project_Unq = df.Project_Name.unique()
        for i in range(len(Project_Unq)):
            Project[Project_Unq[i]] = i
           
        
        Transaction_Unq = df.Transaction_Type.unique()
        for i in range(len(Transaction_Unq)):
            Transaction[Transaction_Unq[i]] = i
           
        
        Address_Unq = df.Address.unique()
        for i in range(len(Address_Unq)):
            Addr[Address_Unq[i]] = i
        print("Values is ",Address_Unq) 
        df['Project_Name'] = df['Project_Name'].map(Project)
        df['Transaction_Type'] = df['Transaction_Type'].map(Transaction)
        df['Address'] = df['Address'].map(Addr)
            
        return render_template('Plot.html',Project_Unq=Project_Unq,Transaction_Unq=Transaction_Unq,Address_Unq=Address_Unq)
@app.route('/Flat',methods=['GET','POST'])
def flat():
    if request.method == 'POST':
        df = pd.read_csv("https://raw.githubusercontent.com/shravankumargottala/Hyderabad_House_Price_Prediction/master/Hyd_Flat_Apartment_House_Price.csv")
        
        Furn_Uniq = df['Furnished_status'].unique()
        for j in range(len(Furn_Uniq)):
            Furn_stat_dict[Furn_Uniq[j]] = j

        Fac_Uniq = df['Facing'].unique()
        for k in range(len(Fac_Uniq)):
            fac_dict[Fac_Uniq[k]] = k

        addr_Uniq = df['Address'].unique()
        for l in range(len(addr_Uniq)):
            addr_dict[addr_Uniq[l]] = l

        df['Furnished_status'] = df['Furnished_status'].map(Furn_stat_dict)
        df['Facing'] = df['Facing'].map(fac_dict)
        df['Address'] = df['Address'].map(addr_dict)

        return render_template('Flat.html',Furn_Uniq=Furn_Uniq,Fac_Uniq=Fac_Uniq,addr_Uniq=addr_Uniq)

@app.route('/flat_predict',methods=['POST'])
def flat_predict():
    '''
    For rendering results on HTML GUI
    '''
    
    model = pickle.load(open('hyd_flat_model.pkl', 'rb'))
    if request.method == 'POST':
        no_of_bed = request.form['no_bed']
        no_of_bath = request.form['no_bath']
        no_of_bolc = request.form['no_balc']
        no_of_pooja = request.form['no_pooja']
        sup_area = request.form['sup_ar']
        car_area = request.form['car_ar']
        flr_nos = request.form['flr_no']
        total_flr_nos = request.form['total_flr_no']
        furn_status = request.form['furn_stat']
        flat_fac = request.form['flat_facing']
        flat_addres = request.form['addr']
        if int(car_area) > int(sup_area) :
            print("entered")
            pymsgbox.alert('Carper area is greater than the Super area', 'Title')
            #request.form['flr_no'] = ""
        int_features =[no_of_bed,no_of_bath,no_of_bolc,no_of_pooja,sup_area,car_area,flr_nos,total_flr_nos,Furn_stat_dict[furn_status],fac_dict[flat_fac],addr_dict[flat_addres]]
        final_features = [np.array(int_features)]
        prediction = model.predict(final_features)

        output = round(np.expm1(prediction[0]),2)
	   
	   
        return render_template('result.html', prediction_text='{} Flat Price for the below Specifications will be ₹ {}/- Lacs'.format(flat_addres,output),no_of_bed_rooms='Flat type : {} BHK '.format(no_of_bed),sup_area='Super Area : {} sqft'.format(sup_area),car_area='Carpet Area : {} sqft'.format(car_area),flat_fac='Flat Facing : {}'.format(flat_fac),flat_addres='Flat Address : {}, Hyderabad'.format(flat_addres))
   
@app.route('/house_predict',methods=['POST'])
def house_predict():
    '''
    For rendering results on HTML GUI
    '''
    
    model = pickle.load(open('House_Vill_model.pkl', 'rb'))
    if request.method == 'POST':
        no_of_bed = request.form['no_bed']
        no_of_bath = request.form['no_bath']
        no_of_bolc = request.form['no_balc']
        no_of_pooja = request.form['no_pooja']
        sup_area = request.form['sup_ar']
        car_area = request.form['car_ar']
        furn_status = request.form['furn_stat']
        house_facing = request.form['house_facing']
        house_addres = request.form['addr']
        int_features =[no_of_bed,no_of_bath,no_of_bolc,no_of_pooja,sup_area,car_area,house_furn_stat_dict[furn_status],house_fac_dict[house_facing],house_addr_dict[house_addres]]
        final_features = [np.array(int_features)]
        prediction = model.predict(final_features)

        output = round(np.expm1(prediction[0]),2)
	   
	   
        return render_template('house_result.html', prediction_text='{} House Price for the below Specifications will be ₹ {}/- Lacs'.format(house_addres,output),no_of_bed_rooms='Flat type : {} BHK '.format(no_of_bed),sup_area='Super Area : {} sqft'.format(sup_area),car_area='Carpet Area : {} sqft'.format(car_area),house_facing='House Facing : {}'.format(house_facing),house_addres='House Address : {}, Hyderabad'.format(house_addres))
   
@app.route('/plot_predict',methods=['POST'])
def plot_predict():
    model = pickle.load(open('Plot_model.pkl', 'rb'))
    if request.method == 'POST':
        prj_name = request.form['prj_name']
        plt_area = request.form.get('plt_area')
        trn_type = request.form['trn_type']
        addre = request.form['addre']
        int_features =[Project[prj_name],plt_area,Transaction[trn_type],Addr[addre]]
        final_features = [np.array(int_features)]
        prediction = model.predict(final_features)

        output = round(np.expm1(prediction[0]),2)
	   
	   
        return render_template('plot_result.html', prediction_text='{} Plot Price for the below Specifications will be ₹ {}/- Lacs'.format(addre,output),proj_name='Project Name : {}.'.format(prj_name),plot_area='Plot Area : {} sqr-yards '.format(plt_area),trans_type='Transaction Type : {}.'.format(trn_type),plot_addres='Plot Address : {}, Hyderabad.'.format(addre))
   

if __name__ == "__main__":
    app.debug = True
    app.run()
