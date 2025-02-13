import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import dotenv
import markdown2
import flask_cors
from flask_cors import CORS

# Load environment variables
dotenv.load_dotenv()

XAI_API_KEY = os.getenv("XAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

# Flask app
app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET", "POST"])
def index():
    response_message = ""
    user_message = ""

    if request.method == "POST":
        user_message = request.form.get("message")
        if user_message:
            # Call the OpenAI API
            completion = client.chat.completions.create(
                model="grok-beta",
                messages=[
                    {"role": "system", "content": "You are Grok, One of the best AI assistants in the world."},
                    {"role": "user", "content": user_message},
                ],
            )
            response_message = completion.choices[0].message.content


    return render_template(
        "index.html",
        user_message=user_message,
        response_message=markdown2.markdown(response_message, extras=["fenced-code-blocks", "tables"]),
    )


if __name__ == "__main__":
    app.run(debug=True)
