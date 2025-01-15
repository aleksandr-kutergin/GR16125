# README.md

## Project Description

This project is a system for processing files containing the word "***". It accepts two types of files: `.txt` and `.csv`. After processing, the information about the file is saved in the database.

The project includes the following functionalities:

1. **File Processing:**
   - For `.txt` files, the word "***" will be searched in the file, which may be large, considering memory limitations.
   - For `.csv` files, the word will be searched in the "Company Name" column. If the word is found in other column, file is not valid
2. **Database:**
   - PostgreSQL is used to store information about the files and comments.
   - Users can upload files info, leave comments, and view their files info.
3. **API Endpoints:**
   - User registration.
   - User login.
   - File upload.
   - Get information about uploaded files.
   - Leave comments.
   - Get comments for a file.

4. **Authorization:**
   - All actions are available only to authorized users.

5. **Technologies:**
   - **Backend:** FastAPI
   - **Database:** PostgreSQL using SQLAlchemy and Alembic for migrations.
   - **Docker:** Support for deployment inside Docker.
   - **AWS:** The application may be deployed on AWS.

---

## Project Structure

1. **app:** Main directory of the project containing:
   - `models.py`: Database models definitions.
   - `schemas.py`: Data validation schemas.
   - `file_processing.py`: File processing logic.
   - `crud.py`: Functions for interacting with the database.
   - `main.py`: Main file with FastAPI settings and endpoint definitions.
   - `auth.py`: User authorization and authentication logic.

2. **app/migrations:** Database migrations folder using Alembic.

3. **tests:** tests

4. **requirements.txt:** A list of dependencies for the project.

5. **README.md:** Documentation for the project (this file).

---

## Setup Instructions

   ```bash
      git clone ...
      cd ...
      touch .env
      docker compose up --build
   ```
 - Make sure, that .env is valid. Should look something like this
 ```
   DB_URI=postgresql://postgres:password@db:5432/file_processing
   SECRET_KEY=my_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=password
   SEARCHED_NAME=***