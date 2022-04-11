from flask import Flask, render_template
import datetime

app = Flask('my_first_server')

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/test')
def this_is_test_handler_func():
	return '<H1 style="color:rgb(100,100,200)">test</H1>'

@app.route('/time')
def time_handler():
    cur_datetime_str = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return render_template("index.html", cur_datetime=cur_datetime_str)
 
app.run(port=9000)