from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def quiz():

    result1 = ""
    result2 = ""

    if request.method == "POST":

        q1 = request.form.get("q1", "").lower()
        q2 = request.form.get("q2", "").lower()

        if q1 == "delhi":
            result1 = "✅ Correct Answer"
        else:
            result1 = "❌ Wrong Answer"

        if q2 == "hyderabad":
            result2 = "✅ Correct Answer"
        else:
            result2 = "❌ Wrong Answer"

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>India & Telangana Quiz</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            min-height: 100vh;

            display: flex;
            justify-content: center;
            align-items: center;
        }

        .quiz-box {
            width: 500px;
            background: white;
            padding: 35px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }

        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }

        .question {
            margin-bottom: 25px;
        }

        .question label {
            display: block;
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }

        input[type="text"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            outline: none;
        }

        input[type="text"]:focus {
            border-color: #667eea;
        }

        button {
            width: 100%;
            padding: 13px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            cursor: pointer;
        }

        button:hover {
            background: #5568d8;
        }

        .result {
            margin-top: 10px;
            padding: 10px;
            border-radius: 8px;
            font-weight: bold;
            text-align: center;
        }

        .correct {
            background: #d4edda;
            color: #155724;
        }

        .wrong {
            background: #f8d7da;
            color: #721c24;
        }
    </style>
</head>

<body>

    <div class="quiz-box">

        <h1>📝 General Knowledge Quiz</h1>

        <form method="POST">

            <div class="question">
                <label>1. What is the capital of India?</label>

                <input type="text"
                       name="q1"
                       placeholder="Enter your answer">

                {% if result1 %}
                    <div class="result {% if 'Correct' in result1 %}correct{% else %}wrong{% endif %}">
                        {{ result1 }}
                    </div>
                {% endif %}
            </div>


            <div class="question">
                <label>2. What is the capital of Telangana?</label>

                <input type="text"
                       name="q2"
                       placeholder="Enter your answer">

                {% if result2 %}
                    <div class="result {% if 'Correct' in result2 %}correct{% else %}wrong{% endif %}">
                        {{ result2 }}
                    </div>
                {% endif %}
            </div>


            <button type="submit">Check Answers</button>

        </form>

    </div>

</body>
</html>
""", result1=result1, result2=result2)


if __name__ == "__main__":
    app.run(debug=True)