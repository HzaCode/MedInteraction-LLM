
import os
from flask import Flask, request, jsonify, render_template
import dashscope


dashscope.api_key = os.getenv('DASHSCOPE_API_KEY', '')
if not dashscope.api_key:
    raise ValueError("API key not set in environment variables or defaulted")

app = Flask(__name__)

def call_with_prompt(prompt):
    
    response = dashscope.Generation.call(
        model=dashscope.Generation.Models.qwen_turbo,
        prompt=prompt
    )

  
    if response.status_code == 200:
        return response.output
    else:
        return f"Error Code: {response.code}, Error Message: {response.message}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    response = call_with_prompt(question)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
