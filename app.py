
from flask import Flask, request, redirect, url_for

app = Flask(__name__)


employees = [
    {"id": 1, "name": "Arun Kumar", "role": "Developer"},
    {"id": 2, "name": "Priya Sharma", "role": "Tester"}
]

next_id = 3
app.employees = employees


@app.route("/", methods=["GET"])
def home():
    rows = ""

    for employee in employees:
        rows += (
            f"<tr><td>{employee['id']}</td>"
            f"<td>{employee['name']}</td>"
            f"<td>{employee['role']}</td>"
            f"<td><a href='/delete/{employee['id']}'>Delete</a></td></tr>"
        )

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Employee Management</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: Arial; margin: 40px; background: #f4f6f8; }}
            main {{ max-width: 850px; margin: auto; background: white;
                    padding: 24px; border-radius: 10px; }}
            input, button {{ padding: 10px; margin: 5px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
            th {{ background: #e9eef5; }}
        </style>
    </head>
    <body>
    <main>
        <h1>Employee Management System</h1>
        <p>Version 3 — Add, Delete and View Employees</p>
        <h2>Add Employee</h2>
        <form action="/add" method="post">
            <input name="name" placeholder="Employee name" required>
            <input name="role" placeholder="Job role" required>
            <button type="submit">Add Employee</button>
        </form>
        <h2>Employee List</h2>
        <table>
            <tr><th>ID</th><th>Name</th><th>Role</th><th>Action</th></tr>
            {rows}
        </table>
    </main>
    </body>
    </html>
    """


@app.route("/add", methods=["POST"])
def add_employee():
    global next_id

    name = request.form.get("name", "").strip()
    role = request.form.get("role", "").strip()

    if name and role:
        employees.append({
            "id": next_id,
            "name": name,
            "role": role
        })
        next_id += 1

    return redirect(url_for("home"))


@app.route("/delete/<int:employee_id>", methods=["GET"])
def delete_employee(employee_id):
    employees[:] = [
        employee for employee in employees
        if employee["id"] != employee_id
    ]
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
