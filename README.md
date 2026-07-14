# TrekFlow - Trekking Management Application (V2)

TrekFlow is a  responsive web application developed by Niharika Soni to manage trekking routes, staff assignments, user bookings, and completed expeditions. It support three users role: **Admins**, **Trek Staff**, and **Trekkers (Users)**.

---

## Table of Contents
1. [Tech Stack](#tech-stack)
2. [Folder Structure Explained](#folder-structure-explained)
3. [Core Workflows & Features](#core-workflows--features)
4. [Asynchronous Backend Jobs (Celery & Redis)](#asynchronous-backend-jobs-celery--redis)
5. [Setup & Running Locally](#setup--running-locally)
6. [Testing & Verification](#testing--verification)

---

## Tech Stack

The application is built using the following technologies:
* **Frontend:** Vue.js  (Single Page Application) with Bootstrap CSS.
* **Backend:** Flask (Python REST API) with SQLite database via SQLAlchemy.
* **Security:** JSON Web Tokens (JWT) for secure authentication.
* **Caching:** Redis for caching frequently accessed treks and status.
* **Background Tasks:** Celery with Redis (as the message broker and result backend).

---

## Folder Structure Explained

```text
trekking_management_system/
├── backend/                  # Flask REST API and Celery Tasks
│   ├── cache/                # Caching setup (Redis wrapper)
│   ├── celery_tasks/         # Asynchronous and scheduled jobs
│   │   ├── celery_app.py     # Celery app initialization and beat scheduler
│   │   ├── daily_reminder.py # Task: Daily upcoming trek notifications
│   │   ├── export_history.py # Task: Export trekker booking history to CSV
│   │   └── monthly_reports.py# Task: Monthly activity reports for Admins
│   ├── controllers/          # Flask API Blueprints (HTTP endpoints)
│   │   ├── admin_controller.py   # Admin operations (routes, staff management)
│   │   ├── authcontrollers.py    # Login, signup, token validation
│   │   ├── public_controller.py  # Public endpoints (dynamic site settings/stats)
│   │   ├── staff_controller.py   # Placeholder for future staff extensions
│   │   └── trek_controller.py    # Trek details, creation, and updates
│   ├── models/               # SQLAlchemy database models
│   │   ├── booking.py        # Booking model (user-to-trek mapping, payments)
│   │   ├── trek.py           # Trek model (dates, slots, difficulty, status)
│   │   ├── trek_staff.py     # Join table for assigned staff-to-trek relationships
│   │   └── user.py           # Unified User model (Admin, Staff, Trekker roles)
│   ├── services/             # Core business logic layer
│   │   ├── admin_services.py # Admin workflow helper functions
│   │   ├── auth_services.py  # Authentication and password hashing helpers
│   │   ├── email_service.py  # SMTP and Google Chat webhook integration
│   │   ├── export_service.py # CSV builder helper
│   │   ├── report_service.py # Monthly report HTML generation logic
│   │   ├── trek_service.py   # Business rules for managing treks
│   │   └── user_service.py   # Profile updating and fetch helpers
│   ├── app.py                # Flask entrypoint & app factory
│   ├── config.py             # App environment variables (database, Redis, SMTP)
│   ├── create_db.py          # Script to create DB tables and seed the Admin user
│   ├── site_settings.json    # JSON storage for editable homepage text
│   └── requirements.txt      # Python dependencies
│
├── frontend/                 # VueJS 3 Frontend SPA
│   ├── src/
│   │   ├── assets/           # Global styles and static assets
│   │   ├── components/       # Shared UI components (Navbar, Sidebar)
│   │   ├── router/           # Vue Router navigation paths
│   │   ├── services/         # API service wrappers (Axios integration)
│   │   ├── store/            # Pinia state management (authentication & global data)
│   │   └── views/            # Main pages / dashboards
│   │       ├── admin/        # Admin dashboards and site settings panels
│   │       ├── auth/         # Login, Register, and Logout pages
│   │       ├── common/       # Profile Editing page
│   │       ├── staff/        # Staff dashboard (Ongoing/Past treks management)
│   │       ├── trekker/      # Trekker dashboard, bookings, history, and browsing
│   │       └── LandingPage.vue # Main landing page
│   ├── package.json          # Node dependencies and scripts
│   └── vite.config.js        # Vite build tool configuration
│
└── instance/                 # SQLite database & CSV Exports directory
    ├── trekking.sqlite3      # Active SQLite Database file
    └── exports/              # Directory where generated CSVs are stored
```

---

## Core Workflows & Features

### 1. Authentication & Security
* Users register as a **Trekker** from the signup page.
* **Admin** and **Staff** cannot self-register; Admin is created programmatically and staff is created by Admin.
* When a user logs in, the backend sends a secure JWT token. The frontend stores this token and includes it in all requests. If the token expires or is invalid, the user is logged out automatically.

### 2. Admin Capabilities
* **Control Panel:** Admins have a dashboard showing total bookings, treks, staff count, and registered users.
* **Trek Management:** Admins create routes (specifying locations, difficulty, dates, prices, and slots) and assign a staff member to lead the trek.
* **Staff Management:** Admins can add new staff members and block/deactivate users.
* **Homepage Editor:** Admins can live-edit the homepage content (About Us, How It Works, Contact Info) and toggle the visibility of statistics.

### 3. Staff Capabilities
* **Assigned Treks:** Staff members see only their assigned treks.
* **Ongoing & Past separation:** Treks are split into *Ongoing* (active/open) and *Past* (completed) views.
* **Manage Treks:** Staff can edit available slots, change status (Open/Closed), and mark a trek as "Completed".
* **Participant Tracking:** When a trek is completed, the staff can still view the historic list of participants who attended.

### 4. Trekker (User) Capabilities
* **Browse & Book:** Trekkers can browse open treks, search/filter by difficulty or location, and book a spot.
* **Prevent Overbooking:** The system automatically prevents booking a trek if slots are full or if the status is closed.
* **My Bookings & History:** Trekkers can view active bookings, cancel a booking, or view a history of their past completed/cancelled treks.
* **Edit Profile:** All roles can edit their personal details (excluding email/password) from their profile page.

---

## Asynchronous Backend Jobs (Celery & Redis)

TrekFlow uses **Celery** with **Redis** to offload heavy operations and schedule automated tasks:

1. **Daily Reminders (Scheduled):**
   * Automatically runs every morning.
   * Finds users who have a trek starting in the next 7 days.
   * Sends them an email with preparation details and a notification to the organization's Google Chat webhook.
2. **Monthly Activity Report (Scheduled):**
   * Runs on the first day of every month.
   * Computes the number of completed treks, number of participants, and the most popular treks in the past month.
   * Generates a clean HTML report and emails it to all Admins.
3. **CSV Export (User-Triggered):**
   * Trekkers can click a button on their dashboard to export their booking history.
   * This queues a background job. The frontend polls the status of the job, and once the CSV is generated on the server, it automatically downloads the file.

---

## Setup & Running Locally

Follow these steps to set up and run the application on your computer.

### Step 1: Start Redis
Make sure Redis is installed and running on its default port:
```bash
# On macOS (using Homebrew)
brew services start redis

# Or run directly in a terminal window
redis-server
```

### Step 2: Set up the Backend
1. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create the database and the default Admin account:
   ```bash
   python3 create_db.py
   ```
   *This creates a default admin with email `admin@trekflow.com` and password `admin123`.*
5. Run the Flask development server:
   ```bash
   python3 app.py
   ```
   *The backend will run on `http://127.0.0.1:5000`.*

### Step 3: Run the Celery Worker & Scheduler
Keep the backend running, open a new terminal window, navigate to the root directory, activate the backend virtual environment, and run:

1. **Start the Celery Worker** (to execute background tasks like CSV exports):
   ```bash
   source backend/.venv/bin/activate
   PYTHONPATH=. ./backend/.venv/bin/celery -A backend.celery_tasks.celery_app.celery worker --loglevel=info
   ```
2. **Start the Celery Beat Scheduler** (optional, to run daily/monthly cron jobs):
   ```bash
   source backend/.venv/bin/activate
   PYTHONPATH=. ./backend/.venv/bin/celery -A backend.celery_tasks.celery_app.celery beat --loglevel=info
   ```

### Step 4: Run the Frontend
1. Open a new terminal window and navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install npm packages:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   *The frontend will run on `http://localhost:5173`. Open this URL in your browser.*

---

## Testing & Verification

### How to test the Caching:
* Access the homepage or browse treks page. The list of open treks will load from the database and cache to Redis. Subsequent loads will fetch the data instantly from Redis.
* Book a trek or modify a trek. The system will automatically clear the cache so the next load gets fresh data.

### How to test the Celery Scheduled Tasks manually:
To verify that the email generator and reminder tasks work without waiting for the scheduled time, run this script from the project root:
```bash
./backend/.venv/bin/python3 -c "
from backend import create_app
from backend.celery_tasks.daily_reminder import send_daily_reminders
from backend.celery_tasks.monthly_reports import send_monthly_report

app = create_app()
with app.app_context():
    print('Daily Reminders Result:', send_daily_reminders())
    print('Monthly Report Result:', send_monthly_report())
"
```
It will query your active database, print the found results, and attempt to send the emails.
