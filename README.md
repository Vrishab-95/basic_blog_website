# 📝 Basic Blog Website

A full-stack blog website built with **Python Flask**, **Flask-SQLAlchemy**, and **Bootstrap**. The application provides user authentication, blog post management, comments, rich-text editing, and an admin-only content management system.

This project was developed to practice building a database-driven web application using Flask, SQLAlchemy, authentication, form handling, and CRUD operations.

---

## 🚀 Features

- 👤 User registration and login
- 🔐 Secure password hashing
- 🚪 User logout functionality
- 📝 Create blog posts
- ✏️ Edit existing blog posts
- 🗑️ Delete blog posts
- 💬 Comment on blog posts
- ✍️ Rich-text blog editor using CKEditor
- 🖼️ Gravatar profile images
- 🛡️ Admin-only blog management
- 🗄️ Database-backed application using SQLAlchemy
- 📱 Bootstrap-based responsive UI
- 🔒 Environment variable support for sensitive configuration
- 🚀 Gunicorn configuration for deployment

---

## 🛠️ Tech Stack

### Backend

- **Python**
- **Flask**
- **Flask-SQLAlchemy**
- **SQLAlchemy**
- **Flask-Login**
- **Flask-WTF**
- **WTForms**
- **Flask-CKEditor**
- **Flask-Gravatar**
- **Werkzeug**

### Frontend

- HTML
- CSS
- Bootstrap 5
- Jinja2 Templates
- CKEditor

### Database

- SQLite — default development database
- PostgreSQL — supported through `psycopg2-binary`

### Deployment

- Gunicorn
- Environment variables using `python-dotenv`

---

## 📂 Project Structure

```text
basic_blog_website/
│
├── static/
│   ├── css/
│   ├── img/
│   └── ...
│
├── templates/
│   ├── index.html
│   ├── post.html
│   ├── login.html
│   ├── register.html
│   ├── make-post.html
│   ├── about.html
│   ├── contact.html
│   └── ...
│
├── forms.py
├── main.py
├── requirements.txt
├── Procfile
├── .gitignore
└── README.md
```

---

## 🧩 Application Architecture

The application follows a simple Flask architecture:

```text
                   ┌─────────────────┐
                   │     Browser     │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │  Flask Routes   │
                   │    main.py      │
                   └────────┬────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        ┌──────────┐  ┌───────────┐  ┌───────────┐
        │  Forms   │  │  Login    │  │ Templates │
        │ forms.py │  │ Management│  │   HTML    │
        └──────────┘  └───────────┘  └───────────┘
              │             │
              └─────────────┼─────────────┐
                            ▼             │
                     ┌─────────────┐      │
                     │ SQLAlchemy  │      │
                     └──────┬──────┘      │
                            ▼             │
                     ┌─────────────┐      │
                     │  Database   │◄─────┘
                     │ SQLite / PG │
                     └─────────────┘
```

---

## 🗄️ Database Design

The application contains three primary database models.

### User

Stores registered users.

```text
User
├── id
├── email
├── password
└── name
```

A user can:

- Create blog posts
- Write comments
- Log in and log out

---

### BlogPost

Stores blog posts.

```text
BlogPost
├── id
├── title
├── subtitle
├── date
├── body
├── img_url
└── author_id
```

Each blog post is associated with an author through a foreign key.

---

### Comments

Stores comments made on blog posts.

```text
Comments
├── id
├── text
├── author_id
└── post_id
```

Comments are associated with both:

- The user who wrote the comment
- The blog post being commented on

---

## 🔐 Authentication

User authentication is handled using **Flask-Login**.

The application supports:

- Registration
- Login
- Logout
- Session management
- Protected functionality

Passwords are not stored as plain text. They are hashed using Werkzeug's password hashing functionality.

```python
generate_password_hash(
    password,
    salt_length=8,
    method='pbkdf2:sha256:600000'
)
```

During login, the stored hash is verified using:

```python
check_password_hash(user.password, password)
```

---

## 👑 Admin System

Blog management operations are restricted to the administrator.

The application uses an `admin_only` decorator to restrict access to users whose database ID is `1`.

Protected operations include:

- Creating posts
- Editing posts
- Deleting posts

Unauthorized users receive a `403 Forbidden` response.

```python
if current_user.id != 1:
    return abort(403)
```

> **Note:** Using a hard-coded user ID for administrator privileges is suitable for a learning project, but a production application should use a proper role/permission system.

---

## 📝 Blog Post Management

Administrators can create blog posts containing:

- Title
- Subtitle
- Image URL
- Rich-text content
- Publication date
- Author

The application uses **CKEditor** to provide a rich-text editing experience.

Blog posts can also be edited and deleted by the administrator.

---

## 💬 Comments

Authenticated users can comment on blog posts.

If an unauthenticated user attempts to comment, they are redirected to the login page.

```text
User
 │
 ├── Login
 │
 ▼
View Blog Post
 │
 ▼
Write Comment
 │
 ▼
Comment stored in database
```

Comments are associated with both the logged-in user and the corresponding blog post.

---

## 🖼️ Gravatar Integration

The application generates Gravatar profile images based on the user's email address.

The email is converted into a SHA-256 hash before being used to construct the Gravatar URL.

This allows users to have automatically generated avatars without storing profile images locally.

---

## 🌐 Available Routes

| Route | Method | Description | Access |
|-------|--------|-------------|--------|
| `/` | GET | Display all blog posts | Public |
| `/register` | GET, POST | Register a new user | Public |
| `/login` | GET, POST | Log in to the application | Public |
| `/logout` | GET | Log out the current user | Logged in |
| `/post/<post_id>` | GET, POST | View a blog post / add comment | Public / Logged in for comments |
| `/new-post` | GET, POST | Create a new blog post | Admin |
| `/edit-post/<post_id>` | GET, POST | Edit a blog post | Admin |
| `/delete/<post_id>` | GET | Delete a blog post | Admin |
| `/about` | GET | About page | Public |
| `/contact` | GET | Contact page | Public |

---

## 📋 Forms

The project uses Flask-WTF and WTForms for form handling and validation.

### CreatePostForm

Used for creating and editing blog posts.

Fields:

- Blog Post Title
- Subtitle
- Blog Image URL
- Blog Content

The image URL is validated using the WTForms `URL` validator.

---

### RegisterForm

Used to register new users.

Fields:

- Email
- Password
- Name

---

### LoginForm

Used for user authentication.

Fields:

- Email
- Password

---

### CommentForm

Used for submitting comments on blog posts.

The comment field uses CKEditor for rich-text input.

---

## ⚙️ Configuration

The application uses environment variables for configuration.

Create a `.env` file in the project root:

```env
FLASK_KEY=your_secret_key
DB_URI=sqlite:///posts.db
```

For PostgreSQL, the database URI can be changed to your PostgreSQL connection string:

```env
DB_URI=postgresql://username:password@host:port/database
```

> Never commit your `.env` file or database credentials to GitHub.

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Vrishab-95/basic_blog_website.git
```

Navigate into the project:

```bash
cd basic_blog_website
```

---

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The project includes dependencies for Flask, SQLAlchemy, authentication, forms, CKEditor, Gravatar, PostgreSQL, Gunicorn, and environment-variable management.

---

### 4. Configure Environment Variables

Create:

```text
.env
```

and add:

```env
FLASK_KEY=your_secret_key
DB_URI=sqlite:///posts.db
```

---

## ▶️ Running the Application

Start the Flask application with:

```bash
python main.py
```

The application will start locally.

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

## 👤 Creating an Admin User

The current application treats the user with database ID `1` as the administrator.

Therefore, when setting up the application for the first time, the first registered user will normally receive ID `1` and will have access to:

- Create posts
- Edit posts
- Delete posts

---

## 🔄 Application Workflow

### New User

```text
Register
   │
   ▼
User Created
   │
   ▼
Automatically Logged In
   │
   ▼
Blog Homepage
```

### Existing User

```text
Login
  │
  ▼
Credentials Verified
  │
  ▼
Flask-Login Session
  │
  ▼
Blog Homepage
```

### Creating a Blog Post

```text
Admin
  │
  ▼
New Post
  │
  ▼
Fill Form
  │
  ▼
Validate Form
  │
  ▼
Save to Database
  │
  ▼
Blog Homepage
```

### Commenting

```text
User
 │
 ▼
Open Blog Post
 │
 ▼
Write Comment
 │
 ▼
Check Authentication
 │
 ├── Not Logged In → Login
 │
 └── Logged In
          │
          ▼
     Save Comment
```

---

## 🔒 Security

The project implements several basic security practices:

- Password hashing using Werkzeug
- Login session management using Flask-Login
- Form handling using Flask-WTF
- Environment variables for application secrets
- Protected admin routes
- Database relationships using SQLAlchemy

For a production deployment, additional security measures should be implemented.

---

## 🚀 Deployment

The application was previously deployed as a live web application using **Render**.

The production deployment used:

- **Render** for application hosting
- **Gunicorn** as the production WSGI server
- **PostgreSQL** for the production database
- Environment variables for application configuration and secrets

The application was successfully deployed and accessible online during the active deployment period.

> **Note:** The live deployment is currently offline because the free PostgreSQL database associated with the deployment expired. The project can still be run locally using SQLite or redeployed with a new production database.

### Production Architecture

```text
                 ┌──────────────────┐
                 │      Browser     │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │     Render       │
                 │   Web Service    │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │     Gunicorn     │
                 │   Flask Server   │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │    PostgreSQL    │
                 │    Database      │
                 └──────────────────┘
```
---

## 📚 Learning Objectives

This project demonstrates practical experience with:

- Python web development
- Flask application structure
- Routing
- Jinja templates
- HTML forms
- WTForms
- Authentication
- Password hashing
- Flask-Login
- SQL databases
- SQLAlchemy ORM
- Database relationships
- CRUD operations
- Foreign keys
- Rich-text editors
- Environment variables
- Web application deployment
- Gunicorn

---

## 🔮 Future Improvements

Some possible improvements for future versions:

- [ ] Replace hard-coded admin ID with a role-based authorization system
- [ ] Add CSRF protection and stronger form validation where needed
- [ ] Add pagination for blog posts
- [ ] Add search functionality
- [ ] Add categories and tags
- [ ] Add user profile pages
- [ ] Allow users to edit/delete their own comments
- [ ] Add post likes/reactions
- [ ] Add image upload instead of image URLs
- [ ] Add password reset functionality
- [ ] Add email verification
- [ ] Add better error pages
- [ ] Add automated tests
- [ ] Improve production security configuration
- [ ] Add a dedicated admin dashboard

---

## 📄 Dependencies

Main dependencies include:

```text
Flask
Flask-Bootstrap
Flask-CKEditor
Flask-Login
Flask-Gravatar
Flask-WTF
WTForms
Flask-SQLAlchemy
SQLAlchemy
Werkzeug
python-dotenv
psycopg2-binary
Gunicorn
```

Exact package versions are specified in `requirements.txt`.

---

## 👨‍💻 Author

**Vrishab Naik**

GitHub: [Vrishab-95](https://github.com/Vrishab-95)

Repository: [basic_blog_website](https://github.com/Vrishab-95/basic_blog_website)

---

## ⭐ Acknowledgements

This project was built as a learning project to practice Python Flask, databases, authentication, and full-stack web development.

If you found this project useful, consider giving the repository a ⭐ on GitHub.

---

## 📜 License

This project does not currently specify a license.
