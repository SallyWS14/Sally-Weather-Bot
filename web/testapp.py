from flask import Flask, request, render_template, url_for, jsonify

tapp = Flask(__name__)
tapp.config.from_object('config')

@tapp.route('/')
def index():
    return render_template('index.html')

@tapp.route('/chat')
def chat():
    return render_template('chat.html')

# receive and send responses to the chat
@tapp.route('/chat', methods=['GET','POST'])
def chat_post():
    if request.method == 'POST':
        message = request.form['message']
        response = process_response(request)
        return response

# processs output
def process_response(text):
    return jsonify({'reseponse': text, 'context': 'text'})

@tapp.route('/about')
def about():
    return render_template('about.html')

@tapp.route('/credits')
def credits():
    return render_template('credits.html')

@tapp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#Test Links actually work
with tapp.test_request_context():
    print(url_for('index'))
    print(url_for('chat'))
    print(url_for('about'))
    print(url_for('credits'))

if __name__ == '__main__':
    # socketio.run(app, debug=True)
    tapp.run(debug=True)