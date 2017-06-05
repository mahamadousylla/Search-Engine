from flask import Flask, render_template, request
import views.ranking as Ranking

app = Flask(__name__, static_url_path='')


@app.route("/")
def search():
    return render_template("index.html")

@app.route("/result", methods=['POST']) 
def getResult():

	#pq should be top 10 results
	search = request.form['query'].strip()
	if search == "": return render_template("index.html")
	Ranking.getStopWords()
	Ranking.getAllFiles()
	pq = Ranking.Calculate(search)
	print("pq: ", pq)
	if pq[0] == False: return render_template("error.html", query = search)
	return render_template("result.html", data = pq, query = search)

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0')