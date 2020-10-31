from flask import Flask
from threading import Thread

#To create a Psuedo Website to send Bot get requests to keep it running
app = Flask('')

@app.route('/')
def home():
    return "Bot is online"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()
