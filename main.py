from flask import Flask, request
from dotenv import load_dotenv
import stripe
from os import getenv
import json
app = Flask(__name__)


stripe.api_key = getenv("STRIPE_SECRET_KEY")

webhook_secret = getenv("WEBHOOK_SECRET")


@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.data
    sig_header = request.headers.get('stripe-signature')
    try:
        event = stripe.Event.construct_from(
            json.loads(payload), sig_header, webhook_secret)
        print(event)
    except ValueError:
        return "Bad payload"
    except stripe.error.SignatureVerificationError:
        print("Invalid signature!")
        return "Bad signature"
    return "Success"


if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True, port=8000, host="0.0.0.0")
