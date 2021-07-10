from flask import Flask, render_template, request, make_response, redirect, session, url_for, Response, stream_with_context
import os
import sys
import platform
from iqoptionbot.starter import start
from iqoptionbot.execute import execute_gen


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

app.secret_key = os.urandom(12).hex()

@app.route('/', methods = ['GET', 'POST'])
def home():
   if request.method == 'POST':
      name = request.form['name']
      email = request.form['email']
      with open('logs/visitors.log','a') as file:
         file.write('[name, email]')

      return redirect(url_for('trader', name = name))

   return render_template('index.html') # ('index.html')

@app.route('/traderstream')
def stream():
   if platform.system() == 'Windows':
      gen = execute_gen(['pythonpath.bat', '.', 'iqoptionbot/starter.py'])
   else: gen = execute_gen(['PYTHONPATH=.', 'python', 'iqoptionbot/starter.py', 'somecommand'])
   return Response(stream_with_context(gen))

@app.route('/trader/')
def trader():
   name = request.args['name']
   return render_template('binary.html', name = name)

if __name__ == '__main__':
   app.run(debug = True)