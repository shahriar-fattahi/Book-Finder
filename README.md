# Book-Finder

**Book Finder** is a RESTful API project designed to make discovering and reviewing books easy. Users can explore a curated list of books, submit their own reviews, and receive personalized reading suggestions based on various genres and interests.

You can find **Detailed Documentation** for this project at the links below:

- [API style](https://github.com/shahriar-fattahi/Book-Finder/blob/main/docs/API_style.md)
- [Authentication system](https://github.com/shahriar-fattahi/Book-Finder/blob/main/docs/authentication_system.md)
- [my ORM in this project](https://github.com/shahriar-fattahi/Book-Finder/blob/main/docs/my_ORM.md)
- [What queries are used for each API endpoint?](https://github.com/shahriar-fattahi/Book-Finder/blob/main/docs/queries_in_urls.md)
- [Recommender system](https://github.com/shahriar-fattahi/Book-Finder/blob/main/docs/recommener_system.md)

## Features

- **Browse Books**: Access an extensive list of books across various genres.
- **Submit Reviews**: Share your thoughts and opinions on the books you've read.
- **Get Book Recommendations**: Receive personalized suggestions for your next read based on your review history and preferences.

## Technologies Used

### 1. ![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white&style=for-the-badge)

### 2. ![Django REST Framework](https://img.shields.io/badge/DRF-ff1709?logo=django&logoColor=white&style=for-the-badge&label=django-rest-framework)

### 3. ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white&style=for-the-badge)

### 4. ![Mypy](https://img.shields.io/badge/Mypy-FFDD00?logo=mypy&logoColor=black&style=for-the-badge)

### 5. ![Pydantic](https://img.shields.io/badge/Pydantic-2CA5E0?logo=pydantic&logoColor=white&style=for-the-badge)

### 6. ![Django-environ](https://img.shields.io/badge/Django--environ-092E20?logo=django&logoColor=white&style=for-the-badge)

### 7. ![DRF-Spectacular](https://img.shields.io/badge/DRF--Spectacular-ff1709?logo=django&logoColor=white&style=for-the-badge)

## Installation

Follow these steps to set up the project on your local machine:

1. Clone the repository:

   ```bash
   git clone https://github.com/shahriar-fattahi/Book-Finder
   cd Book-Finder
   ```

2. Setup a Virtual Environment

- for linux
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- for windows
  ```bash
  python -m venv venv
  venv/scripts/activate
  ```

3. install Dependencies

   ```bash
   pip install -r requirements/local.txt
   ```

4. Create a PostgreSQL database and set the database URL in the .env file

- first, create your .env file
  ```bash
  cp .env.example .env
  ```
- then set DATABASE_URL like this:
  ```
  DATABASE_URL="psql://<user>:<password>@<host>:<port>/<database_name>"
  ```

5. make migrations and migrate
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
6. create an admin
   ```
   python manage.py createsuperuser
   ```
7. run the program
   ```
   python manage.py runserver
   ```
