from flask import Flask
import pandas as pd_users_csv
import requests
import secrets
import string
from random import randint 

SEP=',' # separador de campo, automatic detect with engine python
USER_CSV_URL = 'https://docs.google.com/spreadsheets/d/1aZvrEPvNGssSAQjNLJz1XEDBqAOk4nLs/gviz/tq?tqx=out:csv' # Link users csv 
EPY='python' #Engine 
SR=0 # Skip Rows
ENDPOINT_USERS_REGISTER = 'http://localhost:3000/v1/register'

app = Flask(__name__)

def controller_users():
    user_data = pd_users_csv.read_csv(USER_CSV_URL,skiprows=SR,engine=EPY)
    for user in user_data.iterrows():
        rs_user ={}
        user_name=f"{user[1]['first_name'][:1].lower()}{user[1]['last_name'].lower()}"
        rs_user['first_name']=user[1]['first_name'].lower()
        rs_user['last_name']=user[1]['last_name'].lower()
        rs_user['name'] = user_name
        rs_user['email'] = f"{user_name}{domain_generate()}"
        rs_user['password'] = password_generate()
        #print(rs_user['password'], rs_user['first_name'],rs_user['last_name'], user_name, rs_user['email'])
        requests.post(ENDPOINT_USERS_REGISTER, rs_user)
    return {'status':'success','users':'users successfully registered','count':len(user_data)}

@app.route('/v1/users')
def users():
    res = controller_users()
    return res

def password_generate():
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation
    alphabet = letters + digits + special_chars
    pwd_length = 8 #Quantity chars of passwaord
    pwd = ''
    for i in range(pwd_length):
        pwd += ''.join(secrets.choice(alphabet))
    return pwd

def domain_generate(): 
    domains=['@hotmail.com','@gmail.com','@outlook.com','@yahoo.es']
    return domains[randint(0,3)]

if __name__ == '__main__':
    app.run(host='localhost', port=3001, debug=True)