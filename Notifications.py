from flask import Flask, request
import os
import boto3
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env (pip install python-dotenv)
load_dotenv()

# Ahora podemos acceder a las variables de entorno usando os.getenv
access_key = os.getenv('ACCESS_kEY')
secret_access_key = os.getenv('SECRET_ACCESS_KEY')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Hola, soy Flask"


@app.route("/sms", methods=['POST'])
def sms():
    destination = request.form['destination']
    message = request.form['message']
    print(destination)
    print(message)
    # Create an SNS client
    client = boto3.client(
        "sns",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key,
        region_name="us-east-1"
    )

    # Send your sms message.
    client.publish(
        PhoneNumber=destination,
        Message=message
    )
    return "OK"

# based on the code above, build the email api method using AWS SES
@app.route("/email", methods=['POST'])
def email():
    destination = request.form['destination']
    message = request.form['message']
    subject = request.form['subject']
    # Create an SES client
    client = boto3.client(
        "ses",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key,
        region_name="us-east-1"
    )
    # send the email message using the client
    response = client.send_email(
        Destination={
            'ToAddresses': [
                destination,
            ],
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': "UTF-8",
                    'Data': message,
                },
            },
            'Subject': {
                'Charset': "UTF-8",
                'Data': subject,
            },
        },
        Source="eduardo.villamil37830@ucaldas.edu.co"
    )
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)