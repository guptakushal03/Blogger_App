# Blogging WebApp

This project is a Blogging WebApp that allows users to create, view, like, and comment on blogs. The app also provides blog summaries using Gemini and offers personalized recommendations based on users' liked posts. It is built using Flask, SQLAlchemy, and other web technologies.

## Features
- User Authentication (Login/Sign Up)
- Create, Read, Update, Delete (CRUD) Blogs
- Add images to blogs
- Like and Comment on Blogs
- Get personalized blog recommendations based on user likes
- Blog summary feature using Gemini API
- Secure password storage using PBKDF2 hash function

---

## Prerequisites

Before you begin, ensure that you have the following installed:

- Flask==2.3.2
- Flask-SQLAlchemy==3.0.3
- Flask-Login==0.6.2
- werkzeug==2.3.5
- google-generativeai==0.2.2

---

## Installation Steps

### 1. Clone the Repository

Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/guptakushal03/Blogger_App/
cd Blogger_App
```
---

## Running the App

To run the Flask application, use the following command in your terminal:

```bash
flask run
```

Once the server starts, open your browser and go to `http://127.0.0.1:5000` to view the app.

---

## Technologies Used

- **Flask** - Web framework for Python
- **SQLAlchemy** - ORM for database interaction
- **Flask-Login** - User authentication
- **Werkzeug** - Password hashing
- **Gemini API** - Blog summarization
- **HTML, CSS, JavaScript** - Frontend technologies

---

## Contributing

If you'd like to contribute to this project, feel free to fork the repository, make changes, and submit a pull request.

---

## License

This project is open-source and available under the MIT License.
