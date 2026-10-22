from flask import Flask, request
import requests
import os
import base64

from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


app = Flask(__name__)

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


# ==============================
# GMAIL API
# ==============================

def get_gmail_service():

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build(
        "gmail",
        "v1",
        credentials=creds
    )


# ==============================
# HTML PAGE
# ==============================

def webpage(food=None, message=""):

    result = ""

    if food:

        result = f"""
        <div class="recipe">

            <h2>{food['name']}</h2>

            <p><b>Category:</b> {food['category']}</p>

            <p><b>Area:</b> {food['area']}</p>

            <img src="{food['image']}">

            <h3>Instructions</h3>

            <p>{food['instructions']}</p>

            <hr>

            <h3>Send Recipe Through Gmail</h3>

            <form method="POST" action="/send">

                <input
                    type="email"
                    name="recipient"
                    placeholder="Enter recipient Gmail"
                    required
                >

                <input
                    type="hidden"
                    name="food_name"
                    value="{food['name']}"
                >

                <input
                    type="hidden"
                    name="instructions"
                    value="{food['instructions']}"
                >

                <button type="submit">
                    Send Recipe Using Gmail
                </button>

            </form>

        </div>
        """

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>Healthy Food Assistant</title>

        <style>

            body {{
                font-family: Arial;
                background: #eef7f0;
                margin: 0;
                padding: 40px;
            }}

            .container {{
                max-width: 650px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 0 15px #cccccc;
            }}

            h1 {{
                text-align: center;
                color: green;
            }}

            input {{
                width: 100%;
                padding: 12px;
                margin-top: 10px;
                box-sizing: border-box;
                border: 1px solid #aaa;
                border-radius: 6px;
            }}

            button {{
                width: 100%;
                padding: 12px;
                margin-top: 15px;
                background: green;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
            }}

            button:hover {{
                background: darkgreen;
            }}

            img {{
                width: 100%;
                border-radius: 10px;
                margin-top: 15px;
            }}

            .recipe {{
                margin-top: 25px;
                line-height: 1.6;
            }}

            .message {{
                color: red;
                margin-top: 20px;
            }}

        </style>

    </head>

    <body>

        <div class="container">

            <h1>🥗 Healthy Food Assistant</h1>

            <form method="POST" action="/">

                <input
                    type="text"
                    name="food"
                    placeholder="Enter food name"
                    required
                >

                <button type="submit">
                    Search Food
                </button>

            </form>

            <p class="message">{message}</p>

            {result}

        </div>

    </body>

    </html>
    """


# ==============================
# HOME
# ==============================

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "GET":
        return webpage()

    food_name = request.form.get("food")

    try:

        url = "https://www.themealdb.com/api/json/v1/1/search.php"

        response = requests.get(
            url,
            params={"s": food_name},
            timeout=15
        )

        data = response.json()

        if not data.get("meals"):
            return webpage(
                message="No recipe found. Try chicken, pasta or beef."
            )

        meal = data["meals"][0]

        food = {
            "name": meal["strMeal"],
            "category": meal["strCategory"],
            "area": meal["strArea"],
            "instructions": meal["strInstructions"],
            "image": meal["strMealThumb"]
        }

        return webpage(food=food)

    except Exception as error:

        return webpage(
            message="Food API Error: " + str(error)
        )


# ==============================
# SEND GMAIL
# ==============================

@app.route("/send", methods=["POST"])
def send_email():

    recipient = request.form.get("recipient")
    food_name = request.form.get("food_name")
    instructions = request.form.get("instructions")

    try:

        service = get_gmail_service()

        email_text = (
            "Healthy Food Recipe\n\n"
            "Food Name: " + food_name + "\n\n"
            "Instructions:\n" + instructions
        )

        message = MIMEText(email_text)

        message["to"] = recipient
        message["subject"] = (
            "Healthy Food Recipe - " + food_name
        )

        encoded_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        service.users().messages().send(
            userId="me",
            body={"raw": encoded_message}
        ).execute()

        return """
        <h1>Email Sent Successfully! ✅</h1>
        <p>The recipe was sent through Gmail.</p>
        <a href="/">Go Back</a>
        """

    except Exception as error:

        return f"""
        <h1>Gmail Error ❌</h1>
        <p>{error}</p>
        <a href="/">Go Back</a>
        """


# ==============================
# RUN
# ==============================

if __name__ == "__main__":

    app.run(
        debug=True
    )