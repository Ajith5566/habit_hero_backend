Habit Hero Tracker README
Overview
Habit Hero Tracker is a full-stack web application designed to help users create, track, and analyze their daily habits. Built with React for the frontend and Flask with SQLite for the backend, it provides a user-friendly interface to manage habits, mark daily check-ins, and view analytics such as streaks and success rates.

Setup Steps
Backend
Prerequisites:

Python 3.x installed

Virtual environment recommended

Install dependencies:
pip install -r requirements.txt
(Ensure Flask, flask_sqlalchemy, flask_cors, and other requirements are listed.)

Configure the database:

By default, the app uses SQLite with a local file database.db.

Tables will be auto-created on first run (db.create_all()).

Run the backend server:
python app.py
The backend API will run on http://localhost:5000.

Frontend
Prerequisites:

Node.js and npm installed

Install dependencies:
npm install

Run the development server:
npm start
Frontend runs on usually http://localhost:3000 and calls the backend API.

Build for production:
npm run build

Deployment
For production, configure backend environment variables and consider replacing SQLite with a scalable DB like PostgreSQL.

Update the API base URL in frontend API code accordingly.

Deploy backend (e.g., Heroku, Render) and frontend (e.g., Netlify, Vercel) separately or combined.

Feature List
Habit Management:
Create, edit, and delete habits with details like name, frequency (daily/weekly), category, and start date.

Daily Check-ins:
Mark progress by checking in on habits; prevents duplicate check-ins on the same day.

Analytics:
View total habits, total progress, average success rate, best streak, and most common check-in day.

Responsive UI:
Clean, responsive design with React and Tailwind CSS supporting desktop and mobile views.

Backend API:
Flask-based RESTful API with SQLAlchemy managing data persistence.

Data Persistence:
Uses SQLite for lightweight, easy local storage during development.

Modularity:
Separate frontend components (HabitForm, HabitList, Analytics) and backend API routes for clear architecture.