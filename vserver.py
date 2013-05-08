#!/usr/bin/python

from flask import Flask, request
import json
import alsaaudio
import os

app = Flask(__name__, static_folder = "static")
m = alsaaudio.Mixer()
vol = 0
htmlfile = ""

@app.route("/")
def hello():
	with open(htmlfile) as f:
		return f.read()

@app.route("/volume", methods = ["POST", "GET"])
def volume():
		if request.method == "POST":
			change_volume(request.form['change'])
		return json.dumps({"volume" : get_current_volume()})

@app.route("/mute", methods = ["POST"])
def mute():
	global vol
	if get_current_volume() == 0:
		change_volume(vol)
	else:
		vol = get_current_volume()
		m.setvolume(0)
	return json.dumps({"volume" : get_current_volume()})

def get_current_volume():
	return m.getvolume()[0]

def change_volume(by=10):
	new_volume = get_current_volume() + int(by)
	if new_volume > 100:
		new_volume = 100
	elif new_volume < 0:
		new_volume = 0
	m.setvolume(new_volume)
	



if __name__ == "__main__":
	htmlfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "volumec.html")
	vol =  get_current_volume()
	app.run(debug = False, host = "0.0.0.0")
