from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "Dating Matcher Agent is running",
        "agent": "lovefi-matcher",
        "message": "Flask API endpoint working"
    })

@app.route('/api')
@app.route('/api/')
def api():
    return jsonify({
        "status": "API endpoint working",
        "agent": "lovefi-matcher",
        "endpoints": ["/", "/api", "/submit"]
    })

@app.route('/submit', methods=['GET', 'POST'])
@app.route('/api/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        try:
            data = request.get_json()
            return jsonify({
                "status": "POST received",
                "message": "Submit endpoint working",
                "received_data": bool(data),
                "method": "POST"
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 400
    else:
        return jsonify({
            "status": "GET received",
            "message": "Submit endpoint working",
            "method": "GET"
        })

if __name__ == '__main__':
    app.run(debug=True)
