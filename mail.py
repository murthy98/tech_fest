from flask_mail import Mail, Message

def send_mail():
	try:
		msg = Message("RESONANCE-2k19!",
		  sender="narayanamurthy.gidugu@gmail.com",
		  recipients=["grsssmurthy@gmail.com"])
		msg.body = "Thank you for registering"           
		mail.send(msg)
		return 'Mail sent!'
	except Exception as e:
		return(str(e)) 