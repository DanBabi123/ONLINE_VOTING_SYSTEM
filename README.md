# 🗳️ Human-Centered Electronic Voting System:
A secure, user-friendly web-based electronic voting system built using Flask, MySQL, and email-based OTP verification. Designed with both user and admin interfaces, this system ensures fair elections with verification and transparency.

This project was created to address the common challenges faced in manual voting systems such as vote duplication, security risks, and lack of accessibility. By leveraging modern web technologies and secure verification techniques, this system aims to enhance the credibility, ease of use, and accessibility of the voting process.

The system ensures that:

Only eligible voters can participate.

Every voter can vote only once.

Transparency is maintained in vote counting and result declaration.

Security is enforced through hashed passwords and OTP-based email verification.

It is ideal for use in educational institutions, small organizations, and clubs where electronic voting is required without deploying complex infrastructure.
---

## 🚀 Features

### 👤 User Functionality

* **Register** with student ID, email, and personal details.
* **Email verification using OTP** before account activation.
* **Secure login** using username, password, and OTP verification.
* **One vote per user** restriction with secure tracking.
* **Live voting interface** showing list of candidates and symbols.
* **Final results display** with winner announcement.

### 🛡️ Admin Functionality

* **Admin login** with secure credentials.
* **Candidate management**:

  * Add candidates with name, party name, symbol, and photo.
  * View all registered candidates.
  * Delete candidates.
* **View voting results** instantly based on live votes.

---

## 💡 Tech Stack

| Layer         | Technology Used                             |
| ------------- | ------------------------------------------- |
| Backend       | Python, Flask                               |
| Database      | MySQL                                       |
| Frontend      | HTML, CSS, Bootstrap                        |
| Auth Security | bcrypt (password hashing), OTP (email)      |
| Email Service | Flask-Mail + Gmail SMTP                     |
| File Storage  | Static file uploads (party symbols, photos) |

---

## 🔐 Authentication Flow

### Registration:

1. User submits registration form.
2. Server validates and checks for duplicates.
3. OTP is sent to the user's email.
4. Upon OTP verification, user is stored in the `users` table.

### Login:

1. User enters username & password.
2. Password is validated using `bcrypt`.
3. OTP is sent to registered email.
4. On OTP confirmation, session is created for the user.

---

## 📄 Database Schema (Simplified)

### `users`

| Column         | Type             |
| -------------- | ---------------- |
| id             | INT, PK          |
| username       | VARCHAR          |
| email          | VARCHAR          |
| password       | VARCHAR (hashed) |
| student\_id    | VARCHAR          |
| phone          | VARCHAR          |
| academic\_year | VARCHAR          |
| department     | VARCHAR          |
| dob            | DATE             |
| gender         | VARCHAR          |

### `candidates`

| Column        | Type               |
| ------------- | ------------------ |
| id            | INT, PK            |
| name          | VARCHAR            |
| party\_name   | VARCHAR            |
| party\_symbol | VARCHAR (filename) |
| photo         | VARCHAR (filename) |
| votes         | INT (default: 0)   |

### `votes`

| Column        | Type               |
| ------------- | ------------------ |
| id            | INT, PK            |
| user\_id      | FK → users.id      |
| candidate\_id | FK → candidates.id |

---

## 📷 Screenshots

| Page                   | Description                             |
| ---------------------- | --------------------------------------- |
| `register.html`        | User registration with personal details |
| `email_verify.html`    | OTP verification during registration    |
| `login.html`           | Login page with username & password     |
| `login_otp.html`       | OTP verification for login              |
| `vote.html`            | Voting interface with candidates        |
| `admin_dashboard.html` | Admin panel for managing candidates     |
| `results.html`         | Display election results and winner     |

---

## ⚙️ Setup Instructions

1. **Clone the repo**:

   ```bash
   git clone https://github.com/yourusername/e-voting-flask.git
   cd e-voting-flask
   ```

2. **Create a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup MySQL Database**:

   * Create a database named `voting_system`.
   * Import schema (create tables `users`, `candidates`, `votes`).
   * Update `app.config['MYSQL_*']` settings in `app.py`.

5. **Set up Gmail SMTP for Flask-Mail**:

   * Enable **less secure apps** or **App Passwords** in Gmail.
   * Replace credentials in:

     ```python
     app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
     app.config['MAIL_PASSWORD'] = 'your_app_password'
     ```

6. **Run the application**:

   ```bash
   flask run
   ```

---

## 📦 Requirements (`requirements.txt`)

```txt
Flask
Flask-MySQLdb
Flask-Mail
Flask-Bcrypt
Werkzeug
```

---

## 📁 Project Structure

```
/e-voting-flask
│
├── static/
│   └── uploads/             # For storing party symbols & photos
│
├── templates/
│   ├── index.html
│   ├── register.html
│   ├── email_verify.html
│   ├── login.html
│   ├── login_otp.html
│   ├── vote.html
│   ├── results.html
│   ├── admin.html
│   └── admin_dashboard.html
│
├── app.py                   # Main Flask application
└── README.md                # Project documentation
```

---

## ✅ Security & Validation

* Passwords are stored **hashed** using `bcrypt`.
* OTPs prevent unauthorized access.
* Email verification ensures identity.
* Users can **vote only once**.
* Admin access is **restricted via hardcoded credentials** (can be enhanced later).

---

## 🚧 Future Improvements

* Use SQLAlchemy ORM for DB interaction.
* Admin credential system using a separate table.
* Better UI with AJAX voting and real-time results.
* Prevent double voting with front-end feedback.
* Admin analytics dashboard (voter turnout, charts).

---
