from flask_app import app
from flask_app.controllers import users, recipes

app.secret_key = "Domo Arigato Mister Roboto"

if __name__ == "__main__":
    app.run(debug = True)