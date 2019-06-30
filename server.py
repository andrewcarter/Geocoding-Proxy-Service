from connexion import FlaskApp
from flask import redirect


def create_app():
    app = FlaskApp(__name__, specification_dir="./")
    app.add_api("openapi.yaml")
    return app


app = create_app()


@app.route("/")
def home():
    return redirect("http://0.0.0.0:5000/v1/ui/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
