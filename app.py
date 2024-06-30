from flask import Flask, jsonify, request
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
from loguru import logger

load_dotenv()

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'testing@gmail.com'

mail = Mail(app)

@app.route("/")
def hello_from_root():
    return jsonify(message='Hello from root!')

@app.route('/mail',methods = ['Post'])
def send_email():
    """Sending mail based on the parameters.
    """
    data = request.get_json()
    recipient = data.get('recipient')
    subject = data.get('subject')
    body = data.get('body')

    if not all([recipient, subject, body]):
        logger.error("Missing required fields")
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        msg = Message(subject, recipients=[recipient], body=body, sender="testing@test.com")
        mail.send(msg)
        return jsonify({'message': 'Email sent successfully!'}), 200

    except Exception as err:
        logger.exception(err)
        return jsonify({'message': 'Error in sending mail'}), 500
    

if __name__ == '__main__':
    app.run(debug=True)
  