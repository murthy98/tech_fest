from flask import Flask, render_template, flash, request, url_for, redirect,session
import gc
from flask_mail import Mail, Message
from passlib.hash import sha256_crypt
from wtforms import Form,  StringField, SelectField, validators
import socket
import smtplib
import re
import dns.resolver
from dbconnection import connection
from flask_socketio import SocketIO, emit

app = Flask(__name__)

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.googlemail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'narayanamurthy.gidugu@gmail.com',
	MAIL_PASSWORD = 'zphooxccrztyvtbk'
	)
app.config['SECRET_KEY'] = 'redsfsfsfsfis'
mail = Mail(app)
socketio = SocketIO(app)
@socketio.on('disconnect')
def disconnect_user():
    session.clear()
def mailverify(email):
   
    try:
        addressToVerify =email
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)

        if match == None:
            return 'syntax not valid'
        m=email.split('@')[1]
        m=str(m)
        records = dns.resolver.query(m, 'MX')
        mxRecord = records[0].exchange
        mxRecord = str(mxRecord)
        host = socket.gethostname()
        server = smtplib.SMTP()
        server.set_debuglevel(0)
        server.connect(mxRecord)
        server.helo(host)
        server.mail(email)
        code, message = server.rcpt(str(addressToVerify))
        server.quit()
        if code == 250:
            return 1
        else:
            return 0
    except Exception :
        
        return 0
def send_mail(email):
	try:
        
		msg = Message("RESONANCE-2k19!",sender="narayanamurthy.gidugu@gmail.com",recipients=[str(email)])
		msg.body = "Thanks for registering.\n\t\tYour application has been shared with our related co-ordinators.Please forward your abstract to below mails depending on your stream. \nCSE:   resonance2k19.cse@bvcgroup.in\nECE:   resonance2k19.ece@bvcgroup.in \nEEE:    resonance2k19.eee@bvcgroup.in\nCE:   resonance2k19.civil@bvcgroup.in\nME:   resonance2k19.mech@bvcgroup.in\n\n\n\t\tRegards\n\tBVC ENGG COLLEGE"
                                       
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
def register():
    return render_template("register.html")

@app.route('/kreeda/')
def kreeda():
    return render_template("kreeda.html")
@app.route('/contact/')
def contact():
    return render_template("contact.html")


@app.route('/registration/', methods=["GET","POST"])
def registration():
    try:
        if request.method == "POST" :
            if 'submit_button' in request.form:
                name  = request.form['name']
                clgname = request.form['clgname']
                event = request.form['events']
                email=request.form['email']
                branch = request.form['branch']
                x=mailverify(email)
                
                
                if x == 1:
                    c, conn = connection()
                    c.execute("INSERT INTO festusers(name,clg_name,event,branch,email) VALUES (%s, %s, %s, %s,%s)",(name,clgname,event,branch,email))
                    conn.commit()                    
                    
                    
                    
                    z=send_mail(str(email))
                    
                    c.close()
                    conn.close()
                    gc.collect()
                    flash("Successfully Registered !!")
                    return render_template("resonance.html")
                else:
                    flash("Invalid email!!")
                    return render_template('register.html')
            return render_template("register.html")

    except Exception as e:
        flash(e)
        return render_template("home.html", error = e) 
		
@app.route("/admin/")
def admin():
    return render_template("admin.html")
@app.route("/logout/")
def logout():
    session.clear()
    return render_template("admin.html")
@app.route('/login/', methods=["GET","POST"])
def login():
    c,conn = connection()
   
    try:
        
        if request.method == "POST" :

            if 'adminsubmit' in request.form:
                c.execute("SELECT * FROM admin WHERE email = ('%s')" %request.form["adminmail"])
               
                data = c.fetchone()
              
                if sha256_crypt.verify(request.form['password'],data[1] ):
                    
                    session['logged_in'] = True
                    session['username'] = request.form['adminmail']
                    c.execute("SELECT * FROM festusers WHERE branch = ('%s')" %data[2])
                    tab_data = c.fetchall()
                    c.close()
                    conn.commit()
                    conn.close()
                    gc.collect()
                    return render_template("home.html",data = tab_data)
        return render_template("admin.html")
    except Exception as e:

        return render_template("admin.html", error = e)


if __name__ == "__main__":
    app.secret_key="bvcfest2k19"
    
    app.run(debug=True)
