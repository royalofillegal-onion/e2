import traceback
from flask import Flask, jsonify, request
from scraper.scraper import scrape_attendance

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/attendance', methods=['POST'])
def attendance():
    data = request.get_json(force=True)
    roll_no = data.get('rollNo')
    password = data.get('password')

    if not roll_no or not password:
        return jsonify({'error': 'Missing roll number or password'}), 400

    try:
        attendance_data = scrape_attendance(roll_no, password)
        return jsonify(attendance_data)
    except Exception as error:
        tb = traceback.format_exc()
        print(tb)
        return jsonify({'error': str(error), 'traceback': tb}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
