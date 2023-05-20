import random
import logging
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    try:
        logger.info("Rendering index.html template.")
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error occurred while rendering index.html template: {e}")
        return "An error occurred while rendering the template.", 500

@app.route('/user-text-input', methods=['POST'])
def handle_user_input():
    user_input = request.form.get('user_input')
    response_text = f"You entered {user_input}"
    logger.info(response_text)
    return jsonify({"message": response_text})

@app.route('/your-choice-endpoint', methods=['POST'])
def handle_choice():
    # TODO: Implement handling of choice buttons
    return jsonify({})

@app.route('/your-dice-endpoint/<dice>')
def roll_dice(dice):
    if dice == "d6":
        result = random.randint(1, 6)
    elif dice == "d12":
        result = random.randint(1, 12)
    elif dice == "d20":
        result = random.randint(1, 20)
    else:
        return jsonify({"error": "Invalid dice type"})

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
