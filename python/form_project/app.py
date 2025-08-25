from flask import Flask, request, render_template_string
from pymongo import MongoClient

app = Flask(__name__)  # ✅ fixed

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["client_database"]   # database name
collection = db["clients"]       # collection name

# HTML template
form_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Client Login</title>
</head>
<body>
    <h2>Client Login Form</h2>
    <form method="POST" action="/">
        <label for="name">Name:</label><br>
        <input type="text" id="name" name="name" required><br><br>

        <label for="email">Email:</label><br>
        <input type="email" id="email" name="email" required><br><br>

        <input type="submit" value="Submit">
        <input type="reset" value="Reset">
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name").strip()
        email = request.form.get("email").strip().lower()

        # Check if client already exists (by email or name)
        existing_client = collection.find_one({
            "$or": [{"email": email}, {"name": name}]
        })

        if existing_client:
            return f"""
                <h3>Client with name '{name}' or email '{email}' already exists.</h3>
                <a href="/"><button>Try Again</button></a>
            """

        # Insert new client
        collection.insert_one({"name": name, "email": email})

        return f"""
            <h3>Thank you, {name}. Your information has been saved.</h3>
            <a href="/"><button>Add Another Client</button></a>
        """

    return render_template_string(form_template)

# ✅ fixed
if __name__ == "__main__":
    app.run(debug=True)
