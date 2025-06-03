# XiaoMai

![Project](https://img.shields.io/badge/project-XiaoMai%20Ticketing%20System-lightblue.svg)
![Framework](https://img.shields.io/badge/framework-Vue.js%20%7C%20Flask-brightgreen.svg)
![Language](https://img.shields.io/badge/language-JavaScript%20%7C%20Python-blue.svg)

![Platform](https://img.shields.io/badge/platform-Web-yellow.svg)
![Status](https://img.shields.io/badge/status-developing-orange.svg)
![Version](https://img.shields.io/badge/version-v0.1.0-blueviolet.svg)

![License](https://img.shields.io/badge/license-MIT-green.svg)

**Electronic Ticketing System**  
Software Engineering Course Assignment, 2022  
University of Electronic Science and Technology of China

---

## Introduction

**XiaoMai** is a lightweight, cross-platform **electronic ticketing application** designed for educational and prototyping purposes. Developed as part of the Software Engineering course at the University of Electronic Science and Technology of China, this system showcases a clean separation of concerns between a modern **Vue.js-based frontend** and a **Flask-powered backend API**.

The application allows users to interact with a mock ticketing platform in real time, simulating key features of a production-level system such as:

- UI-based ticket browsing and selection
- Backend data communication via RESTful APIs
- Modular architecture supporting future feature expansion

The entire stack emphasizes **ease of deployment**, **development clarity**, and **team collaboration**, making XiaoMai an ideal learning foundation for teams exploring full-stack web app development.

> **Built with**: JavaScript (Vue.js) & Python (Flask)
> **Version control**: Git + GitHub for real-world collaboration

## Getting Started

This project is under active development. Follow the steps below to set up and run the project in dev-mode.

### Clone

Clone the repository:

```bash
git clone https://github.com/Highsun/XiaoMai.git
cd XiaoMai
```

### Frontend

#### Node.js and npm

The frontend relies on [Node.js](https://nodejs.org/). Ensure the latest version is installed:

```bash
node -v
npm -v
```

Example output:

```text
v23.7.0
10.9.2
```

#### Install Dependencies

Navigate to the project root and install dependencies:

```bash
npm install
```

### Backend

We recommend using [Conda](https://www.anaconda.com/docs/getting-started/miniconda/main) or Python's built-in venv to manage dependencies.

#### Common Steps

Navigate to backend:

```bash
cd backend
```

#### Virtual Environment

##### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

##### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Configure Environment Variables

##### Windows

```powershell
$Env:FLASK_APP = "app.py"
$Env:FLASK_ENV = "development"
```

##### macOS/Linux

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
```

#### Database Initialization

The project includes a pre-initialized SQLite database (`app.db`) and migrations folder (`migrations`). Running database initialization commands is optional and only necessary if you modify the schema:

If it is your first time initializing database migrations, run:

```bash
flask db init
```

Then, for subsequent schema changes:

##### Windows

```powershell
flask db migrate -m "your migration message"
flask db upgrade
```

##### macOS/Linux

```bash
flask db migrate -m "your migration message"
flask db upgrade
```

### Run the Project

Start the backend (within `backend/`):

```bash
flask run --port 8888
```

> **⚠️ Warning**: Avoid using port `5000` on macOS due to conflicts with AirPlay services.

Start the frontend in a new terminal window (project root):

```bash
npm run dev
```

Visit the URL provided (usually `http://localhost:5173/`) in your browser.

### SQLite Database Access

The SQLite database file is located at `backend/app.db`. To access it:

```bash
cd backend
sqlite3 app.db
```

Example SQL queries:

```sql
.tables
SELECT id, username, email, password_hash, created_at FROM users;
```

Sample output:

```text
SQLite version 3.43.2 2023-10-10 13:08:14
Enter ".help" for usage hints.

1|xiaomai|admin@xiaomai.com|$2b$12$HFq/YalXWJMH3J7.O15w9.oLhorZrkCJgDrAnvQNJpQ1C3o4ouIo6|2025-05-31 06:30:47.568050
```


## Membership links

You can access the repositories of other collaborators in this project through the following link.

- [Maxence](https://github.com/Maxence-29/XiaoMai.git): Backend Dev.
- [Liangyuwei](https://github.com/wowpwowowowowpodjckdjckdjfkdjfkdjf/XiaoMai.git): Document & API management.

## License

This project is licensed under the terms of the [MIT License](LICENSE).
