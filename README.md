# ✅ TaskFlow — Full Stack Task Manager

TaskFlow is a full-stack task and project management application built to organize activities, priorities, deadlines, and projects from a modern web interface.

The project started as a simple Python console application and evolved into a full-stack architecture with authentication, REST API, PostgreSQL, React, and Docker.

---

## 🚀 Features

- User registration and login
- JWT authentication
- Password hashing
- User-specific tasks
- Project management
- Task creation and deletion
- Task status management
- Task priorities
- Categories
- Due dates
- Search and filters
- Dashboard statistics
- Overdue task tracking
- Pagination-ready REST API
- PostgreSQL persistence
- Database migrations with Alembic
- Responsive web interface
- Dockerized development environment

---

## 🛠️ Tech Stack

### Frontend

- React
- TypeScript
- Vite
- CSS

### Backend

- Python
- FastAPI
- SQLAlchemy 2
- Pydantic
- JWT Authentication
- Alembic

### Database

- PostgreSQL

### DevOps

- Docker
- Docker Compose
- Nginx
- Git
- GitHub

---

## 🏗️ Architecture

```text
┌─────────────────┐
│ React + TS      │
│ Frontend        │
│ localhost:5173  │
└────────┬────────┘
         │ HTTP / REST
         ▼
┌─────────────────┐
│ FastAPI         │
│ Backend API     │
│ localhost:8000  │
└────────┬────────┘
         │ SQLAlchemy
         ▼
┌─────────────────┐
│ PostgreSQL      │
│ Database        │
└─────────────────┘
```

Authentication is handled using JWT Bearer tokens.

---

## 📁 Project Structure

```text
Gestor/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── autenticacion.py
│   │   │   ├── dashboard.py
│   │   │   ├── proyectos.py
│   │   │   └── tareas.py
│   │   │
│   │   ├── base_datos/
│   │   │   ├── base.py
│   │   │   └── sesion.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── dependencias.py
│   │   │   └── seguridad.py
│   │   │
│   │   ├── modelos/
│   │   │   ├── usuario.py
│   │   │   ├── proyecto.py
│   │   │   └── tarea.py
│   │   │
│   │   ├── esquemas/
│   │   └── main.py
│   │
│   ├── migrations/
│   ├── alembic.ini
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── api.ts
│   │   ├── main.tsx
│   │   ├── styles.css
│   │   └── types.ts
│   │
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── nginx.conf
│   └── Dockerfile
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### Requirements

You need:

- Git
- Docker
- Docker Compose

Clone the repository:

```bash
git clone https://github.com/rodger526/Gestion-de-tareas.git
cd Gestion-de-tareas
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root.

You can use `.env.example` as reference:

```env
DATABASE_URL=postgresql+psycopg://gestor:gestor@db:5432/gestor
SECRET_KEY=your-secret-key
ALGORITMO=HS256
MINUTOS_TOKEN=1440
FRONTEND_ORIGIN=http://localhost:5173
```

Generate a secure secret key with Python:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

> Never commit your real `.env` file or secret keys to GitHub.

---

## 🐳 Run with Docker

Build and start the complete application:

```bash
docker compose up --build
```

Docker will start:

| Service | Address |
|---|---|
| Frontend | `http://localhost:5173` |
| Backend | `http://localhost:8000` |
| Swagger | `http://localhost:8000/docs` |
| PostgreSQL | Port `5432` |

Check containers:

```bash
docker compose ps
```

Stop the application:

```bash
docker compose down
```

---

## 📚 API Documentation

FastAPI automatically generates interactive API documentation.

After starting the application, open:

```text
http://localhost:8000/docs
```

Main API modules:

```text
/auth
/tareas
/proyectos
/dashboard
```

### Authentication

The application provides endpoints for:

- User registration
- Login
- Current user information
- JWT protected endpoints

### Tasks

Users can:

- Create tasks
- List their tasks
- Search tasks
- Filter tasks
- Change task status
- Delete tasks
- Assign priorities
- Set due dates
- Assign tasks to projects

### Projects

Users can create and manage projects and associate tasks with them.

### Dashboard

The dashboard provides statistics for:

- Total tasks
- Pending tasks
- Tasks in progress
- Completed tasks
- Overdue tasks

---

## 🗄️ Database

TaskFlow uses PostgreSQL with SQLAlchemy ORM.

Database schema changes are managed using Alembic migrations.

Main tables:

```text
usuarios
proyectos
tareas
alembic_version
```

You can access PostgreSQL inside Docker with:

```bash
docker exec -it gestor_postgres psql -U gestor -d gestor
```

Then:

```sql
\dt

SELECT id, nombre, email
FROM usuarios;

SELECT id, titulo, estado, prioridad
FROM tareas;
```

Exit PostgreSQL:

```sql
\q
```

---

## 🔒 Security

TaskFlow includes:

- Password hashing
- JWT authentication
- Protected API routes
- User-specific resources
- Environment-based secrets
- Input validation with Pydantic

Sensitive environment variables are excluded from Git through `.gitignore`.

---

## 🧭 Project Evolution

This repository also represents the evolution of the application.

```text
V1
Python console CRUD
        ↓
V2
Modular architecture + SQLite
        ↓
V3
Priorities, states, categories,
deadlines, search and filters
        ↓
V4
FastAPI REST API
        ↓
Current
React + TypeScript
FastAPI
JWT Authentication
PostgreSQL
SQLAlchemy
Alembic
Docker
Nginx
```

This evolution demonstrates the process of refactoring a basic application into a modern full-stack system.

---

## 🔮 Future Improvements

Planned improvements include:

- Task editing from the web interface
- Advanced project management
- Subtasks
- Tags
- Comments
- Improved pagination UI
- Automated testing
- GitHub Actions CI/CD
- Production deployment
- Enhanced responsive design

---

## 👨‍💻 Author

**Rodger M. Muñoz Molina**

Information Technology Engineering Student  
Backend & Full Stack Development

GitHub: [@rodger526](https://github.com/rodger526)

LinkedIn: [Rodger Muñoz](https://www.linkedin.com/in/rodger-muñoz-652542319)

---

## 📄 License

This project is intended for educational and portfolio purposes.