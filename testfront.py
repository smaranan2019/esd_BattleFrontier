from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    #no need to re-run the server everytime you make a change 
    app.run(debug=True)