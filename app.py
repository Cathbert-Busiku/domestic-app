import os
import requests
from flask import Flask, session, render_template, request, logging, url_for, flash, redirect,Response
from flask_session import Session
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt
from datetime import datetime
from fpdf import FPDF
import smtplib
from database import mycursor, db
# from model import mycursor, db




app = Flask(__name__)
# Configure session to use filesystemsss
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# datetime object containing current date and time
now = datetime.now()
dates = now.strftime("%d-%m-%Y %H:%M:%S")


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
        return render_template('index.htm')

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get("name")
        nrcs = request.form.get("nrc")
        location = request.form.get("location")
        occupation = request.form.get("occupation")
        reference = request.form.get("reference")
        phone = request.form.get("phone")
        salary = request.form.get("salary")
       
        search = "SELECT nrc FROM employer WHERE nrc = %(nrc)s"
        mycursor.execute(search, {'nrc': nrcs })
        myresult = mycursor.fetchone()
        
        if myresult is None:
            mycursor.execute("INSERT INTO employer (name,nrc, location,occupation,reference,phone,payment_details) VALUES (%s,%s,%s,%s,%s,%s,%s)", 
                         (name, nrcs, location, occupation,reference,phone,salary,))
            db.commit()
        
            flash("you successfully registered","success")
            return redirect(url_for('index'))
         
        if int(nrcs) == int(myresult[0]): 
                
            flash("The NRC is already registered","danger")
            return render_template('register.htm')
            
        
    return render_template("register.htm")

        
        
        # firstname = request.form.get("firstname")
        # lastname = request.form.get("lastname")
        # nrc = request.form.get("nrc")
        # location = request.form.get("location")
        # guardian = request.form.get("guardian")
        # reference = request.form.get("reference")
        # phone = request.form.get("phone")
        # salary = request.form.get("salary")
        # date = request.form.get("date")

        
        # mycursor.execute("INSERT INTO employ (firstname, lastname ,nrc, location, guardian,reference,phone,salary,date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
        #                  (firstname, lastname ,nrc, location, guardian,reference,phone,salary,date))
        # db.commit()


  
    
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
              return redirect(url_for('admin'))
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
    
   
   

@app.route('/admin/addEmployee/<int:nrc>', methods =['GET', 'POST'] )
def employer(nrc):
    
    search = "SELECT * FROM employ WHERE nrc = %(nrc)s"
    mycursor.execute(search, {'nrc': nrc })
    myresult = mycursor.fetchall()
    for result in myresult:
            id = result[3]
    
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
        
        search = "SELECT nrc FROM employ WHERE nrc = %(nrc)s"
        mycursor.execute(search, {'nrc': nrc })
        myresult = mycursor.fetchone()
        
        if myresult is None:
           mycursor.execute("INSERT INTO employ (firstname, lastname ,nrc, location, guardian,reference,phone,salary,date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
                         (firstname, lastname ,nrc, location, guardian,reference,phone,salary,date))
           db.commit()
        
           flash("you successfully added an employer","success")
           return redirect(url_for('employee',nrc = id))
         
        if int(nrc) == int(myresult[0]):             
            flash("The NRC is already registered","danger")
            return render_template('registerEmployee.htm')

    return render_template("registerEmployee.htm",id = id)
    
        
    
     
@app.route('/admin/employee/edit/<int:nrc>', methods =['GET', 'POST'] )
def edit(nrc):
    
    search = "SELECT * FROM employ WHERE nrc = %(nrc)s"
    mycursor.execute(search, {'nrc': nrc })
    myresult = mycursor.fetchall()
    for result in myresult:
        id = result[3]
    
    if request.method == 'POST':
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        location = request.form.get("location")
        guardian = request.form.get("guardian")
        reference = request.form.get("reference")
        phone = request.form.get("phone")
        salary = request.form.get("salary")
        date = request.form.get("date")
        reason = request.form.get('reason')
        
      
        sets = "UPDATE employ SET firstname = %(firstname)s,lastname = %(lastname)s, location = %(location)s,guardian=%(guardian)s,reference=%(reference)s,phone=%(phone)s,salary=%(salary)s,edit_reason=%(edit_reason)s, date = %(date)s, date_edited=%(date_edited)s WHERE nrc = %(nrc)s "
        mycursor.execute(sets, {'firstname':firstname,'lastname':lastname,'location':location,'guardian':guardian,'reference':reference,'phone':phone,'salary':salary,'edit_reason':reason, 'date':date,'date_edited': dates, 'nrc':id })
        db.commit()
        
        flash("you successfully edited an employer","success")
        return redirect(url_for('admin'))
    
    else:
        return render_template("editEmployee.htm", id = id)
    

       




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
     

@app.route('/admin/employee/add', methods =['GET', 'POST'] )
def addemployee():
    
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

        flash("you successfully added an employee","success")      
        return redirect(url_for('admin'))
           
    return render_template("addEmployee.htm")

    
@app.route('/admin/report', methods=['GET','POST'])
def report():
    
    if request.method == "POST":
       
        date1 = request.form.get("date")
        date2 = request.form.get("dates")
        content = request.form.get("access")
        
        if content  =='employ':
           sea = " SELECT * FROM employ WHERE  date BETWEEN  %s AND %s"
           mycursor.execute(sea, (date1, date2))
           myresult = mycursor.fetchall()
           
           amount = "SELECT SUM(salary) FROM employ" 
           mycursor.execute(amount)
           totalAmount = mycursor.fetchall()[0][0]
           
            
           return render_template('report.htm', employee = myresult, amount = totalAmount)
           
       
           
        # else: 
        #    sea = " SELECT * FROM employer WHERE  date BETWEEN  %s AND %s"
        #    mycursor.execute(sea, (date1, date2))
        #    myresult = mycursor.fetchall()
        #    return render_template('report.htm', employee = myresult)     

@app.route('/download/report/pdf')
def download_report():
      
        mycursor.execute("SELECT * FROM employ")
        result = mycursor.fetchall()
 
        pdf = FPDF()
        pdf.add_page()
         
        page_width = pdf.w - 2 * pdf.l_margin
         
        pdf.set_font('Arial','B',14.0) 
        pdf.cell(page_width, 0.0,'LINKUS MAID CENTER EMPLOYEE REPORT', align='C')
        pdf.ln(10)
 
        pdf.set_font('Courier', '', 10)
         
        col_width = page_width/8
         
        pdf.ln(1)
         
        th = pdf.font_size
        pdf.cell(col_width, th, 'First name', border=1)
        pdf.cell(col_width, th, 'Last name', border=1)
        pdf.cell(col_width, th, 'NRC', border=1)
        pdf.cell(col_width, th, 'Location', border=1)
        pdf.cell(col_width, th, 'Reference', border=1)
        pdf.cell(col_width, th, 'Phone', border=1)
        pdf.cell(col_width, th, 'Salary', border=1)
        pdf.cell(col_width, th, 'Date of start', border=1)
        pdf.ln(th)
         
        for row in result:
            pdf.cell(col_width, th, str(row[1]), border=1)
            pdf.cell(col_width, th, row[2], border=1)
            pdf.cell(col_width, th, str(row[3]), border=1)
            pdf.cell(col_width, th, row[4], border=1)
            pdf.cell(col_width, th, row[6], border=1)
            pdf.cell(col_width, th, str(row[7]), border=1)
            pdf.cell(col_width, th, str(row[8]), border=1)
            pdf.cell(col_width, th, row[9], border=1)
            pdf.ln(th)
         
        pdf.ln(10)
         
        pdf.set_font('Arial','',10.0) 
        pdf.cell(page_width, 0.0, '- end of report -', align='C')
         
        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=LINKUS MAID CENTER_report.pdf'})
   
@app.route('/email', methods=['GET','POST'])
def email():
    
    if request.method == "POST":
       
        names = request.form.get("name")
        address = request.form.get("email")
        heading = request.form.get("subject")
        content = request.form.get("message")
        
        app_pass = "nfenrszaqkbuerqt"
        host_user = "linkusmaidcenter@gmail.com"
        
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        
        smtp.login(host_user,app_pass)
        
        name = names
        Subject = heading.upper()
        Body = content
        msg = f"{Subject}\n\n{name}\n\n{Body}"
        
        return smtp.sendmail(address, host_user,msg)
        
         

if __name__ == "__main__":
    app.secret_key='\x8a\x02\xe2\xed/\xee\xf1#\xbea\xd1\x02\xab|\xa5n'
    app.run(debug=True)












