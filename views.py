from flask import Flask, session, redirect, url_for, escape, request, render_template, g, make_response, send_file, current_app as app
import os
import sqlite3
import link
from OpenSSL import SSL


context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('domain.key')
context.use_certificate_file('domain.crt')

app = Flask(__name__)
DATABASE = 'linkedsume.db'
app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'linkedsume.db'),
    DEBUG = True,
    SECRET_KEY = '\xdc\xc1_tP\x85\x12\x8d\xd7\xdc\xa4\x17\x10\x01\xe8"\xc2\xd1\xfb\xf6?4\xe3\x86'
))
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g,'_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query,args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/', methods = ['GET', 'POST'])
def generate():
    error = None
    if 'code' in request.args:
        generate = "https://localhost:5000/?code=" + request.args['code']
        link.make_json(generate)
        os.system("lualatex resume.tex")
    if request.method == 'POST':
        static_file = open('resume.pdf', 'rb')
        response = send_file(static_file, attachment_filename='resume.pdf')
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = \
            'inline; filename=%s.pdf' % 'resume'
        return response
    return render_template('Generate.html', error = error)

@app.route('/authorize', methods = ['GET', 'POST'])
def authorize():
    error = None
    if request.method == 'POST':
        redirection = link.author()
        return redirect(redirection)
    return render_template('Authorize.html', error = error)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        db = get_db()
        user = query_db('select * from users where username = ?', [request.form['username']], one = True)
        if user != None:
            return render_template('repeatedusername.html', error = error)
        command = 'insert into users (user_id, username, password) values (?,?,?)'
        command_args = [None, request.form['username'], request.form['password']]
        db.execute(command,command_args)
        db.commit()
        return redirect(url_for('login'))
    return render_template('Linkedsume.html', error = error)

@app.route('/login', methods = ['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        user = query_db('select * from users where username = ?', [request.form['username']], one = True)
        if user == None:
            return render_template('invalidinput.html', error = error)
        elif user[2] != request.form['password']:
            return render_template('invalidinput.html', error = error)
            #showing invalid username/password
        else:
            session['logged_in'] = True
            return redirect(url_for('authorize'))
    return render_template('login.html', error = error)


if __name__ == "__main__":
    context = ('domain.crt', 'domain.key')
    app.run(host='127.0.0.1', port=5000, ssl_context=context, threaded=True, debug=True)
