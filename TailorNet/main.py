from flask import Flask, jsonify

app = Flask(__name__)

# @app.route("/")
# def home():
    # return render_template("index.html")
    # return "hello world"

@app.route("/tailor", methods=["GET"])
def predict():
    # features = [float(x) for x in request.form.values()]
    # final_features = [np.array(features)]
    # prediction = model.predict
    # output = "hello"
    # return render_template("index.html", prediction_text = f"flower is {output}")
    return jsonify(
        username="hi",
        email="blah",
        id="id"
    )
if __name__ == "__main__":
    app.run(debug=True)
