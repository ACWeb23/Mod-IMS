import sqlite3
from flask import Flask, render_template_string

# Step 1: Create a SQLite database
def create_database():
    connection = sqlite3.connect("example.db")
    cursor = connection.cursor()

    # Create a table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sample_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            city TEXT NOT NULL
        )
    """)

    # Insert sample data
    cursor.executemany("""
        INSERT INTO sample_data (name, age, city)
        VALUES (?, ?, ?)
    """, [
        ("Alice", 25, "New York"),
        ("Bob", 30, "Los Angeles"),
        ("Charlie", 35, "Chicago")
    ])

    connection.commit()
    connection.close()

# Step 2: Set up Flask app
app = Flask(__name__)

# HTML template to render the data
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Database Viewer</title>
    <style>
        table {
            width: 50%;
            margin: auto;
            border-collapse: collapse;
            text-align: left;
        }
        th, td {
            padding: 8px 12px;
            border: 1px solid #ddd;
        }
        th {
            background-color: #f4f4f4;
        }
    </style>
</head>
<body>
    <h1 style="text-align: center;">Database Contents</h1>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Age</th>
                <th>City</th>
            </tr>
        </thead>
        <tbody>
            {% for row in rows %}
            <tr>
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
                <td>{{ row[3] }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

@app.route("/")
def view_database():
    # Connect to the database
    connection = sqlite3.connect("example.db")
    cursor = connection.cursor()

    # Fetch data from the table
    cursor.execute("SELECT * FROM sample_data")
    rows = cursor.fetchall()
    connection.close()

    # Render the HTML with data
    return render_template_string(HTML_TEMPLATE, rows=rows)

if __name__ == "__main__":
    # Ensure the database and table are created before starting the server
    create_database()
    app.run(debug=True)
