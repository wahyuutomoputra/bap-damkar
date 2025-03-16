# Flask API Project

This is a Flask-based API project with SQLAlchemy integration.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

## Running the Application

1. Make sure your virtual environment is activated
2. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## API Endpoints

- GET `/`: Welcome message

## Environment Variables

Create a `.env` file in the root directory with the following variables:
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db
``` 