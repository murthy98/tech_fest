from flask import Flask, render_template, flash, request, url_for, redirect
import gc
from dbconnection import connection
from flask_mail import Mail, Message
from passlib.hash import sha256_crypt


app = Flask(__name__)

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'narayanamurthy.gidugu@gmail.com',
	MAIL_PASSWORD = 'Sairf529*'
	)
app.config['SECRET_KEY'] = 'redsfsfsfsfis'
mail = Mail(app)
def send_mail():
	try:
		msg = Message("RESONANCE-2k19!",
		  sender="narayanamurthy.gidugu@gmail.com",
		  recipients=["udaysarmarani@gmail.com"])
		msg.body = "Thank you for registering"           
		mail.send(msg)
		return 'Mail sent!'
	except Exception as e:
		return(str(e)) 
@app.route('/')
def homepage():
    return render_template("home.html")
@app.route('/resonance/')
def Resonance():
    return render_template("resonance.html")
@app.route('/register/')
def Register():
    return render_template("register.html")

l=[]		
@app.route('/registration/', methods=["GET","POST"])
def registration():

    error = ''
    try:
        
        if request.method == "POST" :
            if 'submit_button' in request.form:
                name  = request.form['name']
                clgname = request.form['clgname']
                event = request.form['events']
                email=request.form['email']
                branch = request.form['branch']
                
                c, conn = connection()
                c.execute("INSERT INTO festusers(name,clg_name,event,branch,email) VALUES (%s, %s, %s, %s,%s)",(name,clgname,event,branch,email))
                conn.commit()                    
                #flash(attempted_username)
                
                flash("Successfully Registered!!")
                c.close()
                conn.close()
                gc.collect()		
                return render_template("resonance.html",l=l)
        return render_template("resonance.html", error = error)

    except Exception as e:
        flash(e)
        return render_template("home.html", error = error)  
		
@app.route("/admin/")
def admin():
    return render_template("admin.html")
@app.route('/login/', methods=["GET","POST"])
def login():
    c,conn = connection()
    error = ''
    try:
        
        if request.method == "POST" :

            if 'adminsubmit' in request.form:
               
                data = c.execute("SELECT * FROM admin WHERE email = ('%s')" %request.form["adminmail"])
               
                data = c.fetchone()
              
                if sha256_crypt.verify(request.form['password'],data[1] ):
                   
                    tab_data=c.execute("SELECT * FROM festusers")
                    tab_data = c.fetchall()
                    flash("Login Successfully !!")
                    c.close()
                    conn.close()
                    gc.collect()
                    return render_template("participats.html",data = tab_data)
        return render_template("admin.html")
    except Exception as e:

        return render_template("admin.html", error = error)  
		
if __name__ == "__main__":
    app.secret_key="bvcfest2k19"
    app.run()
