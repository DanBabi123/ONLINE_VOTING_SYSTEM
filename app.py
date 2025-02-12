from flask import Flask, render_template, request, redirect, session, flash, jsonify, url_for
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.secret_key = os.urandom(24)
bcrypt = Bcrypt(app)

app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'  
app.config['MYSQL_PASSWORD'] = 'bobby123456' 
app.config['MYSQL_DB'] = 'voting_system'  
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        student_id = request.form['student_id']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        phone = request.form['phone']
        academic_year = request.form.get('academic_year')
        department = request.form['department']
        dob = request.form['dob']
        gender = request.form['gender']

        if not all([username, student_id, email, password, confirm_password, phone, academic_year, department, dob, gender]):
            flash('Please fill out all fields!', 'danger')
            return redirect('/register')

        if password != confirm_password:
            flash("Your passwords don't match!", "danger")
            return redirect('/register')

        if len(password) < 6:
            flash('Your password needs to be at least 6 characters long!', 'danger')
            return redirect('/register')

        if len(phone) < 10 or not phone.isdigit():
            flash("That's not a valid phone number!", 'danger')
            return redirect('/register')

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("That username or email is already in use!", "danger")
            cursor.close()
            return redirect("/register")

        password_hash = generate_password_hash(password)
        cursor.execute("""
            INSERT INTO users (username, email, password, student_id, phone, academic_year, department, dob, gender)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (username, email, password_hash, student_id, phone, academic_year, department, dob, gender))
        mysql.connection.commit()
        cursor.close()

        flash("You're registered! You can now log in.", "success")
        return redirect("/login")
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not all([username, password]):
            flash("Both username and password are required", 'danger')
            return redirect('/login')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user['password'], password):  
            session['user_id'] = user['id']  
            session['username'] = user['username']  
            flash('Welcome back! You are logged in.', 'success')
            return redirect('/vote')
        else:
            flash('Incorrect username or password. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/vote', methods=['GET', 'POST']) 
def vote():
    if 'user_id' not in session:
        flash('You need to log in to vote.', 'warning')
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, party_name, party_symbol FROM candidates")  
    candidates = cur.fetchall()
    cur.close()

    if request.method == 'POST':
        candidate_id = request.form.get('candidate')
        user_id = session['user_id']

        if not candidate_id:
            flash('You need to select a candidate.', 'danger')
            return redirect(url_for('vote'))

        cur = mysql.connection.cursor()  
        cur.execute("SELECT * FROM votes WHERE user_id = %s", [user_id])
        vote = cur.fetchone()
        cur.close() 

        if vote:
            flash('You have already cast your vote.', 'danger')
            return redirect(url_for('vote'))

        try:
            cur = mysql.connection.cursor()  
            cur.execute("INSERT INTO votes (user_id, candidate_id) VALUES (%s, %s)", (user_id, candidate_id))
            cur.execute("UPDATE candidates SET votes = votes + 1 WHERE id = %s", [candidate_id])
            mysql.connection.commit()

            flash('Your vote has been submitted successfully! Please logout.', 'success')
            return redirect(url_for('logout'))  
        except Exception as e:
            print(f"Error while submitting vote: {e}")
            flash('There was an issue submitting your vote. Please try again.', 'danger')
        finally:
            cur.close() 

    return render_template('vote.html', candidates=candidates)



@app.route('/results')
def results():
    cur = mysql.connection.cursor()
    cur.execute("SELECT name, party_name, votes FROM candidates ORDER BY votes DESC") 
    results = cur.fetchall()
    cur.close()

    winner = results[0] if results else None  

    return render_template('results.html', results=results, winner=winner)


@app.route('/logout') 
def logout():
    session.clear() 
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))  

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials.', 'danger')

    return render_template('admin.html')

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if request.method == 'POST':
        name = request.form.get('name')
        party_name = request.form.get('party_name')
        party_symbol = request.files.get('party_symbol')
        photo = request.files.get('photo')

        if not all([name, party_name, party_symbol, photo]):
            flash('Please fill out all fields', 'danger')
            return redirect('/admin_dashboard')

        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        party_symbol_filename = os.path.join(app.config['UPLOAD_FOLDER'], party_symbol.filename)
        party_symbol.save(party_symbol_filename)

        photo_filename = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
        photo.save(photo_filename)

        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO candidates (name, party_name, party_symbol, photo) VALUES (%s, %s, %s, %s)",
                (name, party_name, party_symbol.filename, photo.filename)
            )
            mysql.connection.commit()
            flash('Candidate added successfully!', 'success')
        except Exception as e:
            flash(f'Error while adding candidate: {e}', 'danger')
        finally:
            cur.close()

        return redirect('/admin_dashboard')

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM candidates")
        candidates = cur.fetchall()
        cur.close()
    except Exception as e:
        flash(f"Error fetching candidates: {e}", 'danger')
        candidates = []

    return render_template('admin_dashboard.html', candidates=candidates)

@app.route('/delete_candidate/<int:id>', methods=['POST'])
def delete_candidate(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM candidates WHERE id = %s", (id,))
        mysql.connection.commit()
        flash('Candidate deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error while deleting candidate: {e}', 'danger')
    finally:
        cur.close()  

    return redirect('/admin_dashboard')  

if __name__ == '__main__':
    app.run(debug=True)
