from flask import Flask, render_template, redirect, session, flash, url_for, request
from flask_mysqldb import MySQL 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

app=Flask(__name__)

app.secret_key='karan420'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'KIRUBAkaran1234'
app.config['MYSQL_DB'] = 'student_data'
mysql = MySQL(app)

def isloggedin():
    return "user_id" in session

@app.route('/')
def home():
    
    return render_template('index.html')

@app.route('/dashbord')
def dashbord():
    if isloggedin():
        
        user_id=session['user_id']
        
        cur = mysql.connection.cursor()
        cur.execute('select * from details2 where id=%s',(user_id,))
        data=cur.fetchall()
        cur.close()
        
       
        return render_template('dashbord.html',data=data)
    

class User:
    def __init__(self, id, username, password):
        self.id=id
        self.username=username
        self.password=password
        
class signup_form(FlaskForm):
    username=StringField("username",validators=[InputRequired(), Length(min=4, max=20)])
    password=PasswordField('password',validators=[InputRequired(), Length(min=8, max=50)])
    submit=SubmitField('signup')
    
class login_form(FlaskForm):
    username=StringField("username",validators=[InputRequired(), Length(min=4, max=20)])
    password=PasswordField('password',validators=[InputRequired(), Length(min=8, max=50)])
    submit=SubmitField('login')

@app.route('/signup',methods=['GET','POST'])
def signup():
    
    form=signup_form()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
         
        cur = mysql.connection.cursor()
        cur.execute('select id from details where name=%s',(username,))
        old_user=cur.fetchone()
        
        if old_user:
            cur.close()
            flash('username already taken. please choose a different one.','danger')
            return render_template('signup.html',form=form)
        
        cur.execute('insert into details (name,password) values (%s, %s)',(username,password))
        mysql.connection.commit()
        cur.close()
        flash('signup successful', 'success')
        
        return redirect(url_for('login'))
    return render_template('signup.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    
    form=login_form()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        
        cur = mysql.connection.cursor()
        cur.execute('select id, name, password from details where name=%s',(username,))
        record=cur.fetchone()
        cur.close()
        
        if record and record[2]==password:
            user=User( id=record[0], username=record[1], password=record[2])
            session['user_id']=user.id
            
            flash('login successful','success')
            return redirect(url_for('dashbord'))
        else:
            flash('invalid credential','danger')
         
    return render_template('login.html',form=form)

@app.route('/insert',methods=['GET','POST'])
def add():
    if request.method=='POST':
        name=request.form['Name']
        age=request.form['Age']
        email=request.form['Email']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO details2 (name,age,email_id) VALUES (%s,%s,%s)",(name,age,email))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('dashbord'))
    return render_template('add.html')

@app.route('/edit/<string:id>',methods=['GET','POST'])
def edit(id):
    cur= mysql.connection.cursor()
    cur.execute('select * from details2 where id=%s',(id,))
    data=cur.fetchone()
    mysql.connection.commit()
    cur.close()
    
    if request.method=='POST':    
        name=request.form.get('Name')
        age=request.form.get('Age')
        email=request.form.get('Email')
        
        cur=mysql.connection.cursor()
        cur.execute('update details2 set name=%s, age=%s, email_id=%s where id=%s',(name,age,email,id))
        data=cur.fetchone()
        mysql.connection.commit()
        cur.close()
    
        return redirect(url_for('dashbord'))
    return render_template('edit.html',data=data)

@app.route('/delete/<string:id>')
def delete(id):
    cur=mysql.connection.cursor()
    cur.execute('delete from details2 where id=%s',(id,))
    mysql.connection.commit()
    cur.close()
    
    return redirect(url_for('dashbord'))

@app.route('/logout')
def logout():
    session.pop('user',None)
    flash('logged successful','success')
    return redirect(url_for('login'))

if __name__=='__main__':
    app.run(debug=True)