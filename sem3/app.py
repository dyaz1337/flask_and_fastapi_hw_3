from sqlalchemy.exc import OperationalError
from flask import Flask, render_template, redirect, url_for, flash
from models import db, Student, Faculty, Author, Book, Grade, UserT4, UserT5, UserT7
from forms import RegFormT4, RegFormT5, RegFormT7, LoginFormT7

import random

app = Flask(__name__)
app.config['SECRET_KEY'] = b'8fda4c95f8ced93390919e911abb6b9dcd317ac21a6662e23748d47345e1cb72'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'

db.init_app(app)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('OK')


@app.cli.command('fill-db')
def fill_db_tables():
    for i in range(1, 6):
        new_faculty = Faculty(name=f"Faculty_{i}")
        db.session.add(new_faculty)
    db.session.commit()

    for i in range(1, 11):
        new_student = Student(
            first_name=f'Имя {i}',
            last_name=f'Фамилия {i}',
            age=random.randint(10, 90),
            gender=random.choice([True, False]),
            group=random.randint(100, 200),
            email=f'email{i}',
            faculty_id=random.randint(1, 5)
        )
        db.session.add(new_student)
    db.session.commit()

    for i in range(50):
        new_grade = Grade(
            subject=f"Предмет {random.randint(1, 5)}",
            grade=random.randint(1, 5),
            student_id=i % 10 + 1
        )
        db.session.add(new_grade)
    db.session.commit()

    for i in range(1, 6):
        new_author = Author(
            first_name=f"Имя {i}",
            last_name=f"Фамилия {i}"
        )
        db.session.add(new_author)
    db.session.commit()

    for i in range(1, 21):
        new_book = Book(
            name=f"Книга {i}",
            year=random.randint(1900, 2000),
            count=random.randint(1, 5),
            author_id=random.randint(1, 5)
        )
        db.session.add(new_book)
    db.session.commit()
    print('OK')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


def result(message):
    return render_template('result.html', message=message)


# Создать базу данных для хранения информации о студентах университета.
# База данных должна содержать две таблицы: "Студенты" и "Факультеты".
# В таблице "Студенты" должны быть следующие поля: id, имя, фамилия, возраст, пол, группа и id факультета.
# В таблице "Факультеты" должны быть следующие поля: id и название факультета.
# Необходимо создать связь между таблицами "Студенты" и "Факультеты".
# Написать функцию-обработчик, которая будет выводить список всех студентов с указанием их факультета.
@app.route('/task1/')
def task1_index():
    try:
        students = Student.query.all()
    except OperationalError:
        students = None
    return render_template('task1/index.html', students=students, title="task1")


# Создать базу данных для хранения информации о книгах в библиотеке.
# База данных должна содержать две таблицы: "Книги" и "Авторы".
# В таблице "Книги" должны быть следующие поля:
# id, название, год издания, количество экземпляров и id автора.
# В таблице "Авторы" должны быть следующие поля: id, имя и фамилия.
# Необходимо создать связь между таблицами "Книги" и "Авторы".
# Написать функцию-обработчик,
# которая будет выводить список всех книг с указанием их авторов.
@app.route('/task2/')
def task2_index():
    try:
        books = Book.query.all()
    except OperationalError:
        books = None
    return render_template('task2/index.html', books=books, title='task2')


# Доработаем задача про студентов
# Создать базу данных для хранения информации о студентах и их оценках в учебном заведении.
# База данных должна содержать две таблицы: "Студенты" и "Оценки".
# В таблице "Студенты" должны быть следующие поля: id, имя, фамилия, группа и email.
# В таблице "Оценки" должны быть следующие поля: id, id студента, название предмета и оценка.
# Необходимо создать связь между таблицами "Студенты" и "Оценки".
# Написать функцию-обработчик, которая будет выводить список всех студентов с указанием их оценок.
@app.route('/task3/')
def task3_index():
    try:
        grades = Grade.query.join(Student).order_by(Grade.subject, Student.first_name, Student.last_name).all()
    except OperationalError:
        grades = None
    return render_template('task3/index.html', grades=grades, title='task3')


# Создайте форму регистрации пользователя с использованием Flask-WTF.
# Форма должна содержать следующие поля:
# Имя пользователя (обязательное поле)
# Электронная почта (обязательное поле, с валидацией на корректность ввода email)
# Пароль (обязательное поле, с валидацией на минимальную длину пароля)
# Подтверждение пароля (обязательное поле, с валидацией на совпадение с паролем)
# После отправки формы данные должны сохраняться в базе данных (можно использовать SQLite)
# и выводиться сообщение об успешной регистрации.
# Если какое-то из обязательных полей не заполнено или данные не прошли валидацию,
# то должно выводиться соответствующее сообщение об ошибке.
# Дополнительно: добавьте проверку на уникальность имени пользователя и электронной почты в базе данных.
# Если такой пользователь уже зарегистрирован, то должно выводиться сообщение об ошибке.
@app.route('/task4/', methods=['GET', 'POST'])
@app.route('/task4/registration', methods=['GET', 'POST'])
def task4_registration():
    form = RegFormT4()
    if form.validate_on_submit():
        is_errors = False
        name = form.name.data
        email = form.email.data
        password = form.password.data
        if UserT4.query.filter_by(name=name).first():
            form.name.errors.append("Такое Имя уже присутствует! Выберите другое.")
            is_errors = True
        if UserT4.query.filter_by(email=email).first():
            form.email.errors.append("Такая Почта уже присутствует! Выберите другую.")
            is_errors = True
        if not is_errors:
            new_user = UserT4(
                name=name,
                email=email,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()
            return result(f"{name}, Добро пожаловать!")
    return render_template('task4/registration.html', form=form, title='task4')


# Создать форму регистрации для пользователя.
# Форма должна содержать поля:
# имя, электронная почта,пароль (с подтверждением), дата рождения, согласие на обработку персональных данных.
# Валидация должна проверять, что все поля заполнены корректно
# (например, дата рождения должна быть в формате дд.мм.гггг).
# При успешной регистрации пользователь должен быть перенаправлен на страницу подтверждения регистрации.
@app.route('/task5/', methods=['GET', 'POST'])
@app.route('/task5/registration', methods=['GET', 'POST'])
def task5_registration():
    form = RegFormT5()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        birth_date = form.birth_date.data
        new_user = UserT5(
            name=name,
            email=email,
            password=password,
            birth_date=birth_date
        )
        db.session.add(new_user)
        db.session.commit()
        return result(f'{name}, Добро пожаловать')
    return render_template('task5/registration.html', form=form, title='task5')


# Создайте форму регистрации пользователей в приложении Flask.
# Форма должна содержать поля: имя, фамилия, email, пароль и подтверждение пароля.
# При отправке формы данные должны валидироваться на следующие условия:
# ○ Все поля обязательны для заполнения.
# ○ Поле email должно быть валидным email адресом.
# ○ Поле пароль должно быть зашифровано,
# а так же содержать не менее 8 символов, включая хотя бы одну букву и одну цифру.
# ○ Поле подтверждения пароля должно совпадать с полем пароля.
# ○ Если данные формы не прошли валидацию, на странице должна быть выведена соответствующая ошибка.
# ○ Если данные формы прошли валидацию, на странице должно быть выведено сообщение об успешной регистрации.
@app.route('/task7/registration', methods=['GET', 'POST'])
@app.route('/task7/', methods=['GET', 'POST'])
def task7_registration():
    form = RegFormT7()
    if form.validate_on_submit():
        is_error = False
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password: str = form.password.data
        if UserT7.query.filter_by(email=email).first():
            is_error = True
            form.email.errors.append('Эта почта уже зарегистрирована!')
        if not any(char.isdigit() for char in password):
            is_error = True
            form.password.errors.append('В пароле должна быть хоть 1 цифра!')
        if not any(char.isupper() for char in password):
            is_error = True
            form.password.errors.append('В пароле должна быть хоть 1 заглавная буква!')
        if not is_error:
            new_user = UserT7(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('task7_login'))
    return render_template('task7/registration.html', form=form, title='task7')


@app.route('/task7/login', methods=['GET', 'POST'])
def task7_login():
    form = LoginFormT7()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = UserT7.query.filter_by(email=email).first()
        if user and user.verify_password(password):
            return result("Добро пожаловать!")
        flash('Почта и/или пароль не подошли.', 'danger')
    return render_template('task7/login.html', form=form, title='task7')


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


if __name__ == '__main__':
    app.run(debug=True)
