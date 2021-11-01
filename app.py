import os
import requests
from flask import Flask, session, render_template, request, logging, url_for, flash, redirect
from flask_session import Session
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt
from datetime import datetime
from models import mycursor, db



app = Flask(__name__)
# Configure session to use filesystemsss
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# datetime object containing current date and time
now = datetime.now()
date = now.strftime("%d-%m-%Y %H:%M:%S")


@app.route("/" ,methods = ['GET','POST'])
def index():
    
     if request.method == "GET":
         if session.get("usser"):
             return render_template('index.htm', session=session["user"])
         return render_template('new.htm')

@app.route("/homes" ,methods = ['GET','POST'])
def homes():
    
     if request.method == "GET":
        return render_template('home.htm')


@app.route("/new" ,methods = ['GET','POST'])
def new():
    
     if request.method == "GET":
        return render_template('new.htm')

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        nrc = request.form.get("nrc")
        location = request.form.get("location")
        guardian = request.form.get("guardian")
        reference = request.form.get("reference")
        phone = request.form.get("phone")
        salary = request.form.get("salary")
        date = request.form.get("date")

        
        mycursor.execute("INSERT INTO employ (firstname, lastname ,nrc, location, guardian,reference,phone,salary,date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
                         (firstname, lastname ,nrc, location, guardian,reference,phone,salary,date))
        db.commit()

        flash("you successfully registered","success")
        return redirect(url_for('index'))
    
    return render_template("register.htm")

  
    
@app.route("/home",methods=['GET','POST'])
def home():

     if request.method == "GET":
         if session.get("usser"):
             return render_template('login.htm', session=session["user"])
         return render_template('login.htm')
       
     else:
        username = request.form.get("username")
        password = request.form.get("password")
        
        search = "SELECT username FROM users WHERE username = %(username)s  "
        mycursor.execute(search, {'username': username })
        pname= mycursor.fetchone()
        
        searched = "SELECT password FROM users WHERE username = %(username)s  "
        mycursor.execute(searched, {'username': username })
        passworddata= mycursor.fetchone()
        
        data = "SELECT password FROM users WHERE username = %(username)s  "
        mycursor.execute(data, {'username': username })
        userdata= mycursor.fetchone()
        '''
        pname ="SELECT username FROM users WHERE username=:username",{"username":username}).fetchone()
        passworddata =db.execute("SELECT password FROM users WHERE username= :username",{"username":username}).fetchone()
        userdata = db.execute("SELECT * FROM users WHERE username=:username",{"username":username}).fetchone()
        '''                      
        
        if pname is None:
            flash("No one with that name", "danger")
            return render_template("login.htm")
        else:
              for password_now in passworddata:            
                if sha256_crypt.verify(password,password_now):
                    session["user"]=userdata[0]
                    return render_template("admin.htm")
                else:
                    flash("incorrect password","danger")
                    return render_template("login.htm")
                


@app.route("/home/register", methods=['GET','POST'])
def createAdmin():
    if request.method == 'POST':
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        secure_password = sha256_crypt.encrypt(str(password))

        if password == confirm:
            mycursor.execute("INSERT INTO users (name, username , password) VALUES (%s,%s,%s)", (name, username, secure_password))
            db.commit()

            flash("you successfully registered and now you can login","success")
            return redirect(url_for('home'))
        else:
            flash("password does not match please re-enter information ","danger")
            return render_template("admin_register.htm")
   
    return render_template("admin_register.htm")




@app.route("/home/admin", methods=['GET','POST'])
def admin():
    if request.method == 'GET':
       return render_template('admin.htm')
   
    else:
        employee_nrc = request.form.get("nrc")
        employer_nrc= request.form.get("nrcs")
        
        if employee_nrc:
          search = "SELECT firstname, lastname ,nrc FROM employ WHERE nrc = %(nrc)s"
          mycursor.execute(search, {'nrc':  employee_nrc })
          myresult = mycursor.fetchall()
        
          if myresult == []:
            flash("No one with that NRC ", "danger")
            return redirect(url_for('admin'))
          else:    
            return render_template('admin.htm', employee = myresult)
        
        else:
            search = "SELECT name,nrc FROM employer WHERE nrc = %(nrc)s"
            mycursor.execute(search, {'nrc':  employer_nrc })
            myresult = mycursor.fetchall()
        
            if myresult == []:
              flash("No one with that NRC ", "danger")
              return redirect(url_for('home'))
            else:    
               return render_template('admin.htm', employer = myresult)
            
       
        

@app.route('/admin/employee/<int:nrc>', methods =['GET', 'POST'] )
def employee(nrc):
    
    search = "SELECT * FROM employ WHERE nrc = %(nrc)s"
    mycursor.execute(search, {'nrc': nrc })
    myresult = mycursor.fetchall()
    
    for result in myresult:
        reference = result[6]
   
    if request.method == 'GET':
         searched = "SELECT * FROM employer WHERE reference = %(reference)s"
         mycursor.execute(searched, {'reference': reference })
         employer = mycursor.fetchall()
         return render_template('employee.htm', employee = myresult, employer = employer)
    
   
   

@app.route('/admin/employer/<int:nrc>', methods =['GET', 'POST'] )
def employer(nrc):
    
    search = "SELECT * FROM employ WHERE nrc = %(nrc)s"
    mycursor.execute(search, {'nrc': nrc })
    myresult = mycursor.fetchall()
    for result in myresult:
            id = result[3]
    
    if request.method == 'POST':
        name = request.form.get("name")
        nrcs = request.form.get("nrc")
        location = request.form.get("location")
        occupation = request.form.get("occupation")
        reference = request.form.get("reference")
        phone = request.form.get("phone")
        salary = request.form.get("salary")
       

        
        mycursor.execute("INSERT INTO employer (name,nrc, location,occupation,reference,phone,payment_details) VALUES (%s,%s,%s,%s,%s,%s,%s)", 
                         (name, nrcs, location, occupation,reference,phone,salary,))
        db.commit()

        flash("you successfully added an employer","success")
        return redirect(url_for('employee',nrc = id))
        #render_template('employee.htm',employee = myresult)
           
    else:
        return render_template("employer.htm",id = id)
    
    
     
@app.route('/admin/employer/edit/<int:nrc>', methods =['GET', 'POST'] )
def edit(nrc):
    
    search = "SELECT * FROM employer WHERE nrc = %(nrc)s"
    mycursor.execute(search, {'nrc': nrc })
    myresult = mycursor.fetchall()
    for result in myresult:
        id = result[2]
    
    if request.method == 'POST':
        name = request.form.get("name")
        nrcs = request.form.get("nrc")
        location = request.form.get("location")
        occupation = request.form.get("occupation")
        reference = request.form.get("reference")
        phone = request.form.get("phone")
        salary = request.form.get("salary")
        reason = request.form.get('reason')
       

             
        sets = "UPDATE employer SET name = %(name)s,location=%(location)s,occupation=%(occupation)s,reference=%(reference)s,phone=%(phone)s,payment_details=%(payment_details)s,edit_reason=%(edit_reason)s,date_edited=%(date_edited)s WHERE nrc = %(nrc)s "
        mycursor.execute(sets, {'name':name,'location':location,'occupation':occupation,'reference':reference,'phone':phone,'payment_details':salary,'edit_reason':reason, 'date_edited': date, 'nrc':id })
        db.commit()
        
        flash("you successfully added an employer","success")
        return redirect(url_for('home'))
    
    else:
        return render_template("edit.htm", id = id)
    

       




@app.route('/admin/employers/<int:nrc>', methods =['GET', 'POST'] )
def employers(nrc):
    
    search = "SELECT * FROM employer WHERE nrc = %(nrc)s"
    mycursor.execute(search, {'nrc': nrc })
    myresult = mycursor.fetchall()
    for result in myresult:
            id = result[3]
    
    for result in myresult:
        reference = result[5]
   
    if request.method == 'GET':
         searched = "SELECT firstname,lastname,nrc FROM employ WHERE reference = %(reference)s"
         mycursor.execute(searched, {'reference': reference })
         employee = mycursor.fetchall()
         return render_template('employers.htm', employer = myresult, employee = employee)
     

@app.route('/admin/employer/add', methods =['GET', 'POST'] )
def addemployer():
    
    if request.method == 'POST':
        name = request.form.get("name")
        nrcs = request.form.get("nrc")
        location = request.form.get("location")
        occupation = request.form.get("occupation")
        reference = request.form.get("reference")
        phone = request.form.get("phone")
        salary = request.form.get("salary")
       

        
        mycursor.execute("INSERT INTO employer (name,nrc, location,occupation,reference,phone,payment_details) VALUES (%s,%s,%s,%s,%s,%s,%s)", 
                         (name, nrcs, location, occupation,reference,phone,salary,))
        db.commit()

        flash("you successfully added an employer","success")      
        return redirect(url_for('admin'))
           
    return render_template("add.htm")

    
@app.route('/admin/report', methods=['GET','POST'])
def report():
    
    if request.method == "POST":
       
        date1 = request.form.get("date")
        date2 = request.form.get("dates")
        
        sea = " SELECT * FROM employ WHERE  date BETWEEN  %s AND %s"
        mycursor.execute(sea, (date1, date2))
        myresult = mycursor.fetchall()
        
       
        return render_template('report.htm', employee = myresult)      
  
    

if __name__ == "__main__":
    app.secret_key='\x8a\x02\xe2\xed/\xee\xf1#\xbea\xd1\x02\xab|\xa5n'
    app.run(debug=True)












