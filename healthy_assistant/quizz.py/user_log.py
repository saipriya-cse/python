from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Login Page</title>

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

        .login-container {
            width: 380px;
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25);
        }

        .login-container h1 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
        }

        .login-container p {
            text-align: center;
            color: #777;
            margin-bottom: 30px;
        }

        .input-group {
            margin-bottom: 20px;
        }

        .input-group label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: bold;
        }

        .input-group input {
            width: 100%;
            padding: 13px;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 15px;
            outline: none;
        }

        .input-group input:focus {
            border-color: #667eea;
            box-shadow: 0 0 5px rgba(102, 126, 234, 0.3);
        }

        .login-btn {
            width: 100%;
            padding: 13px;
            border: none;
            border-radius: 8px;
            background: #667eea;
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }

        .login-btn:hover {
            background: #5568d9;
        }

        .message {
            text-align: center;
            margin-top: 20px;
            padding: 10px;
            border-radius: 8px;
            font-weight: bold;
        }

        .success {
            color: green;
            background: #e8f8e8;
        }

        .error {
            color: red;
            background: #ffe8e8;
        }
    </style>
</head>

<body>

    <div class="login-container">

        <h1>Welcome Back</h1>
        <p>Login to your account</p>

        <form method="POST">

            <div class="input-group">
                <label>Username</label>
                <input type="text"
                       name="username"
                       placeholder="Enter your username"
                       required>
            </div>

            <div class="input-group">
                <label>Password</label>
                <input type="password"
                       name="password"
                       placeholder="Enter your password"
                       required>
            </div>

            <button type="submit" class="login-btn">
                LOGIN
            </button>

        </form>

        {% if message %}
            <div class="message {{ message_type }}">
                {{ message }}
            </div>
        {% endif %}

    </div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def login():

    message = ""
    message_type = ""

    if request.method == "POST":

        user_name = request.form["username"]
        user_password = request.form["password"]

        inbuilt_user_name = "admin"
        inbuilt_user_password = "admin123"

        if user_name == inbuilt_user_name and user_password == inbuilt_user_password:
            message = "Login Successful!"
            message_type = "success"
        else:
            message = "Invalid Username or Password."
            message_type = "error"

    return render_template_string(
        HTML,
        message=message,
        message_type=message_type
    )


if __name__ == "__main__":
    app.run(debug=True)