import requests
import json
from threading import Thread
from flask import Flask
from mcstatus import JavaServer


app = Flask("app")

@app.route('/')
def home():
    home = "<h1>Welcome!</h1>"
    home += "<p>How did you get here? 🤔</p>"
    return home
#java status, using ̶d̶i̶n̶n̶e̶r̶b̶o̶n̶e̶'̶s̶ ̶p̶y̶t̶h̶o̶n̶  py-mine/mcstatus
@app.route('/java/<ip>/<port>', methods=['GET'])
def java(ip, port):
    try:
      jserver = JavaServer.lookup(f"{ip}:{port}")
      jstatus = jserver.status()
      rjava = {
        "players": jstatus.players.online,
        "max": jstatus.players.max,
        "version": jstatus.version.name,
        "protocol": jstatus.version.protocol,
        "motd": jstatus.description,
        "response": jstatus.latency
      }
      return json.dumps(rjava)
    except:
      return "error"
#idk why, mcstatus gives errors on bedrock, so, we have to eat the cache of 5 minutes with chips.
@app.route('/bedrock/<ip>/<port>', methods=['GET'])
def bedrock(ip, port):
    try:
      r = requests.get(f"https://api.mcstatus.io/v2/status/bedrock/{ip}:{port}")

      rjson = r.json()
      bbedrock = {
        "players": rjson["players"]["online"],
        "max": rjson["players"]["max"],
        "protocol": rjson["version"]["protocol"],
        "motd": rjson["motd"]["clean"],
        "response": r.elapsed.total_seconds() * 1000
      }
      return json.dumps(bbedrock)
    except:
      return "error"
    

def run():
    app.run(host='0.0.0.0', port=8080)

def runner():
    Thread(target=run).start()
