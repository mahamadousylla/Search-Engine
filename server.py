from flask import Flask, send_from_directory, request

app = Flask(__name__, static_url_path='')

@app.route("/")
def search():
    return app.send_static_file("index.html")

@app.route("/result", methods=['POST']) 
def getResult():
	search = request.form['query'].strip()
	print("made it", search)
	return app.send_static_file("result.html")

if __name__ == "__main__":
    app.run(debug=True)