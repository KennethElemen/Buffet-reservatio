from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'sibro'


# Initialize the MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="buffet"
)

# Create a cursor object to interact with the database
cursor = db.cursor()

# Route to update a reservation
@app.route('/update_reservation/<int:id>', methods=['GET', 'POST'])
def update_reservation(id):
    if request.method == 'POST':
        # Get the updated reservation details from the form
        name = request.form['name']
        contact_number = request.form['contact-number']
        date = request.form['date']
        meal_type = request.form['meal-type']
        num_people = request.form['num-people']

        # Update the reservation in the database based on the provided ID
        cursor.execute("UPDATE reservations SET name = %s, contact_number = %s, date = %s, meal_type = %s, num_people = %s WHERE id = %s",
                       (name, contact_number, date, meal_type, num_people, id))
        db.commit()
        flash('Reservation updated successfully', 'success')
        return redirect(url_for('admin'))

    # Fetch the reservation to display in the update form
    cursor.execute("SELECT * FROM reservations WHERE id = %s", (id,))
    reservation = cursor.fetchone()
    
    return render_template('update_reservation.html', id=id, reservation=reservation)



@app.route("/")
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'sibro':
            session['username'] = username
            return redirect(url_for('admin'))
        else:
            flash('Login failed. Please try again.', 'danger')

    return render_template('login.html')


@app.route('/admin')
def admin():
    if 'username' in session:
        # Fetch reservation data from the database
        cursor.execute("SELECT * FROM reservations")
        reservations = cursor.fetchall()
        return render_template("admin.html", reservations=reservations)
    else:
        return redirect(url_for('login'))


@app.route('/delete_reservation/<int:id>')
def delete_reservation(id):
    # Delete the reservation from the database based on the provided ID
    cursor.execute("DELETE FROM reservations WHERE id = %s", (id,))
    db.commit()
    flash('Reservation deleted successfully', 'success')
    return redirect(url_for('admin'))


@app.route("/home")
def home():
    return render_template("home.html")


@app.route('/reserve', methods=['POST', 'GET'])
def reserve():
    if request.method == 'POST':
        # Get reservation details from the form
        name = request.form['name']
        contact_number = request.form['contact-number']
        date = request.form['date']
        meal_type = request.form['meal-type']
        num_people = request.form['num-people']

        # Insert the reservation into the database
        cursor.execute("INSERT INTO reservations (name, contact_number, date, meal_type, num_people) VALUES (%s, %s, %s, %s, %s)",
                       (name, contact_number, date, meal_type, num_people))
        db.commit()

    # Fetch reservation data from the database
    cursor.execute("SELECT * FROM reservations")
    reservations = cursor.fetchall()

    # Render the template and pass the reservations data to it
    return render_template("reserve.html", reservations=reservations)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
