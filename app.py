from flask import Flask, render_template, request, redirect, session, url_for
import pymongo
import urllib 
from util import get_user_posts, encode_text, decode_text

mongo_uri = "mongodb+srv://gk2605:"+ urllib.parse.quote("Gunkirat@16") +"@cluster0.sgvz48r.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(mongo_uri)

app = Flask(__name__)

app.secret_key = 'SECRET_KEY'

username_auth = ""
email_auth = ""


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.form['username']
        password = request.form['password']

        db = client.OpioidsData
        collection_User = db.Annotators
        cursor_user = collection_User.find()
        users = list(cursor_user)
        # Check if the username and password are correct
        for user in users:
            if user['username'] == username and decode_text(user['password']) == password:
                username_auth = user['username']
                email_auth = user["email"]
                # Redirect the user to the dashboard
                return redirect(url_for('index', username_auth= username_auth, email_auth=email_auth))

    # If the request method is GET, show the login form
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the username, email, and password from the form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        db = client.OpioidsData
        collection_User = db.Annotators
        item = {'username': username, 'email': email, 'password': encode_text(password)}
        # Add the new user to the list of users
        rec_id1 = collection_User.insert_one(item)

        # Redirect the user to the login page
        return redirect(url_for('login'))

    # If the request method is GET, show the signup form
    return render_template('signup.html')

@app.route('/start', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print('Button clicked!')
        username_auth = request.args.get('username_auth')
        email_auth = request.args.get('email_auth')
        return redirect(url_for('form_page', username_auth= username_auth, email_auth=email_auth))
    return render_template('index.html')

@app.route('/form-page')
def form_page():
    data_posts, user_id, user_id_count, user_name = get_user_posts(client)
    username_auth = request.args.get('username_auth')
    email_auth = request.args.get('email_auth')
    return render_template('form.html',data_posts = enumerate(data_posts), user_id = user_id, user_name = user_name, length = len(data_posts), username_auth= username_auth, email_auth=email_auth)

@app.route('/submit', methods=['POST'])
def submit():
    db = client.OpioidsData
    collection_PostSubmission = db.PostsSubmission
    collection_PostAnnotatedCounter = db.PostsAnnotatedCounter
    for i in range(int(request.form.get('length'))):
        # print("itemname",item_name)
        user_id_post = request.form.get('User_id{}'.format(i+1))
        user_name_ = request.form.get('User_name{}'.format(i+1))
        post_id = request.form.get('Post_id{}'.format(i+1))
        time = request.form.get('Time{}'.format(i+1))
        title = request.form.get('Title{}'.format(i+1))
        body = request.form.get('Body{}'.format(i+1))
        label = request.form.get('answer{}'.format(i+1))
        Explanation = request.form.get('Explanation{}'.format(i+1))
        username_auth = request.form.get('username_auth')
        email_auth = request.form.get('email_auth')
        ps_item = {
            "post_id":post_id,
            "user_id":user_id_post,
            "user_name":user_name_,
            "time": time,
            "title":title,
            "body":body,
            "label":label,
            "explanation":Explanation,
            "annotator_name": username_auth,
            "annotator_email":email_auth
        }

        rec_id1 = collection_PostSubmission.insert_one(ps_item)
    cursor_PostAnnotatedCounter = collection_PostAnnotatedCounter.find( { 'user_id': { "$eq": int(user_id_post) } })
    data_PostAnnotatedCounter = list(cursor_PostAnnotatedCounter)
    user_id_count_ = int(data_PostAnnotatedCounter[0]['count'])
    user_id_count_ = user_id_count_+1
    response = collection_PostAnnotatedCounter.update_one({"user_id" : int(user_id_post)},{"$set": { "count" : user_id_count_}});
    return redirect(url_for('form_page', username_auth= username_auth, email_auth=email_auth))

@app.route('/logout', methods=['POST'])
def logout():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
