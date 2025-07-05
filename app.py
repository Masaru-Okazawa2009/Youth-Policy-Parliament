from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Email
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    is_legislator = db.Column(db.Boolean, default=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='topics')

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegisterForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired(), Length(max=80)])
    age = IntegerField('年齢', validators=[DataRequired(), NumberRange(min=0, max=18, message='18歳以下のみ登録できます')])
    password = PasswordField('パスワード', validators=[DataRequired()])
    submit = SubmitField('登録')

class LoginForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired()])
    password = PasswordField('パスワード', validators=[DataRequired()])
    submit = SubmitField('ログイン')

class ProposeForm(FlaskForm):
    title = StringField('タイトル', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('内容', validators=[DataRequired()])
    submit = SubmitField('送信')

class ContactForm(FlaskForm):
    name = StringField("名前", validators=[DataRequired(), Length(max=80)])
    email = StringField("メール", validators=[DataRequired(), Email()])
    message = TextAreaField("メッセージ", validators=[DataRequired()])
    submit = SubmitField("送信")


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('すでに同じユーザー名が存在します')
        else:
            user = User(username=form.username.data, age=form.age.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('登録完了しました。ログインしてください')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('ログインしました')
            return redirect(url_for('index'))
        else:
            flash('ユーザー名またはパスワードが間違っています')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました')
    return redirect(url_for('index'))

@app.route('/propose', methods=['GET', 'POST'])
@login_required
def propose():
    form = ProposeForm()
    if form.validate_on_submit():
        topic = Topic(title=form.title.data, description=form.description.data, user=current_user)
        db.session.add(topic)
        db.session.commit()
        flash('議題を提案しました')
        return redirect(url_for('index'))
    return render_template('propose.html', form=form)

@app.route("/info")
def info():
    return render_template("info.html")

@app.route("/participation")
def participation():
    return render_template("participation.html")

@app.route("/news")
def news():
    return render_template("news.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = ContactMessage(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash("送信しました")
        return redirect(url_for("index"))
    return render_template("contact.html", form=form)

@app.route('/legislator')
@login_required
def legislator():
    if not current_user.is_legislator:
        flash('アクセス権がありません')
        return redirect(url_for('index'))
    return render_template('legislator.html')

@app.route('/vote')
def vote():
    # Replace with your actual Google Form URL
    google_form_url = 'https://docs.google.com/forms/d/e/your-form-id/viewform?embedded=true'
    return render_template('vote.html', google_form_url=google_form_url)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
