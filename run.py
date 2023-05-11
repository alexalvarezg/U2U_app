from app import app

def create_app():
    app = Flask(__name__)

    with app.app_context():
        app.run()

    return app

if __name__ == "__main__":
    create_app()