from flask import Flask, render_template, jsonify, Response, Markup
from flask_restful import reqparse, abort, Api, Resource
from requests.auth import HTTPBasicAuth
import requests
import json 

# Init flask
app = Flask(__name__,
static_url_path="",
static_folder="public",
template_folder="views",
root_path="")

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/kanbanboard")
def kanbanboard():
    return render_template("kanbanboard.html")
    
@app.route("/project-create")
def project_create():
    return render_template("project-create.html")
    
@app.route("/project-detail")
def project_detail():
    return render_template("project-detail.html")
    
@app.route("/project-edit")
def project_edit():
    return render_template("project-edit.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/translation")
def feminenza():
    r = requests.get("https://www.feminenza.org/wp-json/wp/v2/pages", auth=HTTPBasicAuth("gedens", "1Feminenza#1234th"))
    return Response(r.content.decode("utf-8"), mimetype="text/json")

@app.route("/feminenza-welcome")
def feminenza_welcome():
    r = requests.get("https://www.feminenza.org/wp-json/wp/v2/pages?slug=welcome&lang=en", auth=HTTPBasicAuth("gedens", "1Feminenza#1234th"))
    v = json.loads(r.text)
    v[0]["content"]["rendered"] = Markup(v[0]["content"]["rendered"])
    return render_template("feminenza.html", data=v)

@app.route("/feminenza-welcome-nl")
def feminenza_welcome_nl():
    r = requests.get("https://www.feminenza.org/wp-json/wp/v2/pages?slug=welkom&lang=nl", auth=HTTPBasicAuth("gedens", "1Feminenza#1234th"))
    v = json.loads(r.text)
    v[0]["content"]["rendered"] = Markup(v[0]["content"]["rendered"])
    return render_template("feminenza.html", data=v)

@app.route("/feminenza-welcome-fr")
def feminenza_welcome_fr():
    r = requests.get("https://www.feminenza.org/wp-json/wp/v2/pages?slug=bienvenue&lang=fr", auth=HTTPBasicAuth("gedens", "1Feminenza#1234th"))
    v = json.loads(r.text)
    v[0]["content"]["rendered"] = Markup(v[0]["content"]["rendered"])
    return render_template("feminenza.html", data=v)