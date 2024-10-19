import africastalking
from flask import Flask, request, jsonify
from transformers import pipeline


app = Flask(__name__)


username = "sandbox"  
api_key = "atsk_b538ea5fdf34b66f2d71cdfb2772fdd6a680511fba2a3a5684cbf3dbda3aea72631a0b70" 


africastalking.initialize(username, api_key)
sms = africastalking.SMS


qa_model = pipeline("health_(1).ipynb", model="https://colab.research.google.com/drive/11Swu7y3Nr-yIXQkXGtbGGacng4kL1vbl#scrollTo=WCeseMgPaxRT")


def send_sms(message, recipient):
    try:
        response = sms.send(message, [recipient])
        print(f"SMS sent successfully: {response}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")

def get_model_response(question, context):
    try:
    
        response = qa_model(question=question, context=context)
        return response["answer"]
    except Exception as e:
        print(f"Error generating response from model: {e}")
        return "Sorry, I couldn't process your request at the moment."


context = """
Pregnancy is the state of carrying a developing embryo or fetus within the female body. 
Common early signs of pregnancy include missed periods, nausea, vomiting, fatigue, and breast tenderness.
Consult a healthcare provider for confirmation and advice.
"""


@app.route('/sms', methods=['POST'])
def sms_callback():
    phone_number = request.values.get('from')  # Sender's phone number
    message_text = request.values.get('text').lower()  # User's message

    
    model_response = get_model_response(question=message_text, context=context)

   
    send_sms(model_response, phone_number)

   
    return jsonify({"status": "success"}), 200


if __name__ == "__main__":
    app.run(debug=True)
