from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='')
pq = []


@app.route("/")
def search():
    return render_template("index.html")

@app.route("/result", methods=['POST']) 
def getResult():
	#pq should be top 10 results
	search = request.form['query'].strip()
	print("made it", search)
	return render_template("result.html", data = pq)

if __name__ == "__main__":
    app.run(debug=True)