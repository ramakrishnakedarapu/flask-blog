from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from bson.objectid import ObjectId
import bcrypt

from pymongo import MongoClient
client = MongoClient('mongodb+srv://ramakrishnakedarapu:5RsjGiXFhcQQEx62@cluster0.b4outis.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.Cluster0
product = db.product
user_log = db.login

app = Flask( __name__ )
app.config['SECRET_KEY'] = 'testing'

# Routes
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/editpost')
def editpost():
    if request.method == 'POST':
        render_template('editpost.html')
        print("test")
    
    all_posts = product.find()
    return render_template( 'editpost.html', product=all_posts)

@app.route('/dashboard')
def dashboard():
    if request.method == 'POST':
        render_template('posts.html')
        print("test")

    all_posts = product.find()
    return render_template('dashboard.html', product=all_posts)

@app.route('/articles', methods=( 'GET','POST' ))
def articles():
    if request.method == 'POST':
        render_template('posts.html')
        print("test")
    all_posts = product.find()

    return render_template('articles.html', product=all_posts)




@app.route('/login', methods=("GET", "POST"))
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        decoding = password.encode('utf-8')
        stored_password = user_log.find_one({'email': email})

        if stored_password and bcrypt.checkpw(decoding, stored_password['password']):
            print("match")
            session['email'] = email
            return redirect(url_for('dashboard'))
        else:
            print("does not match")
            return render_template('login.html')

    else:
        return render_template('login.html')


def create_hashed_password(password):
    encoded = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(encoded, salt)
    return hashed



@app.route('/register', methods=("GET", "POST"))
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if len(password) >= 7:
            hashed = create_hashed_password(password)
            print(hashed)
            user_log.insert_one({'email': email, 'password': hashed})
            return redirect(url_for('home'))
        else:
            return render_template('register.html')
    else:
        return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))


@app.route("/posts", methods=("GET", "POST"))
def posts():
    name = request.args.get('name')
    query = {"name": name}
    content = product.find(query)
    print(query)
    search_results = [result for result in content]
    return render_template('posts.html', search_results=search_results)

@app.route('/write', methods=("GET", "POST"))
def write():
    if 'email' in session:
        if request.method == 'POST':
            content = request.form['name']
            degree = request.form['content']
            product.insert_one({'name': content, 'content': degree})
            return redirect(url_for('write'))

        all_posts = product.find()
        return render_template('write.html', product=all_posts, email=session['email'])

    else:
        return redirect(url_for('login'))



@app.route('/<id>/delete/', methods=("GET", "POST"))
def delete(id):
    product.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('dashboard'))


@app.route('/<id>/edit/', methods=("GET", "POST"))
def edit(id):
    name = request.form['name']
    content = request.form['content']
    product.update_one({"_id": ObjectId(id)}, {'$set': {'name': name, 'content': content}})
    return redirect(url_for('dashboard'))


@app.route('/process', methods=['POST'])
def process():
    find = request.form.get('search_query')
    query = {"name": find}
    results = product.find(query)

    search_results = [result for result in results]

    return render_template('search_results.html', search_results=search_results)





