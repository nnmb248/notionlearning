from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# JSON 데이터 불러오기 함수
def load_concepts():
    with open("concepts.json", "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/")
def index():
    data = load_concepts()
    return render_template("index.html", data=data)

@app.route("/api/concepts")
def api_concepts():
    data = load_concepts()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
