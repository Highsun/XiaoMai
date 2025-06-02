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

This project is still under development, but if you are interested in our project, you can follow the steps below to run our website in dev-mode.

### Clone

Execute the following command to clone this repository.

```bash
git clone https://github.com/Highsun/XiaoMai.git
```

### Frontend

#### Node.js and npm

The frontend of our project is based on [Node.js](https://nodejs.org/zh-cn), make sure that your computer has installed the lateset version of Node.js.

You can use the following commands on cmd(Windows) or terminal(macOS) to check whether the installation is successful.

```bash
node -v
npm -v
```

The results should be something like this.

```text
v23.7.0
10.9.2
```

#### Vue.js dependency

Execute the following command under the root directory of the project.

```bash
npm install
```

This will automatically install all the dependencies of the project in the `package.json`.

### Backend

We highly recommend that you use [Conda](https://www.anaconda.com/docs/getting-started/miniconda/main) to manage python environment. You can use this tool to isolate a convenient environment to avoid version conflicts.

#### Common

```bash
cd backend
```

#### Windows

##### 1. Create/Activate venv

```bash
python -m venv .venv
.\.venv\Scripts\Activate
```

##### 2. Install dependencies

```bash
pip install -r requirements.txt
```

##### 3. Configure environment variables

```bash
$Env:FLASK_APP = "app.py"
$Env:FLASK_ENV = "development"
```

##### 4. Initialization

```bash
python -m flask db init
python -m flask db migrate -m "init users"
python -m flask db upgrade
```

> Only do THE FIRST LINE (python -m flask db init) for the first time you deploy our project.

#### macOS/Linux

##### 1. Create/Activate venv

```bash
python3 -m venv .venv
source .venv/bin/activate
```

##### 2. Install dependencies

```bash
pip install -r requirements.txt
```

##### 3. Configure environment variables

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
```

##### 4. Initialization

```bash
python3 -m flask db init
python3 -m flask db migrate -m "init users"
python3 -m flask db upgrade
```

> Only do THE FIRST LINE (python -m flask db init) for the first time you deploy our project.

### Run the project

Enter your back-end path and start the virtual environment(if it exists). Then, execute the following command.

```bash
flask run --port 8888 # You may choose other port number you like
```

> **⚠️ Warning**:
> Do not use the port '5000' on macOS since it's the default AirPlay/AirTunes services port of macOS.

Open **another** new terminal/cmd windows and execute the following command.

```bash
npm run dev
```

Visit the prompted URL(Usually http://localhost:5173/) in the browser to preview the project.

### Options

#### SQL access

The back-end uses `SQLite` storage, and the database file is located in `backend/app.db`.

You can use the following command to access to the dataset.

```bash
cd backend
sqlite3 app.db
```

For example, you can access the user table in the following ways.

```bash
.tables
SELECT id, username, email, password_hash, created_at FROM users;
```

The results would be something like this if you've registered some users.

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
