from flask import Flask, render_template, redirect, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    age = db.Column(db.Integer, unique=True, nullable=True)
    image = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(80), nullable=False)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class UserAddForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    age = IntegerField('Age', validators=[DataRequired()])
    submit = SubmitField('Save')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProfileEditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Save')

class CalcForm(FlaskForm):
    num1 = IntegerField('Num1', validators=[DataRequired()])
    num2 = IntegerField('Num2', validators=[DataRequired()])
    submit = SubmitField('Calculate')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/home/upload', methods=['POST'])
def upload_file():
    # Получение загруженного файла из запроса
    file = request.files['file']

    # Проверка, что файл был отправлен и имеет допустимое расширение
    if file and allowed_file(file.filename):
        # Безопасное сохранение файла с учетом его имени
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Получение списка имен загруженных файлов
        filenames = os.listdir(app.config['UPLOAD_FOLDER'])
        return redirect('profile.html')
    else:
        return 'Недопустимый файл. <a href="/">Вернуться</a>'

@app.route('/home')
@login_required
def home():
    return render_template('index.html')

@app.route('/check')
def check():
    return redirect('/home')

@app.route('/test-addition', methods=['GET', 'POST'])
def testadd():
    form = CalcForm()
    if form.validate_on_submit():
        a = form.num1.data
        b = form.num2.data
        answer = a + b
        flash("Answer: " + str(answer), "Answer")
    return render_template('calc.html', form=form)

@app.route('/test-subtraction', methods=['GET', 'POST'])
def testsub():
    form = CalcForm()
    if form.validate_on_submit():
        a = form.num1.data
        b = form.num2.data
        answer = a - b
        flash("Answer: " + str(answer), "Answer")
    return render_template('calc.html', form=form)

@app.route('/test-multiplication', methods=['GET', 'POST'])
def testmult():
    form = CalcForm()
    if form.validate_on_submit():
        a = form.num1.data
        b = form.num2.data
        answer = a * b
        flash("Answer: " + str(answer), "Answer")
    return render_template('calc.html', form=form)


@app.route('/test-division', methods=['GET', 'POST'])
def testdiv():
    form = CalcForm()
    if form.validate_on_submit():
        a = form.num1.data
        b = form.num2.data
        answer = a / b
        flash("Answer: " + str(answer), "Answer")
    return render_template('calc.html', form=form)

@app.route("/home/profile", methods=['GET','POST'])
@login_required
def profile():
    form = ProfileEditForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(id=current_user.id).first()
        if not existing_user:
            return ""
        existing_user.username = form.username.data
        existing_user.email = form.email.data
        db.session.commit()
        flash('Edit success', 'success')
        return redirect('/home/profile')
    return render_template('profile.html', form=form)

@app.route('/home/users')
def testusers():
    users = User.query.all()
    return render_template('testusers.html', users=users)



@app.route('/home/users/edit/<int:id>',methods=["POST","GET"])
def users_edit(id):
    user = User.query.get_or_404(id)
    if request.method == "POST":
        user.username = request.form['username']
        user.email = request.form['email']
        user.age = request.form['age']
        db.session.commit()
        return redirect('/home/users')
    return render_template('users_edit.html', user=user)


@app.route('/home/users/delete/<int:id>', methods=["GET"])
def users_delte(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/home/users')

@app.route('/home/users/read/<int:id>',methods=["GET"])
def users_read(id):
    user = User.query.get_or_404(id)
    return render_template('users_read.html', user=user)

    return render_template('users_delete.html', user=user)

@app.route('/home/2048')
@login_required
def game2048():
    return render_template('2048.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/data', methods=['GET'])
def get_data():
    data = {'name': 'Arlen', 'age': 11}
    return jsonify(data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists! Please choose a different one.', 'danger')
            return redirect('/register')
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect('/login')
    return render_template('register.html', form=form)

@app.route('/home/users/add',methods=["POST","GET"])
def users_add():
    form = UserAddForm()
    if request.method == 'POST' and form.validate_on_submit():
        # existing_user = User.query.filter_by(username=form.username.data).first()
        # if existing_user:
        #     flash('Username already exists! Please choose a different one.', 'danger')
        #     return redirect('/home/users/add')
        user = User(username=form.username.data, email=form.email.data, age=form.age.data)
        form.email.data = user.email
        form.username.data = user.username
        form.age.data = user.age
        db.session.add(user)
        db.session.commit()
        flash('Adding User successful! You can now view it.', 'success')
        return redirect('/home/users')
    return render_template('users_add.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            flash('Login successful!', 'success')
            login_user(user)
            return redirect('/home')
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    return render_template('login.html', form=form)

@app.errorhandler(404)
def error404(error):
    error_message = {'Error 404': 'Page not Found'}
    return render_template('error404.html'), 404

@app.errorhandler(500)
def error500(error):
    error_message = {'Error 500': 'Server not Found'}
    return jsonify(error_message), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run('0.0.0.0', 80, debug=True)
