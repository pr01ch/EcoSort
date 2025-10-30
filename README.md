# ♻️ EcoSort AI

EcoSort AI is a smart e-waste management web application that helps users report, classify, and responsibly dispose of electronic waste using AI-powered detection and AI-powered EcoSort assistant to guide you with proper ewaste disposal.

---

## 🌟 Features

- 🤖 **AI-Powered Waste Type Detection**
- 📍 **Optional input for location and weight** (for referenced pickup or drop-off points)
- 💬 **Chatbot assistant** for e-waste awareness and disposal guidance
- 🔐 **Email-based Firebase Authentication**

---

## 🧑‍💻 Tech Stack

### Frontend

- Next.js with Typescript
- Tailwind CSS

## Database & Authentication

- Firebase

### Backend

- Python
- FastAPI
- Tensorflow
- AI Model (created on Google Colab)
- Google AI Studio (Gemini API)

---

### Setup instructions

- 1. Clone the repository
- 2. cd folderpath/backend
- python -m venv venv
- venv\Scripts\activate (windows)
- pip install -r requirements.txt
- 3. Create a .env file inside backend/ and add your Gemini API key:
- GEMINI_API_KEY=your_api_key_here

4. Start the backend : uvicorn main:app --reload --port 8000
5. cd folderpath/frontend

- python -m http.server 5600
- open http://localhost:5600

---

## 🚧 Project Status

EcoSort AI is currently under active development.  
I’m continuously improving the AI model, integrating Gemini API for enhanced e-waste classification,  
and refining the chatbot experience.  

![Status](https://img.shields.io/badge/status-in%20progress-yellow)

--

© 2025 Pragya Chauhan
