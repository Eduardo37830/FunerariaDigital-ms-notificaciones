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
    email = request.form['email']
    destinatary = request.form['destinatary']
    message = request.form['message']
    subject = request.form['subject']

    cuerpo_html = cargar_y_personalizar_plantilla(destinatary, message)


    # Create an SES client
    client = boto3.client(
        "ses",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key,
        region_name="us-east-1"
    )
    # send the email message using the client
    response = client.send_email(
            Destination={'ToAddresses': [email]},
            Message={
                'Body': {
                    'Html': {  # Asegúrate de usar 'Html' en lugar de 'Text'
                        'Charset': "UTF-8",
                        'Data': cuerpo_html,
                    },
                },
                'Subject': {
                    'Charset': "UTF-8",
                    'Data': subject,
                },
            },
            Source="eduardo.villamil37830@ucaldas.edu.co"  # Tu correo verificado en SES
        )
    return response


def cargar_y_personalizar_plantilla(nombre_destinatario, mensaje):
    """Carga la plantilla HTML y reemplaza los marcadores de posición con datos reales."""
    with open('plantilla_email.html', 'r', encoding='utf-8') as archivo:
        plantilla = archivo.read()
    
    # Reemplazar los marcadores de posición con los datos reales
    plantilla_personalizada = plantilla.replace("{{nombre_destinatario}}", nombre_destinatario)
    plantilla_personalizada = plantilla_personalizada.replace("{{mensaje}}", mensaje)
    
    return plantilla_personalizada

if __name__ == '__main__':
    app.run(debug=True, port=5000)