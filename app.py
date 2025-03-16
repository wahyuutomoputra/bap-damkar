from app import create_app
from app.utils.response_handler import success_response

app = create_app()

@app.route('/')
def index():
    return success_response(
        message="Welcome to Flask API",
        data={
            "version": "1.0.0",
            "documentation": "/docs"  # if you have API documentation
        }
    )

if __name__ == '__main__':
    app.run(debug=True) 