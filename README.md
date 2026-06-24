# SysGuardian

## 📌 Description

SysGuardian is an intelligent system monitoring and administration platform built with FastAPI. It provides real-time information about system resources and allows role-based administration through a REST API and an AI-powered command interface.

The project is designed for small organizations and IT environments where administrators and technicians need quick access to system information and management tools.

---

## 🎯 Objectives

- Monitor system resources in real time.
- Provide secure access using JWT authentication.
- Implement role-based access control.
- Allow user management through an administration interface.
- Provide a simple AI assistant capable of interpreting commands and returning system information.

---

## 🚀 Features

### Authentication
- User registration
- User login
- JWT token authentication
- Current user information

### System Monitoring
- CPU usage
- Memory usage
- Storage information
- Global system summary
- Running processes
- Open ports
- Services information

### User Management
- List users
- Retrieve user by ID
- Change user role
- Disable users

### Administration
- Kill process by PID
- Restricted access based on roles

### AI Assistant
Natural language commands such as:

- "show cpu"
- "show memory"
- "show storage"
- "show summary"
- "show processes"
- "show ports"
- "show services"

---

## 👥 Roles

### Viewer
Accessible routes:

- Authentication
- CPU information
- Memory information
- Storage information
- Summary

### Technician

Viewer permissions +

- Processes
- Ports
- Services

### Administrator

Technician permissions +

- User management
- Change role
- Disable users
- Kill process

---

## 🛠 Technologies

### Backend
- Python 3
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy

### Security
- JWT
- Passlib
- Python-Jose

### System Monitoring
- psutil

### Database
- SQLite

---

## 📁 Project Structure

```text
app/
│
├── main.py
├── database.py
│
├── models/
│     └── user.py
│
├── schemas/
│     ├── user.py
│     └── ia.py
│
├── routers/
│     ├── auth.py
│     ├── system.py
│     ├── users.py
│     └── ai.py
│
├── security/
│     ├── auth.py
│     └── permissions.py
│
├── services/
│     └── system_service.py
│
└── scripts/
      └── seed.py
```

---

## 🔐 Predefined Users

### Administrator

```
Email: admin@sysguardian.com
Password: admin123
```

### Technician

```
Email: tech@sysguardian.com
Password: tech123
```

### Viewer

```
Email: viewer@sysguardian.com
Password: viewer123
```

---

## ⚙ Installation

Clone the repository:

```bash
git clone <repository-url>
cd sysguardian
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn app.main:app --reload
```

API documentation:

```
http://127.0.0.1:8000/docs
```

---

## 🔮 Future Improvements

- React frontend dashboard
- AI integration with LLMs
- System notifications and alerts
- Docker support
- PostgreSQL support
- Logging system
- Export reports
- Performance charts and statistics

---

## 👨‍💻 Author

Final Year Project (PFE)

**SysGuardian – AI-Powered System Monitoring and Administration Platform**