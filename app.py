from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ice_cream123",
    database="blood_donor"
)

cursor = db.cursor()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/add_donor', methods=['POST'])
def add_donor():
    name = request.form['name']
    age = request.form['age']
    blood_group = request.form['blood_group']
    phone = request.form['phone']
    city = request.form['city']

    query = """
    INSERT INTO donors
    (name, age, blood_group, phone, city)
    VALUES (%s,%s,%s,%s,%s)
    """

    values = (name, age, blood_group, phone, city)

    cursor.execute(query, values)
    db.commit()

    return render_template("register_success.html")

@app.route('/search')
def search():
    
    return render_template('search.html')

@app.route('/find', methods=['POST'])
def find():

    blood_group = request.form['blood_group']

    cursor.execute(
        """
        SELECT * FROM donors
        WHERE blood_group=%s
        """,
        (blood_group,)
    )

    donors = cursor.fetchall()

    return render_template(
        'results.html',
        donors=donors
    )

@app.route('/request_blood')
def request_blood():
    return render_template('request_blood.html')


@app.route('/submit_request', methods=['POST'])
def submit_request():

    patient_name = request.form['patient_name']
    blood_group = request.form['blood_group']
    city = request.form['city']
    hospital = request.form['hospital']
    contact = request.form['contact']

    query = """
    INSERT INTO blood_requests
    (patient_name,blood_group,city,hospital,contact)
    VALUES (%s,%s,%s,%s,%s)
    """

    cursor.execute(
        query,
        (patient_name,blood_group,city,hospital,contact)
    )

    db.commit()

    return render_template("request_success.html")

@app.route('/dashboard')
def dashboard():

    cursor.execute(
        "SELECT COUNT(*) FROM donors"
    )
    total_donors = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM blood_requests"
    )
    total_requests = cursor.fetchone()[0]

    return render_template(
        'dashboard.html',
        total_donors=total_donors,
        total_requests=total_requests
    )

if __name__ == '__main__':
    app.run(debug=True)