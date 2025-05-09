# Text Extraction Service

This project provides a text extraction service that processes documents (PDF, DOCX, DOC, Public Url.), extracts the contents, and stores the extracted data into a PostgreSQL database.

## Introduction

The **Text Extraction Service** is a FastAPI-based web application that allows you to upload documents in various formats (PDF, DOCX, DOC, Public Url.), extract their text, and store it in a PostgreSQL database. 

---

## Setup Instructions

Follow these steps to set up the project and get it running on your local machine.

### Step 1: Create a Database

1. **Install PostgreSQL** if it's not already installed on your machine.
2. **Create a new database**. For example:

   ```bash
   CREATE DATABASE text_extraction_db;
   ```

3. Ensure the database user has the necessary permissions to interact with the database.

---

### Step 2: Add Database Credentials in `.env.local` File

Create a `.env.local` file in the root directory of the project and add the following database configuration:

```env
POSTGRES_DB=text_extraction_db
POSTGRES_USERNAME=your_db_username
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_SCHEMA=public
```

Make sure to replace `your_db_username` and `your_db_password` with your actual PostgreSQL database credentials.

---

### Step 3: Set Up Virtual Environment

#### For Linux/MacOS:
1. Create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

#### For Windows:
1. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:

   ```bash
   .\venv\Scripts\activate
   ```

---

### Step 4: Install Requirements

Once your virtual environment is activated, install the required dependencies:

```bash
pip install -r requirements.txt
```

This will install all necessary packages, including FastAPI, SQLAlchemy, PostgreSQL libraries, and other dependencies required for the project.

---


## Running Migrations

To run the database migrations, you will need to use **Alembic**. If Alembic is already configured in your project (which is typically the case in SQLAlchemy projects), you can follow these steps:

1. **Create a migration script** (this will generate a new migration based on your database models):

   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

2. **Run the migration** to apply the changes to the database:

   ```bash
   alembic upgrade head
   ```

   This will update the database schema to match your SQLAlchemy models.


---

## Running the Application

After installing the dependencies and setting up the database, you can run the application.

1. **Start the FastAPI server**:

   ```bash
   uvicorn src.main:backend_app
   ```

2. The application will be available at `http://127.0.0.1:8000`. You can access the API documentation at `http://127.0.0.1:8000/docs`.

---

## Testing the API
To test the API:

1. Open `http://127.0.0.1:8000/docs` in your browser to view the Swagger UI.
2. Use the UI to send requests to the API endpoints.

---

## Sending Payload Example

To extract text from documents or URLs, send a POST request to `/documents/extract` with the following payload:

#### Example Input Payload:

```json
{
  "file_paths_or_urls": [
    "C:\\Users\\user\\Downloads\\2019-04-01 To 2020-03-31.docx",
    "C:\\Users\\user\\Downloads\\content.pdf",
    "C:\\Users\\user\\Downloads\\EdTech_Scope_Document.pdf",
    "C:\\Users\\user\\Downloads\\Fodo AI sheet - Sheet1.pdf",
    "C:\\Users\\user\\Downloads\\Full function.pdf",
    "C:\\Users\\user\\Downloads\\GJAHD15674760000010199_2023.pdf",
    "C:\\Users\\user\\Downloads\\Harshil -NDA.pdf",
    "C:\\Users\\user\\Downloads\\HarshilVagadiyaResume.pdf",
    "https://docs.google.com/document/d/e/2PACX-1vRxYNoXOUhOztXG6HYBWeg0m-71Wjs9iAZtsi83pdmEko14KDi_iROaQdQ0Cb99rE-VXx5gVTglxgYn/pub#h.8ji3d3dtthmj",
    "https://docs.google.com/document/d/e/2PACX-1vRxYNoXOUhOztXG6HYBWeg0m-71Wjs9iAZtsi83pdmEko14KDi_iROaQdQ0Cb99rE-VXx5gVTglxgYn/pub#h.8ji3d3dtthmj",
    "https://docs.google.com/document/d/e/2PACX-1vRxYNoXOUhOztXG6HYBWeg0m-71Wjs9iAZtsi83pdmEko14KDi_iROaQdQ0Cb99rE-VXx5gVTglxgYn/pub#h.8ji3d3dtthmj",
  ]
}
```

In this example, you can upload both local file paths and document URLs. Ensure the URLs are publicly accessible (e.g., Google Docs links).

---

## Additional Configuration

You may need to adjust other configurations such as JWT settings, email settings, or logging in the `.env.local` file.

### Example `.env.local` Configuration:

```env
# Database Configuration
POSTGRES_DB=text_extraction_db
POSTGRES_USERNAME=your_db_username
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_SCHEMA=public

# JWT Configuration
JWT_SECRET_KEY=your_jwt_secret_key
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# SMTP Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@example.com
SMTP_PASSWORD=your_email_password
SMTP_FROM_EMAIL=no-reply@yourdomain.com
SMTP_USE_TLS=true
```