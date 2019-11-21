import pandas as pd
from flask_wtf import FlaskForm
from wtformsparsleyjs import StringField, PasswordField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired, ValidationError, Required
from wtforms import SubmitField, TextField

house_furn_stat_dict = {}
house_fac_dict = {}
house_addr_dict = {}
flat_furn_stat_dict = {}
flat_fac_dict = {}
flat_addr_dict = {}

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
class HousePrice(FlaskForm):
    
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

    furn_main_list = []
    for i in range(len(Furn_Uniq)):
        furn_sub_list = []
        for j in range(2):
            furn_sub_list.append(Furn_Uniq[i])
        furn_main_list.append(tuple(furn_sub_list))

    fac_main_list = []
    for i in range(len(Fac_Uniq)):
        fac_sub_list = []
        for j in range(2):
            fac_sub_list.append(Fac_Uniq[i])
        fac_main_list.append(tuple(fac_sub_list))

    addr_main_list = []
    for i in range(len(addr_Uniq)):
        addr_sub_list = []
        for j in range(2):
            addr_sub_list.append(addr_Uniq[i])
        addr_main_list.append(tuple(addr_sub_list))
        
    

    df['Furnished_status'] = df['Furnished_status'].map(house_furn_stat_dict)
    df['Facing'] = df['Facing'].map(house_fac_dict)
    df['Address'] = df['Address'].map(house_addr_dict)
    No_of_Bedrooms = IntegerField('No of Bedrooms:',validators=[Required(), Length(min=0,max=2)])
    No_of_Bathrooms = IntegerField('No of Bathrooms:', validators=[Required(), Length(min=0,max=2)])
    No_of_Balconies = IntegerField('No of Balconies:', validators=[Required(), Length(min=0,max=1)])
    No_of_Poojarooms = IntegerField('No of Poojarooms:', validators=[Required(), Length(min=0,max=1)])
    Supr_Area = IntegerField('Super Area:', validators=[Required(), Length(min=0,max=10)])
    Carp_Area = IntegerField('Carpet Area:', validators=[Required(), Length(min=0,max=10)])
    Furn_status = SelectField('Furnishing Status:', choices=tuple(furn_main_list))
    Fac_status = SelectField('Facing:', choices=tuple(fac_main_list))
    Addrss = SelectField('Address:', choices=tuple(addr_main_list))
    submit = SubmitField('Predict', render_kw={"onclick": "checkform()"})
    

class FlatPrice(FlaskForm):
    
    df_flat = pd.read_csv("https://raw.githubusercontent.com/shravankumargottala/Hyderabad_House_Price_Prediction/master/Hyd_Flat_Apartment_House_Price.csv")
    
    Flat_Furn_Uniq = df_flat['Furnished_status'].unique()
    for j in range(len(Flat_Furn_Uniq)):
        flat_furn_stat_dict[Flat_Furn_Uniq[j]] = j

    Flat_Fac_Uniq = df_flat['Facing'].unique()
    
    for k in range(len(Flat_Fac_Uniq)):
        flat_fac_dict[Flat_Fac_Uniq[k]] = k  

    flat_addr_Uniq = df_flat['Address'].unique()
    for l in range(len(flat_addr_Uniq)):
        flat_addr_dict[flat_addr_Uniq[l]] = l

    furn_main_list = []
    for i in range(len(Flat_Furn_Uniq)):
        furn_sub_list = []
        for j in range(2):
            furn_sub_list.append(Flat_Furn_Uniq[i])
        furn_main_list.append(tuple(furn_sub_list))

    fac_main_list = []
    for i in range(len(Flat_Fac_Uniq)):
        fac_sub_list = []
        for j in range(2):
            fac_sub_list.append(Flat_Fac_Uniq[i])
        fac_main_list.append(tuple(fac_sub_list))

    addr_main_list = []
    for i in range(len(flat_addr_Uniq)):
        addr_sub_list = []
        for j in range(2):
            addr_sub_list.append(flat_addr_Uniq[i])
        addr_main_list.append(tuple(addr_sub_list))
        
    

    df_flat['Furnished_status'] = df_flat['Furnished_status'].map(house_furn_stat_dict)
    df_flat['Facing'] = df_flat['Facing'].map(house_fac_dict)
    df_flat['Address'] = df_flat['Address'].map(house_addr_dict)
    No_of_Bedrooms = IntegerField('No of Bedrooms:',validators=[InputRequired()])
    No_of_Bathrooms = IntegerField('No of Bathrooms:', validators=[InputRequired()])
    No_of_Balconies = IntegerField('No of Balconies:', validators=[DataRequired()])
    No_of_Poojarooms = IntegerField('No of Poojarooms:', validators=[DataRequired()])
    Supr_Area = IntegerField('Super Area:', validators=[DataRequired()])
    Carp_Area = IntegerField('Carpet Area:', validators=[DataRequired()])
    Floor_No = IntegerField('Floor No:', validators=[DataRequired()])
    Total_Floors = IntegerField('Total Floors:', validators=[DataRequired()])
    Furn_status = SelectField('Furnishing Status:', choices=tuple(furn_main_list))
    Fac_status = SelectField('Facing:', choices=tuple(fac_main_list))
    Addrss = SelectField('Address:', choices=tuple(addr_main_list))
    submit = SubmitField('Predict', render_kw={"onclick": "checkform()"})
    
    
