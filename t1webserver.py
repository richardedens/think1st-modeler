from flask import Flask, render_template, jsonify, Response, Markup
from flask_restful import reqparse, abort, Api, Resource
from requests.auth import HTTPBasicAuth
import requests
import json 

# Init flask
t1webserver = Flask(__name__,
static_url_path="",
static_folder="public",
template_folder="views",
root_path="")

@t1webserver.route("/")
def homepage():
    return render_template("homepage.html")

@t1webserver.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@t1webserver.route("/kanbanboard")
def kanbanboard():
    return render_template("kanbanboard.html")
    
@t1webserver.route("/project-create")
def project_create():
    return render_template("project-create.html")
    
@t1webserver.route("/project-detail")
def project_detail():
    return render_template("project-detail.html")
    
@t1webserver.route("/project-edit")
def project_edit():
    return render_template("project-edit.html")

@t1webserver.route("/signin")
def signin():
    return render_template("signin.html")

@t1webserver.route("/signup")
def signup():
    return render_template("signup.html")

@t1webserver.route("/translation")
def feminenza():
    r = requests.get("https://www.feminenza.org/wp-json/wp/v2/pages", auth=HTTPBasicAuth("gedens", "1Feminenza#1234th"))
    return Response(r.content.decode("utf-8"), mimetype="text/json")

@t1webserver.route("/feminenza-welcome")
def feminenza_welcome():
    r = requests.get("https://www.feminenza.org/wp-json/wp/v2/pages?slug=welcome&lang=en", auth=HTTPBasicAuth("gedens", "1Feminenza#1234th"))
    v = json.loads(r.text)
    v[0]["content"]["rendered"] = Markup(v[0]["content"]["rendered"])
    return render_template("feminenza.html", data=v)

@t1webserver.route("/feminenza-welcome-nl")
def feminenza_welcome_nl():
    r = requests.get("https://www.feminenza.org/wp-json/wp/v2/pages?slug=welkom&lang=nl", auth=HTTPBasicAuth("gedens", "1Feminenza#1234th"))
    v = json.loads(r.text)
    v[0]["content"]["rendered"] = Markup(v[0]["content"]["rendered"])
    return render_template("feminenza.html", data=v)

@t1webserver.route("/feminenza-welcome-fr")
def feminenza_welcome_fr():
    r = requests.get("https://www.feminenza.org/wp-json/wp/v2/pages?slug=bienvenue&lang=fr", auth=HTTPBasicAuth("gedens", "1Feminenza#1234th"))
    v = json.loads(r.text)
    v[0]["content"]["rendered"] = Markup(v[0]["content"]["rendered"])
    return render_template("feminenza.html", data=v)