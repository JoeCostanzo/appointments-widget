from flask import Flask, render_template, send_from_directory, request
import json
from sqlalchemy import create_engine
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__, static_url_path='')
cors = CORS(app, resources={r"/add": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

e = create_engine('sqlite:///appointments.db')

def Insert_Appointment(date, time, description):
    date_object = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M%p')
    conn = e.connect()
    query = conn.execute("INSERT INTO Appointments (datetime,description) VALUES (?,?)", (date_object, description))

def Appointments_Meta():
    conn = e.connect()
    query = conn.execute("""SELECT strftime('%m', datetime) || "-"
        || strftime('%d', datetime) || "-" || strftime('%Y', datetime) as Date,
        strftime('%H', datetime) || ":" || strftime('%M', datetime) as Time,
        description as Description FROM Appointments;""")
    return json.dumps([dict(r) for r in query])

def Appointments_Search(string):
    string = '%' + string + '%'
    conn = e.connect()
    query = conn.execute("""SELECT strftime('%m', datetime) || "-"
        || strftime('%d', datetime) || "-" || strftime('%Y', datetime) as Date,
        strftime('%H', datetime) || ":" || strftime('%M', datetime) as Time,
        description as Description FROM Appointments
        WHERE (Description LIKE (?) OR Date LIKE (?) OR Time LIKE (?));""", (string, string, string))
    return json.dumps([dict(r) for r in query])

# Uncomment to re-seed the database

# dummy_data = [
#     {'Date': '2016-05-02', 'Time': '11:00am', 'Description': 'Something'},
#     {'Date': '2016-05-02', 'Time': '12:00pm', 'Description': 'Something else'},
#     {'Date': '2016-05-04', 'Time': '8:00am', 'Description': 'Meet foo'}
# ]
#
# def populate_db_on_init():
#     for event in dummy_data:
#         Insert_Appointment(event['Date'], event['Time'], event['Description'])
#
# populate_db_on_init()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,OPTIONS,DELETE')
    return response

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route("/appointments")
def route():
    search = request.args.get('search')
    if search:
        qryresult = Appointments_Search(search)
    else:
        qryresult = Appointments_Meta()
    return qryresult

@app.route('/add', methods=['POST'])
def handle_data():
    if request and request.form:
        newAppointmentDate = request.form['newAppointmentDate']
        newAppointmentTime = request.form['newAppointmentTime']
        newAppointmentDesc = request.form['newAppointmentDesc']
    else:
        post = json.loads(request.data.decode())
        newAppointmentDate = post['newAppointmentDate']
        newAppointmentTime = post['newAppointmentTime']
        newAppointmentDesc = post['newAppointmentDesc']
    Insert_Appointment(newAppointmentDate, newAppointmentTime, newAppointmentDesc)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
