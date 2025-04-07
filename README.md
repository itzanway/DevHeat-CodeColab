# Collaborative Code Editor

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-Latest-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-0.24%2B-yellowgreen.svg)](https://scikit-learn.org/)

> Transform your coding experience with real-time collaboration! Write, share, and execute Python/C++/Java code together in a powerful, intuitive environment.

## Project Information

This project is part of the **DevHeat event**, organized by the college hackathon group **GDG (Google Developer Group)**.

### Team Members:
- [Shaurya Bisht](https://github.com/ShauryaDusht)
- [Rahul Patel](https://github.com/RAHULPATEL2002)
- [Anway Durge](https://github.com/itzanway)

## Preview
You can view demo from the link: [Video](https://m.youtube.com/watch?v=mJ2Cj7APq-8)


## Key Features
- Real-time collaboration with live editing, cursor tracking, and room-based sessions
- Powerful editor with syntax completion, auto-indentation, and in-browser Python execution
- **Bracket and Quote Completion**: Automatically closes brackets `{}`, `[]`, `()` and quotes `"` and `'` as you type.
- **AI Code Completion**: Integrated with Hugging Face API for AI-powered code suggestions and completions, assisting developers in writing code faster.
- **Room Recommendation Based on Interests**: Using machine learning, rooms are recommended to users based on their stated interests, improving the chances of productive collaborations.
- Secure authentication, private rooms, and sandboxed code execution
- Built-in chat for team discussions

## Quick Start

### Prerequisites
  ```
  - Python 3.9+
  - Docker
  - Docker Compose
  ```

### Clone the Repository

  ```
  git clone https://github.com/ShauryaDusht/CodeTogether.git
  cd CodeTogether
  ```

### Install Dependencies

  1. **Create a Virtual Environment**:
       ```bash
       python3 -m venv venv
       ```
       For Linux:
       ```bash
       source venv/bin/activate  
       ```
       For Windows:
       ```bash
       .\venv\Scripts\activate
       ```
  
  2. **Install Requirements**:
       ```bash
       pip install -r requirements.txt
       pip install python-dotenv requests
       ```
  
### Set Up Environment Variables
  
  Create a `.env` file in the root directory with the following content:
  ```env
  SECRET_KEY=your-secret-key
  DEBUG=True
  ALLOWED_HOSTS=127.0.0.1,localhost
  HUGGINGFACE_API_KEY=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
  ```
  
  ###  Run Migrations
  
  ```bash
  python manage.py migrate
  ```
  
  ### Start the Server
  
  ```bash
  python manage.py runserver
  ```
  
  Open your browser and access the app at `http://127.0.0.1:8000`.
  
---

## Running with Docker Compose

### Set Up Environment Variables

Ensure the `.env` file is present with the following content:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
HUGGINGFACE_API_KEY=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
```

### Use Docker Compose

1. **Build and Run the Application**:
   ```bash
   docker-compose up --build
   ```

2. **Stop the Application**:
   ```bash
   docker-compose down
   ```

Open your browser and access the app at `http://127.0.0.1:8000`.

---

## Technologies Used
### Backend:
- Django & Django Channels for robust server-side operations
- WebSocket implementation for real-time features
- **Hugging Face API** for AI-driven code completion and suggestions

### Frontend:
- Modern Bootstrap and Particle React for responsive design
- Integration for code editing features like bracket/quote completion, syntax highlighting, cursor tracking,and AI-powered code suggestions
- Real-time features enabled with WebSockets

### Database:
- SQLite (default) for easy setup

### Machine Learning:
- **Scikit-learn** (or any other ML library) used for **interest-based room recommendations** to match users based on their project preferences and skills.

###  Development:
- Docker Compose for container orchestration
- Environment-based configuration

---

## Folder Structure

```
collaborative_code_editor/            # Root project directory
│
├── collaborative_code_editor/        # Project configuration
│   ├── __init__.py
│   ├── admin.py
│   ├── asgi.py                       # ASGI configuration (needed for WebSockets)
│   ├── settings.py                   # Project settings
│   ├── urls.py                       # Main URL configuration
│   └── wsgi.py                       # WSGI configuration
│
├── code_editor/                      # Main app
│   ├── migrations/
│   │   └── __init__.py
│   │
│   ├── templates/                    # HTML templates
│   │   ├── code_editor/
│   │   │   ├── home.html
│   │   │   ├── join_room.html
│   │   │   └── room.html
│   │   ├── authentication/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├──  interests.html
│   │   └──  base.html
│   ├── admin.py                     # Admin interface configuration
│   ├── apps.py                      # App configuration
│   ├── consumers.py                 # WebSocket consumers
│   ├── models.py                    # Database models
│   ├── routing.py                   # WebSocket URL routing
│   ├── urls.py                      # HTTP URL routing
│   └── views.py                     # HTTP views
│
├── static/                           # Static files
│   └── code_editor/
│       ├── css/
│       │   ├── auth.css              # Authentication styles
│       │   ├── join_room.css         # Join room page styles
│       │   └── style.css             # Global styles
│       └── js/
│           └── script.js             # Frontend JavaScript
│
├── .gitignore                       # Git ignore file
├── docker-compose.yml               # Docker Compose configuration
├── Dockerfile                       # Docker configuration
├── LICENSE                          # Project license
├── manage.py                        # Django management script
├── README.md                        # Project documentation
├── .env                             # Environment variables file (to be created)
├── vercel.json                      # Vercel configuration file
├── build_files.sh                   # Automates docker build
└── requirements.txt                 # Project dependencies
```
