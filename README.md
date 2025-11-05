# Patient Management System

A simple web application for managing patient records. This project demonstrates a decoupled architecture where a static frontend (HTML/JS) communicates with a dynamic Python backend (FastAPI).

The backend serves patient data from a `patients.json` file, and the frontend fetches and displays this data, allowing for a fully interactive (though simple) web app.

## 🚀 Live Demo

This project is deployed in two separate parts, which is **required** for it to work:

* **Frontend (GitHub Pages):** **[https://Devil-8790.github.io/Patient_management_System/](https://Devil-8790.github.io/Patient_management_System/)**
    * *Note: This link works because the `patient_frontend.html` file was renamed to `index.html`.*

* **Backend (Render):** **`[REPLACE-THIS-WITH-YOUR-OWN-RENDER-URL]`**
    * *The backend API must be deployed separately on a service like Render for the frontend to be able to fetch data.*

---

## 🏛️ Project Architecture

This project is split into two main components:

### 1. Frontend (Client-Side)
* **Files:** `index.html` (or `patient_frontend.html`), CSS, and JavaScript.
* **Technology:** Pure HTML, CSS, and JavaScript (using the `fetch` API).
* **Hosting:** Hosted on **GitHub Pages**, a static site host. It can *only* serve files; it **cannot** run Python code like `main.py`.

### 2. Backend (Server-Side)
* **Files:** `main.py`, `patients.json`, `requirements.txt`.
* **Technology:** **FastAPI** (Python). This is a server that listens for API requests.
* **Hosting:** Must be hosted on a dynamic web service platform like **Render** or Heroku.
* **CORS:** The backend includes `CORSMiddleware` to allow the GitHub Pages frontend to make requests to it from a different domain.

---

## 💻 Tech Stack

* **Backend:** Python, FastAPI, Uvicorn
* **Frontend:** HTML, CSS, JavaScript (Fetch API)
* **Database:** `patients.json` (acting as a simple file-based database)
* **Deployment:**
    * Frontend: GitHub Pages
    * Backend: Render (or similar)

---

## 🛠️ How to Run Locally

To run this project on your own machine, you must run both the backend and frontend.

### 1. Run the Backend (FastAPI)

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Devil-8790/Patient_management_System.git](https://github.com/Devil-8790/Patient_management_System.git)
    cd Patient_management_System
    ```
2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # On Mac/Linux
    python3 -m venv venv
    source venv/bin/activate

    # On Windows
    python -m venv venv
    venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the server:**
    ```bash
    uvicorn main:app --reload
    ```
    Your backend is now running at `http://127.0.0.1:8000`.

### 2. Run the Frontend (Browser)

1.  After the backend is running, simply open the `index.html` (or `patient_frontend.html`) file directly in your web browser.
2.  The JavaScript in the file is configured to make requests to your local server (`http://127.0.0.1:8000`) and will display the patient data.
