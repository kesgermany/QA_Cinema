from application import app, db
from flask import render_template, request, redirect, url_for, flash, session
from models import User
from werkzeug.security import check_password_hash, generate_password_hash
from models import Movie, Discussion
from forms import DiscussionPost, PayForm


app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'    

'''
the following app.py file defines all known routes
'''
@app.route("/")
def home():
    return render_template ("homepage.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/openingtimes")
def opening_times():
    return render_template("opening.html")

@app.route("/classifications")
def classifications():
    return render_template("classification.html")

@app.route("/screens")
def screens():
    return render_template("screens.html")

@app.route("/services")
def cinema_services():
    return render_template("services.html")

@app.route("/movies/<int:movie_id>")
def view_movie():
    return render_template("movie.html")

@app.route("/listings")
def listings():
    return render_template("gallery.html")

@app.route('/newreleases', methods=['GET'])
def new_releases():
    from models import Movie  

    new_releases = Movie.query.filter_by(classic=False).all()
    
    return render_template('new_releases.html', films=new_releases)

@app.route("/classics", methods=['GET'])
def classics():

    classics = Movie.query.filter_by(classic=True).all()

    return render_template('classics.html', films=classics)


@app.route("/serchresults")
def search_results():
    return render_template("gallery.html")

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    message = ""
    form = PayForm()
    if request.method == 'POST':
            first_name = form.first_name.data
            last_name = form.last_name.data
            message = f'Thank you ,{ first_name} {last_name} Payment has been accepted' 
    return render_template('payment.html', form=form, message=message)


@app.route("/signup", methods=["GET","POST"])
def signup():

    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        if User.check_unique_username != True:
            flash("user already exists")
        
        password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        new_user = User.add_user(username, email, password_hash)

        return render_template("login.html")

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        session["username"] = request.form["username"]
        username = request.form.get("username")
        password = request.form.get("password")

        # below we retrieve user by username and check if the password is correct
        user = User.retrieve_user(username)
        if user is not None:
            if check_password_hash(user.password, password):
                session["username"] = user.username

            print(session["username"])
        return redirect ("/")
    
    return render_template ("login.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    if request.method == "POST":
        # Clear the user's session
        session.clear()
        return redirect("/")
    return render_template("logout.html")

@app.route('/forum', methods=["GET","POST"])
def discussionboard():
    
    all_posts= Discussion.all_discussion()
    form = DiscussionPost()

    if request.method == "POST":
        if form.validate_on_submit():
            with app.app_context():
                new_post = Discussion(
                    user_id = form.user_id.data,
                    movie_id = form.user_id.data,
                    topic = form.topic.data,
                    comment = form.comment.data,
                    timestamp = form.timestamp.data
                )
                db.session.add(new_post)
                db.session.commit()
                all_posts= Discussion.all_discussion()

    return render_template('discussion-board.html', all_posts=all_posts, form=form)
