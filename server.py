from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='')

@app.route("/")
def search():
    return render_template("index.html")

@app.route("/result", methods=['POST']) 
def getResult():
	search = request.form['query'].strip()
	print("made it", search)
	return render_template("result.html")

if __name__ == "__main__":
    app.run(debug=True)