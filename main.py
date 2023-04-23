from flask import Flask,render_template,request,flash#,abort,session,jsonify,redirect,url_for
from coder import Myclass
from firebase_admin import credentials,auth
import pyrebase

app=Flask(__name__,static_url_path='/static',static_folder='static')

config = {
    'apiKey': "AIzaSyD3NrOZZkICuDTOQMgCGydz_5ZGi-R8Lbg",
    'authDomain': "word-d1791.firebaseapp.com",
    'projectId': "word-d1791",
    'storageBucket': "word-d1791.appspot.com",
    'messagingSenderId': "378498108244",
    'appId': "1:378498108244:web:c1a6776f5d1852b61696c1",
    'measurementId': "G-FW14HLJLFQ",
    'databaseURL' : ""
}


firebase=pyrebase.initialize_app(config)
auth=firebase.auth()


app = Flask(__name__)
app.secret_key='cn4bhbh6h6'


@app.route('/')
def home():
    return render_template('home.html')


global score
global lives
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/sign_up')
def sigin_up():
    return render_template('sign_up.html')


@app.route('/scramble')
def scramble():
    global val_score
    val_score=0
    global lives
    lives=3
    obj=Myclass()
    tosend,hint=obj.fun()
    lst.append(obj.wk)
    return render_template('scramble.html',word=tosend,hint=hint,lives=lives,val_score=val_score)

global lst
lst=[""]


@app.route('/word_entered', methods=['POST'])
def reter():
    global score
    global lives
    global player_score
    global player_email
    btn=request.form['button']
    obj = Myclass()
    tosend, hint = obj.fun()
    lst.append(obj.wk)
    if btn=='Quit':
        with open('scores.txt', 'r+') as file:
            lines = file.readlines()
            email_found = False
            for i, line in enumerate(lines):
                parts = line.strip().split(',')
                if parts[0] == player_email:
                    lines[i] = f"{player_email},{player_score}\n"
                    email_found = True
                    current_score = int(line.strip().split(',')[1])
                    print(current_score)
                    print(player_score)
                    lines[i] = f"{player_email},{max(player_score,current_score)}\n"
                    break
            if not email_found:
                lines.append(f"{player_email},{player_score}\n")
            file.seek(0)
            file.truncate()
            file.writelines(lines)
        score=0
        lives=3
        return render_template("quit.html",score=player_score)
    if len(lst)==2:
        k=lst[-1]
    else:
        k=lst[-2]
    print(lst)
    print(k)
    if btn=='Next':
        word= request.form['entered_word']
        if(word==''):
            lives=lives-1
            val_score=score
        else:
            lives,val_score=obj.validat(word,k,score,lives)
            score=val_score
            player_score=score
        if lives==0:
            with open('scores.txt', 'r+') as file:
                lines = file.readlines()
                email_found = False
                for i, line in enumerate(lines):
                    parts = line.strip().split(',')
                    if parts[0] == player_email:
                        lines[i] = f"{player_email},{player_score}\n"
                        email_found = True
                        current_score = int(line.strip().split(',')[1])
                        print(current_score)
                        print(player_score)
                        lines[i] = f"{player_email},{max(player_score, current_score)}\n"
                        break
                if not email_found:
                    lines.append(f"{player_email},{player_score}\n")
                file.seek(0)
                file.truncate()
                file.writelines(lines)
            player_score=score
            return render_template("quit.html",score=player_score)
        return render_template("scramble.html",word=tosend,hint=hint,lives=lives,val_score=val_score)
    else:
        lives,val_score =lives,score #obj.validat()
        return render_template("scramble.html",word=tosend,hint=hint,lives=lives,val_score=val_score)


@app.route('/your_signup', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']

    try:
        user = auth.create_user_with_email_and_password(email,password)
        return render_template('login.html')
    except:
        flash('E-mail already exists')
        return render_template('login.html')


@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')


@app.route('/quit')
def quit():
    return render_template('quit.html')

@app.route('/play_again')
def play_again():
    return render_template('game.html')


@app.route('/user_data', methods=['POST'])
def user_data():
    email = request.form['email']
    password = request.form['password']
    try:
        global player_email
        global player_score
        player_email = email
        player_score=0
        global score
        global lives
        lives = 3
        score = 0
        user=auth.sign_in_with_email_and_password(email,password)
        return render_template('game.html')
    except:
        return render_template('login.html', error='Invalid email or password')


@app.route('/admin_data', methods=['POST'])
def admin_data():
    email = 'admin@gmail.com'
    password = request.form['admin_password']
    print(email)
    try:
        user=auth.sign_in_with_email_and_password(email,password)
        info=auth.get_account_info(user['idToken'])
        with open('scores.txt', 'r') as file:
            lines = file.readlines()
        scores = [(line.strip().split(',')[0], line.strip().split(',')[1]) for line in lines]
        return render_template('dashboard.html', scores=scores,email=email)
    except:
        return render_template('login.html', error='Invalid email or password')


if __name__ == '__main__':
    app.run(debug=True)