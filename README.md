# South India Tourism

A web application built with Django to help users explore, plan, and personalize their travel experiences across the beautiful states of South India.

## 🌏 Project Overview
This platform provides:
- State and place details (with weather, hotels, and attractions)
- User registration, login, and profile management
- Favorites and bucket list features
- AI-powered travel recommendations (Gemini API)
- Itinerary planning and history
- Reviews, ratings, and travel stats
- Interactive map view

## 🚀 Features
- Browse states and discover top places
- Add places and states to your favorites
- Get personalized recommendations using AI
- Plan and save your own itineraries
- View weather and safety tips for destinations
- Submit travel inquiries
- User profile and travel stats dashboard

## 🛠️ Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd south_india_tourism
   ```
2. **Create a virtual environment:**
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up the PostgreSQL database:**
   - Make sure PostgreSQL is installed and running on your system.
   - Open a terminal and run the following commands to create the database and user:
     ```bash
     psql postgres
     ```
     Then, in the psql prompt:
     ```sql
     CREATE DATABASE south_india_tourism;
     CREATE USER southindiauser WITH PASSWORD '1234';
     GRANT ALL PRIVILEGES ON DATABASE south_india_tourism TO southindiauser;
     \q
     ```
   - These credentials match the default settings in `settings.py`. You can change them as needed.
5. **Set up environment variables:**
   - Create a `.env` file or set the following in your environment:
     - `DJANGO_SECRET_KEY`
     - `GOOGLE_MAPS_API_KEY`
     - `OPENWEATHERMAP_API_KEY`
     - `GEMINI_API_KEY`
6. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
7. **Load initial data (optional):**
   ```bash
   python manage.py loaddata core_data.json
   ```
8. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## 🗂️ Key Files & Directories
- `core/` – Main Django app (views, models, templates, static files)
- `core/templates/core/` – HTML templates
- `core/static/core/` – CSS, JS, images
- `core/views.py` – Main logic for all features
- `requirements.txt` – Python dependencies
- `manage.py` – Django management script

## 💡 Usage
- Visit `http://127.0.0.1:8000/` in your browser
- Sign up or log in to access all features
- Explore states, add favorites, plan itineraries, and get AI recommendations

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## 📬 Contact
- Email: rahulview65@gmail.com
- Instagram: [rahul_nani65](https://instagram.com/rahul_nani65)

---
Enjoy exploring South India! 🇮🇳 
