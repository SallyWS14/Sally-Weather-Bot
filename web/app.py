from flask import Flask, request, render_template, url_for, jsonify
# from ../SallyPython import location

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

# receive and send responses to the chat
@app.route('/chat', methods=['GET','POST'])
def chat_post():
    if request.method == 'POST':
        message = request.form['message']
        response = process_response(message)
        return response

def process_response(text):
    print("Processing response")
    """
    response: "The bot message",
    command: "history",
    data: [list of data]
    """
    # result = {'response': "What can I help you with?"}
    result = {'response': text}
    return jsonify(result)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/credits')
def credits():
    return render_template('credits.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

with app.test_request_context():
    print(url_for('index'))
    print(url_for('chat'))
    print(url_for('about'))
    print(url_for('credits'))

if __name__ == '__main__':
    # socketio.run(app, debug=True)
    app.run(debug=True)