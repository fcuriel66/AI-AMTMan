from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from openai import OpenAI

# Keeping the API_KEY secure
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Define the client relation to the AI API
client = OpenAI(api_key=api_key)

# Start Flask
app = Flask(__name__)

# Database Env.

# basedir = os.path.abspath(os.path.dirname(__file__))
# db_path = os.path.join(basedir, 'data', 'movies.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db.init_app(app)  # Link the database and the app. This is the reason you need to import db from models
# data_manager = DataManager() # Create an instance object of your DataManager class


# Route for the request (POST). GET to just first display the index.html page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        question = request.form['question']
        response = client.responses.create(
            model="gpt-5-mini",
            input=question + ". Keep the answer short."
        )
        answer = response.output_text
        return render_template('index.html', answer=answer)
    else:
        return render_template('index.html')


# @app.route('/users', methods=['POST'])
# def create_user():
#     try:
#         name = request.form.get('user')
#         if not name:
#             return redirect(url_for('index'))
#
#         data_manager.create_user(name)
#         return redirect(url_for('index'))
#     except Exception as e:
#         print(f"Error in user create_user route call: {e}")
#         return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)