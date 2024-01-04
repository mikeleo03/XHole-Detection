from flask import Flask, render_template, Response
from lib.framegenerator import generate_frames

app = Flask(__name__)

@app.route('/detector')
def detector():
    return render_template('detector.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
