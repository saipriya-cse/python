from flask import Flask, request, render_template_string

app = Flask(__name__)

correct_password = "admin123"
attempts = 0
account_locked = False

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Password Login</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }

        body {
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #667eea, #764ba2);
        }

        .login-box {
            width: 380px;
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            text-align: center;
        }

        .login-box h1 {
            color: #333;
            margin-bottom: 10px;
        }

        .login-box p {
            color: #777;
            margin-bottom: 30px;
        }

        .password-input {
            width: 100%;
            padding: 14px;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 16px;
            outline: none;
            margin-bottom: 20px;
        }

        .password-input:focus {
            border-color: #667eea;
        }

        .login-button {
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 8px;
            background: #667eea;
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }

        .login-button:hover {
            background: #5568d9;
        }

        .success {
            margin-top: 20px;
            padding: 12px;
            border-radius: 8px;
            background: #d4edda;
            color: #155724;
        }

        .error {
            margin-top: 20px;
            padding: 12px;
            border-radius: 8px;
            background: #f8d7da;
            color: #721c24;
        }

        .locked {
            margin-top: 20px;
            padding: 12px;
            border-radius: 8px;
            background: #343a40;
            color: white;
        }

        .attempts {
            margin-top: 20px;
            color: #777;
            font-size: 14px;
        }
    </style>
</head>

<body>

    <div class="login-box">

        <h1>🔐 Login</h1>
        <p>Enter your password to continue</p>

        {% if not locked and not success %}
        <form method="POST">

            <input
                type="password"
                name="password"
                class="password-input"
                placeholder="Enter your password"
                required
            >

            <button type="submit" class="login-button">
                Login
            </button>

        </form>
        {% endif %}


        {% if success %}
            <div class="success">
                ✅ Login successful!
            </div>
        {% endif %}


        {% if wrong %}
            <div class="error">
                ❌ Wrong password
            </div>
        {% endif %}


        {% if locked %}
            <div class="locked">
                🔒 Account locked
            </div>
        {% endif %}


        {% if not locked and not success %}
            <div class="attempts">
                Attempt {{ attempt }} of 3
            </div>
        {% endif %}

    </div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def login():

    global attempts
    global account_locked

    success = False
    wrong = False

    if request.method == "POST":

        if account_locked:
            return render_template_string(
                html,
                locked=True,
                success=False,
                wrong=False,
                attempt=3
            )

        password = request.form["password"]

        attempts += 1

        if password == correct_password:
            success = True

        else:
            wrong = True

            if attempts == 3:
                account_locked = True
                wrong = False

    return render_template_string(
        html,
        locked=account_locked,
        success=success,
        wrong=wrong,
        attempt=attempts
    )


if __name__ == "__main__":
    app.run(debug=True)