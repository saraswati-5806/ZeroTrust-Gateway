# IBM Zero Trust Security Gateway

## 🚀 Project Overview

The **IBM Zero Trust Security Gateway** is an enterprise-grade security proxy and access control system developed as a final project for the IBM SkillsBuild Internship. The platform enforces rigorous Zero Trust principles by evaluating real-time access contexts and leveraging artificial intelligence to dynamically analyze, explain, and log security anomalies before granting access to internal micro-applications.

---

## 🛠️ Technology Stack

* **Backend:** Python, Flask, PyJWT (JSON Web Tokens), Werkzeug
* **Data Layer:** Lightweight JSON-based flat-file storage and SQLite support
* **Frontend:** HTML5, CSS3, Vanilla JavaScript, Chart.js, Font Awesome
* **AI & Analytics:** Google Gemini API for automated threat log analysis and risk scoring, alongside Scikit-Learn, Pandas, and NumPy
* **Cloud & Deployment:** Configured for deployment via Gunicorn and container-ready environments

---

## 📁 Project Directory Structure

```text
ZeroTrust-Gateway/
│
├── app.py                      # Root application entry point
├── requirements.txt            # Python package dependencies
├── .env.example                # Environment configuration template
│
├── auth/
│   └── jwt_handler.py          # Helper for JWT encoding/decoding
│
├── middleware/
│   └── interceptor.py          # Dedicated request interceptor logic
│
├── backend/
│   ├── app.py                  # Main Flask application logic & API routes
│   ├── auth.py                 # Authentication blueprint & endpoints
│   ├── middleware.py           # Middleware registration
│   ├── models.py               # Response formatters and data models
│   ├── policy_engine.py        # Zero-trust evaluation and access rules
│   └── database/
│       └── db.py               # Data retrieval and access logging functions
│
├── frontend/
│   ├── index.html              # Main security operations dashboard
│   ├── login.html              # Secure authentication portal
│   └── static/                 # Stylesheets and client-side scripts
│
└── config/
    └── apps_registry.json      # Registered micro-applications configuration

```

---

## ⚙️ Installation & Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/saraswati-5806/ZeroTrust-Gateway.git
cd ZeroTrust-Gateway

```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Configure Environment Variables

Create a `.env` file in the root directory based on `.env.example`:

```env
FLASK_ENV=development
SECRET_KEY=cf414e67cb61ab121497c7e1a0999e8f93040a908af052060ef0b8f6a09aa1e8
JWT_SECRET=cf414e67cb61ab121497c7e1a0999e8f93040a908af052060ef0b8f6a09aa1e8
DATABASE_URL=sqlite:///zero_trust.db
GEMINI_API_KEY=your_google_gemini_api_key_here

```

### 5. Run the Application

```bash
python app.py

```

*The application starts at: `http://localhost:5000*`

---

## 🔐 Demo Credentials

* **Username:** `IBM2026`
* **Password:** `Model`

---

## 🛡️ Core Features & Architecture

* **Zero Trust Policy Engine:** Evaluates five independent security signals prior to authorization:
1. User Role (RBAC)
2. Device Posture & Fingerprinting
3. Time-of-Day Policy
4. Geo-Location Validation
5. AI-Driven Risk Score


* **Identity-Aware Proxy:** Intercepts requests, validates security posture, blocks unauthorized access, and routes approved requests to registered micro-applications (CRM, HR Portal, Finance Dashboard, Inventory Management).
* **AI Risk Analysis:** Evaluates request behaviors dynamically using Google Gemini to output real-time risk scores and threat metrics.
* **Security Operations Dashboard:** Provides real-time tracking of verified users, active alerts, firewall operational status, and access log analytics.

---

## 👥 Team Responsibilities

* **Member 1:** Frontend UI and Dashboard
* **Member 2:** Backend APIs and Authentication
* **Member 3:** Zero Trust Policy Engine and Identity-Aware Proxy
* **Member 4:** AI/ML Risk Detection
* **Member 5:** Cloud and Deployment
* **Member 6:** Documentation and Testing