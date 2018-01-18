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

df_jd = pd.read_csv('static/jd_selections.csv', dtype=str)
df_jd.fillna('None', inplace=True)

df_jd2 = pd.read_csv('static/jd_round3_ned.csv', dtype=str, index_col='ID')
df_jd2.fillna('None', inplace=True)

df_jd3 = pd.read_csv('static/jd_round3_ned_2.csv', dtype=str, index_col='ID')
df_jd3.fillna('None', inplace=True)

df_final = pd.read_csv('static/revised.csv', dtype=str, index_col='ID')
df_final.fillna('None', inplace=True)


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

handle_jd, outfile_jd = tempfile.mkstemp()
with open(outfile_jd, mode='w') as f:
    f.write('ID,Score,RA,Dec,Notes\n')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', table = df_all.to_html(index=False))

@app.route('/gallery', methods=['GET'])
def gallery():
    thumb_list = []
    for name,k in df_jd2['Keep?'].iteritems():
        img = 'static/img/{}.jpg'.format(name)
        if not os.path.exists(img):
            img = 'static/img/{}.jpg'.format(name[:-1])
        thumb_dict = {'img':img, 'name':name, 'shortname':name.replace('Arp-Madore','AM'), 'keep':k}
        thumb_list.append(thumb_dict)
    return render_template('gallery.html', thumb_list = thumb_list)

@app.route('/gallery2', methods=['GET'])
def gallery2():
    thumb_list = []
    for name, k in df_jd3['Score'].iteritems():
        img = 'static/img/{}.jpg'.format(name)
        if not os.path.exists(img):
            img = 'static/img/{}.jpg'.format(name[:-1])
        thumb_dict = {'img':img, 'name':name, 'shortname':name.replace('Arp-Madore','AM'), 'keep':k}
        thumb_list.append(thumb_dict)
    return render_template('gallery2.html', thumb_list = thumb_list)

@app.route('/gallery_final', methods=['GET'])
def gallery_final():
    thumb_list = []
    for name in df_final.index.values:
        img = 'static/img/{}_lg.jpg'.format(name)
        thumb_dict = {'img':img, 'name':name, 'shortname':name.replace('Arp-Madore','AM')}
        thumb_list.append(thumb_dict)
    return render_template('gallery_final.html', thumb_list = thumb_list)

cols = 'RA,Dec,ObjectName,Object,Score,Notes,Galactic Extinction,cz,z,Basic-Data,Basic-Data.1,Galaxy Morphology,Activity Type,Kronap.AB,Kronap.AB.1,Kronap.AB.2,Kronap.AB.3,K_s_total,K_s_total.1,K_s_total.2,K_s_total.3,25micron,25micron.1,25micron.2,25micron.3,60micron,60micron.1,60micron.2,60micron.3,1.4GHz,1.4GHz.1,1.4GHz.2,1.4GHz.3,1.4GHz.4,1.4GHz.5,1.4GHz.6,1.4GHz.7,20.0K-magarcsec^-2,25.0B-magarcsec^-2'.split(',')

from collections import OrderedDict

@app.route('/view/<arp>', methods=['GET'])
def view(arp):
    try:
        galaxy = df_jd2[cols].loc[arp].to_dict(into=OrderedDict)
    except:
        try:
            galaxy = df_jd3.loc[arp].to_dict(into=OrderedDict)
        except:
            galaxy = df_final.loc[arp].to_dict(into=OrderedDict)
    return render_template('view.html', galaxy = galaxy)

@app.route('/classify_5/<int:page>', methods=['GET','POST'])
def classify_5(page):
    n_images = df_jd.shape[0]
    row = df_jd.iloc[page-1]
    galaxy = row.to_dict()
    hst = pd.read_csv('https://archive.stsci.edu/hst/search.php?RA={}&DEC={}&radius=6&max_records=100&outputformat=CSV&action=Search'.format(galaxy['RA'],
        galaxy['Dec'])).shape[0]
    if hst == 0:
        hst = 'None'
    elif hst >= 100:
        hst = '100+'
    else:
        hst -= 1
    if request.method == "POST":
        with open(outfile_jd, mode='a+') as f:
            f.write('{},{},{},{}\n'.format(request.form['id'], request.form['classify'],
                request.form['coords'], request.form['notes'].replace(',','\\,')))
    return render_template('page.html', galaxy=galaxy, n_images=n_images, page=page, n=5, hst=hst)

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

@app.route('/results_5', methods=['GET'])
def show_table_jd():
    return render_template('index.html', table = pd.read_csv(outfile_jd, escapechar='\\').to_html(index=False))

@app.route('/results_5.csv', methods=['GET'])
def send_csv_jd():
    return send_file(outfile_jd)

if __name__ == '__main__':
    app.debug = False # set this to false before putting on production!!!
    app.run()
