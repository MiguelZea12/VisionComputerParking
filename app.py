from flask import Flask, render_template
from flask_cors import CORS
from controllers.status_controller import status_controller
from controllers.video_controller import video_controller

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(status_controller)
app.register_blueprint(video_controller)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
