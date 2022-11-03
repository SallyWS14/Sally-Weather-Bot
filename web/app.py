from flask import Flask, render_template, url_for

app = Flask(__name__)

app.config.from_object('config')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

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
    app.run(debug=True)