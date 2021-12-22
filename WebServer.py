from flask import Flask, render_template, send_from_directory   
from threading import Thread
app = Flask('',static_url_path='/static')

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/css/landing.css')
def css():
    return send_from_directory('css', "templates/css/landing.css")

@app.route('/js/landing.js')
def js():
    return send_from_directory('js', "templates/js/landing.js")





def run():
    app.run(host="0.0.0.0", port=8080)


def start():
    server = Thread(target=run)
    server.start()