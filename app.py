from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env if it exists
if os.path.exists(".env"):
    load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for session management

# Access DATABASE_URL from the environmen
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("No DATABASE_URL found. Make sure to set it in your environment.")

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def init_db():
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    message TEXT NOT NULL
                );
            ''')
            conn.commit()
        conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/testimonials")
def testimonials():
    return render_template("testimonials.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        conn = get_db_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute('''
                        INSERT INTO messages (name, email, message)
                        VALUES (%s, %s, %s);
                    ''', (name, email, message))
                    conn.commit()
                    flash("Message sent successfully!", "success")
            except Exception as e:
                conn.rollback()
                print(f"Error inserting message: {e}")
                flash("Could not insert message.", "error")
            finally:
                conn.close()
        else:
            flash("Database connection failed.", "error")
        return redirect(url_for('home'))

    return render_template("contact.html")

# Initialize and run Flask
if __name__ == '__main__':
    app.run(host='http://stat-site.onrender.com', port=8000, debug=True)
