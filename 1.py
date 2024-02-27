from flask import Flask, render_template, request, jsonify
import openai
# import logging
import os  # Import os to use environment variables

app = Flask(__name__)

# Configure logging
# logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    # Renders the mermaid.html file when accessing the root URL
    return render_template('index.html')

@app.route('/generate_mermaid', methods=['POST'])
def generate_mermaid():
    required_params = ['title', 'audience', 'category', 'length', 'content']
    data = request.json
    if not data or not all(param in data for param in required_params):
        missing_params = [param for param in required_params if param not in data]
        print("ERROR BROKEN")
        return jsonify({'error': f"Missing required parameters: {', '.join(missing_params)}"}), 400

    title = data['title']
    audience = data['audience']
    category = data['category']
    length = data['length']
    content = data['content']

    print("Processing your request")
    # It's recommended to use environment variables for API keys
    # api_key = os.getenv('OPENAI_API_KEY')
    # if not api_key:
    #     logging.error("OpenAI API key is not set in environment variables.")
    #     return jsonify({'error': 'OpenAI API key is not configured on the server.'}), 500

    try:
        prompt = f"Generate Mermaid syntax for a flowchart based on the following description: {description}. Only return mermaid code starting from graph TD. DO not include mermaid in response. For example, if the description is 'A flowchart to show the process of a user signing up for a website', the response should be"
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            # api_key=api_key
        )
        mermaid_syntax = response.choices[0].message.content.strip()
        # mermaid_syntax = response.choices[0].message['content']
        print("mermaid_syntax: ", mermaid_syntax)
        # print("mermaid_syntax: ", mermaid_syntax)
        return jsonify({'mermaidSyntax': mermaid_syntax})
    except Exception as e:
        # logging.error(f"Error: {e}")
        return jsonify({'error': 'Failed to generate Mermaid syntax', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
