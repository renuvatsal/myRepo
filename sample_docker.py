from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    # Run the app on host 0.0.0.0 to ensure it accepts connections from outside the container
    app.run(host='0.0.0.0', port=80)
