from flask import Flask, request, jsonify, send_file
from api import generate_content, fetch_content, clean_data
app = Flask(__name__)

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')
    url = data.get('url', '')
    
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    
    try:
        context = ''
        if url:
            raw_content = fetch_content(url)
            if not raw_content.startswith('Error:'):
                context = clean_data(raw_content)
        
        response = generate_content(prompt, context)
        return jsonify({'response': response})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)