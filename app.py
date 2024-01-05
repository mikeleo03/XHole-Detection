from flask import Flask, render_template, Response
from lib.framegenerator import generate_frames

app = Flask(__name__)

@app.route('/')
def home():
    apps = ['detector']  # Replace with your actual app names
    return render_template('index.html', title='XHole Detection', apps=apps)

@app.route('/detector')
def detector():
    return render_template('detector.html', title='XHole Detection Main Cam')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
