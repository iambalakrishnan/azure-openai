import os
from openai import AzureOpenAI
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from utils.exception import OpenAIAPIError
from utils.logger import setup_logger

app = Flask(__name__)

load_dotenv()

AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
MODEL_DEPLOYMENT_NAME = os.environ.get("MODEL_DEPLOYMENT_NAME")


logger = setup_logger(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            user_input = request.form["user_input"]
            client = AzureOpenAI(
                azure_endpoint=AZURE_OPENAI_ENDPOINT,
                api_key=AZURE_OPENAI_API_KEY,
                api_version="2024-02-01"  # Update to the latest version if needed
            )

            response = client.chat.completions.create(
                model=MODEL_DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": user_input}
                ],
            )
            ai_response = response.choices[0].message.content
            return jsonify({"response": ai_response})

        except OpenAIAPIError as e:
            logger.error(f"OpenAI API Error: {e.message} (Status Code: {e.status_code})")
            return jsonify({"error": "Error communicating with OpenAI"}), 500

        except Exception as e:
            logger.error(f"Unexpected Error: {e}")
            return jsonify({"error": "Internal server error"}), 500
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
