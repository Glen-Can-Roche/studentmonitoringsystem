from flask import Flask, render_template, request, send_file
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
REPORT_FOLDER = 'reports'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_video():
    video = request.files['video']
    mode = request.form['mode']
    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    video.save(filepath)

    from face_recognition_attendance import mark_attendance
    student_ids = mark_attendance(filepath)

    if mode == 'normal':
        from analyze_normal import generate_normal_report
        output_path = generate_normal_report(filepath, student_ids)
    else:
        from analyze_exam import generate_exam_report
        output_path = generate_exam_report(filepath, student_ids)

    return render_template("index.html", report_link='/' + output_path)

@app.route('/reports/<filename>')
def download_file(filename):
    return send_file(os.path.join(REPORT_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
