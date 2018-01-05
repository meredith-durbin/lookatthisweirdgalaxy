import glob
import os
import pandas as pd
from flask import Flask
from flask import render_template, request, send_file
import tempfile

app = Flask(__name__)

df = pd.read_csv('static/data.csv', dtype=str)
n_images = df.shape[0]

handle, outfile = tempfile.mkstemp()

with open(outfile, mode='w') as f:
    f.write('ID,Score,Notes\n')

# mast_url = 'https://archive.stsci.edu/hst/search.php?ra={}&dec={}\
# &resolver=Resolve&radius=1&sci_aec=S&action=Search\
# &outputformat=CSV&max_records=9999999'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', table = df.to_html(index=False))

@app.route('/classify/<int:page>', methods=['GET','POST'])
def classify(page):
    row = df.iloc[page-1]
    galaxy = row.to_dict()
    if request.method == "POST":
        with open(outfile, mode='a+') as f:
            f.write('{},{},{}\n'.format(request.form['id'], request.form['classify'],
                request.form['notes'].replace(',','\\,')))
    return render_template('page.html', galaxy=galaxy, n_images=n_images, page=page)

@app.route('/results', methods=['GET'])
def show_table():
    return render_template('index.html', table = pd.read_csv(outfile, escapechar='\\').to_html(index=False))

@app.route('/results.csv', methods=['GET'])
def send_csv():
    return send_file(outfile)

if __name__ == '__main__':
    app.debug = False # set this to false before putting on production!!!
    app.run()
