import glob
import os
import pandas as pd
from flask import Flask
from flask import render_template, request, send_file
import tempfile

app = Flask(__name__)

df_all = pd.read_csv('static/alldata.csv', dtype=str)
df_all['Diam'] = df_all['Diam'].astype(float)

df_cut = pd.read_csv('static/more_cut.csv', dtype=str)
df_cut['Diam'] = df_cut['Diam'].astype(float)

handle, outfile = tempfile.mkstemp()
with open(outfile, mode='w') as f:
    f.write('ID,Score,Notes\n')

handle1, outfile1 = tempfile.mkstemp()
with open(outfile1, mode='w') as f:
    f.write('ID,Score,Notes\n')

handle2, outfile2 = tempfile.mkstemp()
with open(outfile2, mode='w') as f:
    f.write('ID,Score,Notes\n')

handle3, outfile3 = tempfile.mkstemp()
with open(outfile3, mode='w') as f:
    f.write('ID,Score,Notes\n')

handle4, outfile4 = tempfile.mkstemp()
with open(outfile4, mode='w') as f:
    f.write('ID,Score,Notes\n')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', table = df_all.to_html(index=False))

@app.route('/classify/<int:page>', methods=['GET','POST'])
def classify(page):
    df = df_all.query('(Diam < 5) & (Diam > 2)').reset_index()
    n_images = df.shape[0]
    row = df.iloc[page-1]
    galaxy = row.to_dict()
    if request.method == "POST":
        with open(outfile, mode='a+') as f:
            f.write('{},{},{}\n'.format(request.form['id'], request.form['classify'],
                request.form['notes'].replace(',','\\,')))
    return render_template('page.html', galaxy=galaxy, n_images=n_images, page=page, n=0)

@app.route('/classify_1/<int:page>', methods=['GET','POST'])
def classify_1(page):
    df = df_all.query('(Diam <= 2) & (Diam > 1)').reset_index()
    n_images = df.shape[0]
    row = df.iloc[page-1]
    galaxy = row.to_dict()
    if request.method == "POST":
        with open(outfile1, mode='a+') as f:
            f.write('{},{},{}\n'.format(request.form['id'], request.form['classify'],
                request.form['notes'].replace(',','\\,')))
    return render_template('page.html', galaxy=galaxy, n_images=n_images, page=page, n=1)

@app.route('/classify_2/<int:page>', methods=['GET','POST'])
def classify_2(page):
    df = df_cut.query('(Diam <= 1) & (Diam > 0.5)').reset_index()
    n_images = df.shape[0]
    row = df.iloc[page-1]
    galaxy = row.to_dict()
    if request.method == "POST":
        with open(outfile2, mode='a+') as f:
            f.write('{},{},{}\n'.format(request.form['id'], request.form['classify'],
                request.form['notes'].replace(',','\\,')))
    return render_template('page.html', galaxy=galaxy, n_images=n_images, page=page, n=2)

@app.route('/classify_3/<int:page>', methods=['GET','POST'])
def classify_3(page):
    df = df_cut.query('(Diam <= 0.5)').reset_index()
    n_images = df.shape[0]
    row = df.iloc[page-1]
    galaxy = row.to_dict()
    if request.method == "POST":
        with open(outfile3, mode='a+') as f:
            f.write('{},{},{}\n'.format(request.form['id'], request.form['classify'],
                request.form['notes'].replace(',','\\,')))
    return render_template('page.html', galaxy=galaxy, n_images=n_images, page=page, n=3)

@app.route('/classify_4/<int:page>', methods=['GET','POST'])
def classify_4(page):
    df = df_all.query('(Diam >= 5)').reset_index()
    n_images = df.shape[0]
    row = df.iloc[page-1]
    galaxy = row.to_dict()
    if request.method == "POST":
        with open(outfile4, mode='a+') as f:
            f.write('{},{},{}\n'.format(request.form['id'], request.form['classify'],
                request.form['notes'].replace(',','\\,')))
    return render_template('page.html', galaxy=galaxy, n_images=n_images, page=page, n=4)

@app.route('/results', methods=['GET'])
def show_table():
    return render_template('index.html', table = pd.read_csv(outfile, escapechar='\\').to_html(index=False))

@app.route('/results.csv', methods=['GET'])
def send_csv():
    return send_file(outfile)

@app.route('/results_1', methods=['GET'])
def show_table_1():
    return render_template('index.html', table = pd.read_csv(outfile1, escapechar='\\').to_html(index=False))

@app.route('/results_1.csv', methods=['GET'])
def send_csv_1():
    return send_file(outfile1)

@app.route('/results_2', methods=['GET'])
def show_table_2():
    return render_template('index.html', table = pd.read_csv(outfile2, escapechar='\\').to_html(index=False))

@app.route('/results_2.csv', methods=['GET'])
def send_csv_2():
    return send_file(outfile2)

@app.route('/results_3', methods=['GET'])
def show_table_3():
    return render_template('index.html', table = pd.read_csv(outfile3, escapechar='\\').to_html(index=False))

@app.route('/results_3.csv', methods=['GET'])
def send_csv_3():
    return send_file(outfile3)

@app.route('/results_4', methods=['GET'])
def show_table_4():
    return render_template('index.html', table = pd.read_csv(outfile4, escapechar='\\').to_html(index=False))

@app.route('/results_4.csv', methods=['GET'])
def send_csv_4():
    return send_file(outfile4)

if __name__ == '__main__':
    app.debug = False # set this to false before putting on production!!!
    app.run()
