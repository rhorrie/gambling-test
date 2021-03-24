from flask import Flask, request
import pandas as pd
app = Flask(__name__)

@app.route('/')
def index():
    
    df = pd.DataFrame({'A': [0, 1, 2, 3, 4],
                       'B': [5, 6, 7, 8, 9],
                       'C': ['a', 'b', 'c--', 'd', 'e']})
    
    return render_template('simple.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
    #return "<h1>Welcome to our server !!</h1>"
