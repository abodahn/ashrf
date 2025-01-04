from flask import Flask, render_template_string, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Hardcoded credentials for login and update
MAIN_USERNAME = 'admin'
MAIN_PASSWORD = '1234'
UPDATE_PASSWORD = '12'

# Use the external icon URL
icon_url = "https://img.freepik.com/premium-photo/atm-machine-icon-banking-financial-services-symbol-art-logo-illustration_762678-19449.jpg?w=740"

# Path to the Excel file with machine data
excel_path = 'D:\\New Microsoft Excel Worksheet.xlsx'

# Machines with a "down" status to be highlighted in red
down_machines = {'MOJ015', 'MOJ018', 'MOJ021', 'MOJ023', 'MOJ024'}

# Dictionary to store comments for each machine
comments = {}

def load_machine_data():
    # Load the data from the Excel sheet
    sheet_data = pd.read_excel(excel_path)
    # Convert to a list of dictionaries for easy access in Flask
    return sheet_data.to_dict(orient='records')

# HTML template for login page
login_page = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MOJ Project - Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-image: url('https://lh3.googleusercontent.com/p/AF1QipNnpnMYM8ycpiZinR1odECJTt2p6OdLkpBJgVWZ=s1360-w1360-h1020');
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .login-container {
            background-color: rgba(255, 255, 255, 0.8);
            padding: 40px;
            border-radius: 10px;
            text-align: center;
            width: 300px;
        }
        input[type="text"], input[type="password"], button {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: none;
            border-radius: 5px;
        }
        button {
            background-color: #007bff;
            color: white;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>MOJ Project Login</h2>
        <form action="/login" method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        {% if error %}
        <p style="color: red;">{{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
'''

# HTML template for the machines page
machines_page = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MOJ Project - Machines</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding-top: 20px;
        }
        .machines-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
        }
        .machine-button {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 120px;
            padding: 15px;
            border: 1px solid #ccc;
            border-radius: 10px;
            cursor: pointer;
            text-decoration: none;
            color: #000;
            font-size: 1.1em;
            background-color: #e6ffe6; /* Default green for "up" machines */
        }
        .machine-button:hover {
            background-color: #d0f0d0;
        }
        .machine-down {
            background-color: #ff4d4d; /* Red background for down machines */
            color: white;
        }
        .machine-icon {
            width: 50px;
            height: 50px;
            margin-bottom: 5px;
        }
    </style>
</head>
<body>
    <h2>Select a Machine</h2>
    <div class="machines-container">
        {% for machine in machine_data %}
        <a href="{{ url_for('machine_detail', machine_id=machine['Terminal']) }}"
           class="machine-button {% if machine['Terminal'] in down_machines %}machine-down{% endif %}">
            <span>{{ machine['Location'] }}</span>
            <img src="{{ icon_url }}" alt="Machine Icon" class="machine-icon">
            <span>{{ machine['Terminal'] }}</span>
        </a>
        {% endfor %}
    </div>
</body>
</html>
'''

# HTML template for the machine detail page with comments
machine_detail_page = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Machine {{ machine['Terminal'] }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding-top: 30px;
        }
        .card {
            background-color: #f9f9f9;
            border: 1px solid #ccc;
            border-radius: 10px;
            width: 350px;
            padding: 20px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
            text-align: center;
        }
        .card h2 {
            color: #333;
            margin-bottom: 10px;
        }
        .detail-item {
            text-align: left;
            font-size: 1rem;
            color: #555;
            margin: 10px 0;
        }
        .status-form, .comment-form {
            margin-top: 20px;
        }
        .status-form label, .comment-form label {
            font-weight: bold;
            margin-right: 10px;
        }
        .status-form select,
        .status-form input[type="password"],
        .comment-form textarea {
            padding: 8px;
            margin: 5px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
            width: 100%;
        }
        .status-form button, .comment-form button {
            padding: 10px;
            width: 100%;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .status-form button:hover, .comment-form button:hover {
            background-color: #0056b3;
        }
        .back-link {
            margin-top: 15px;
            color: #007bff;
            text-decoration: none;
        }
        .back-link:hover {
            text-decoration: underline;
        }
        .comments-section {
            margin-top: 20px;
            text-align: left;
            width: 100%;
        }
        .comments-section h3 {
            color: #333;
        }
        .comment {
            background-color: #f1f1f1;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="card">
        <h2>Details for {{ machine['Terminal'] }}</h2>
        {% for key, value in machine.items() %}
            {% if key != 'Terminal' %}
                <div class="detail-item"><strong>{{ key }}:</strong> {{ value }}</div>
            {% endif %}
        {% endfor %}
        <form class="status-form" method="POST" action="{{ url_for('update_status', machine_id=machine['Terminal']) }}">
            <label for="status">Change Status:</label>
            <select name="status" id="status">
                <option value="up" {% if machine['Terminal'] not in down_machines %}selected{% endif %}>Up</option>
                <option value="down" {% if machine['Terminal'] in down_machines %}selected{% endif %}>Down</option>
            </select>
            <label for="password">Enter Password:</label>
            <input type="password" id="password" name="password" required>
            <button type="submit">Update Status</button>
        </form>
        <div class="comments-section">
            <h3>Comments:</h3>
            {% for comment in comments %}
            <div class="comment">{{ comment }}</div>
            {% endfor %}
        </div>
        <form class="comment-form" method="POST" action="{{ url_for('add_comment', machine_id=machine['Terminal']) }}">
            <label for="comment">Add Comment:</label>
            <textarea id="comment" name="comment" rows="3" required></textarea>
            <button type="submit">Submit Comment</button>
        </form>
    </div>
    <a href="{{ url_for('machines') }}" class="back-link">Back to Machines</a>
</body>
</html>
'''

@app.route('/')
def login():
    return render_template_string(login_page)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if username == MAIN_USERNAME and password == MAIN_PASSWORD:
        return redirect(url_for('machines'))
    else:
        return render_template_string(login_page, error="Invalid credentials")

@app.route('/machines')
def machines():
    # Load machine data for the machines page
    machine_data = load_machine_data()
    return render_template_string(machines_page, icon_url=icon_url, machine_data=machine_data, down_machines=down_machines)

@app.route('/machine/<machine_id>', methods=['GET'])
def machine_detail(machine_id):
    machine_data = load_machine_data()
    machine = next((m for m in machine_data if m['Terminal'] == machine_id), None)
    if machine:
        machine_comments = comments.get(machine_id, [])
        return render_template_string(
            machine_detail_page,
            machine=machine,
            down_machines=down_machines,
            comments=machine_comments
        )
    else:
        return "Machine not found", 404

@app.route('/machine/<machine_id>/comment', methods=['POST'])
def add_comment(machine_id):
    new_comment = request.form['comment']
    if machine_id not in comments:
        comments[machine_id] = []
    comments[machine_id].append(new_comment)
    return redirect(url_for('machine_detail', machine_id=machine_id))

@app.route('/update_status/<machine_id>', methods=['POST'])
def update_status(machine_id):
    # Check password
    password = request.form['password']
    if password != UPDATE_PASSWORD:
        return "Incorrect password", 403

    # Update the machine status
    status = request.form['status']
    if status == 'down':
        down_machines.add(machine_id)
    else:
        down_machines.discard(machine_id)

    # Redirect back to machine detail page
    return redirect(url_for('machine_detail', machine_id=machine_id))

if __name__ == '__main__':
    app.run(debug=True)
