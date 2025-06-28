# 🏔️ South India Tourism

A comprehensive Django web application showcasing the rich culture, heritage, and beauty of South India. Discover destinations, plan trips, explore local cuisine, and connect with fellow travelers.

![South India Tourism](https://img.shields.io/badge/Django-5.2+-green) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-orange) ![Gunicorn](https://img.shields.io/badge/Gunicorn-21.0+-red)

## 🌟 Features

### 🗺️ **Destination Discovery**
- **5 South Indian States**: Kerala, Karnataka, Tamil Nadu, Telangana, Andhra Pradesh
- **Interactive Maps**: Explore destinations with Google Maps integration
- **Detailed Information**: History, culture, climate, and best visiting times
- **Safety Tips**: Cultural and travel safety guidelines

### 🏨 **Accommodation & Dining**
- **Hotel Recommendations**: Curated accommodation options near attractions
- **Local Cuisine**: Authentic South Indian dishes and restaurants
- **Restaurant Guide**: Specialty dishes and average costs
- **Culinary Experiences**: State-wise cuisine showcases

### 👥 **User Experience**
- **User Authentication**: Secure login/signup system
- **Personal Profiles**: Travel preferences and achievements
- **Favorites System**: Save favorite places and states
- **Reviews & Ratings**: Share experiences and read others' reviews
- **Travel Statistics**: Track your travel journey

### 🎯 **Trip Planning**
- **Itinerary Builder**: Day-wise travel plans for each state
- **Transportation Options**: Bus, train, flight, and taxi information
- **Event Calendar**: Local festivals and cultural events
- **Cost Estimation**: Entry fees and transportation costs

### 🤖 **AI-Powered Features**
- **Personalized Recommendations**: AI-driven travel suggestions
- **Route Planning**: Intelligent itinerary optimization
- **Cultural Insights**: AI-generated cultural information
- **Travel Assistance**: Smart travel planning tools

## 🛠️ Technology Stack

### **Backend**
- **Django 5.2+**: Web framework
- **PostgreSQL**: Database
- **Gunicorn**: Production WSGI server
- **WhiteNoise**: Static file serving

### **Frontend**
- **Bootstrap 5**: Responsive UI framework
- **Font Awesome**: Icons
- **AOS (Animate On Scroll)**: Scroll animations
- **Custom CSS**: Enhanced styling

### **APIs & Services**
- **Google Maps API**: Location services
- **Google Generative AI**: AI-powered features
- **OpenWeatherMap API**: Weather information
- **Composio**: AI integration platform

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL 13 or higher
- Git
- Virtual environment (recommended)

## 🚀 Installation

### 1. **Clone the Repository**
```bash
git clone <repository-url>
cd south_india_tourism
```

### 2. **Create Virtual Environment**
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Environment Setup**
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://username:password@localhost:5432/south_india_tourism
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
GEMINI_API_KEY=your-gemini-api-key
OPENWEATHERMAP_API_KEY=your-openweathermap-api-key
```

### 5. **Database Setup**
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. **Create Superuser**
```bash
python manage.py createsuperuser
```

### 7. **Collect Static Files**
```bash
python manage.py collectstatic
```

### 8. **Populate Data (Optional)**
```bash
python manage.py populate_places
python manage.py populate_cuisine_data
```

## 🏃‍♂️ Running the Application

### **Development Mode**
```bash
python manage.py runserver
```
Access the application at: http://127.0.0.1:8000

### **Production Mode**
```bash
gunicorn south_india_tourism.wsgi:application
```
Access the application at: http://127.0.0.1:8000

## 📁 Project Structure

```
south_india_tourism/
├── core/                          # Main Django app
│   ├── models.py                  # Database models
│   ├── views.py                   # View functions
│   ├── urls.py                    # URL routing
│   ├── admin.py                   # Admin interface
│   ├── forms.py                   # Form definitions
│   ├── static/                    # Static files
│   │   ├── css/                   # Stylesheets
│   │   ├── js/                    # JavaScript files
│   │   └── images/                # Images
│   ├── templates/                 # HTML templates
│   │   ├── core/                  # Core templates
│   │   └── registration/          # Auth templates
│   └── management/                # Custom commands
├── south_india_tourism/           # Project settings
│   ├── settings.py                # Django settings
│   ├── urls.py                    # Main URL configuration
│   └── wsgi.py                    # WSGI configuration
├── staticfiles/                   # Collected static files
├── requirements.txt               # Python dependencies
├── Procfile                       # Deployment configuration
├── manage.py                      # Django management script
└── README.md                      # This file
```

## 🗄️ Database Models

### **Core Models**
- **State**: South Indian states with cultural information
- **Place**: Tourist destinations and attractions
- **Hotel**: Accommodation options
- **Cuisine**: Local food specialties
- **Restaurant**: Dining recommendations
- **Event**: Cultural events and festivals
- **Itinerary**: Travel plans and schedules

### **User Models**
- **UserProfile**: Extended user information
- **Review**: User reviews and ratings
- **Favorite**: User's favorite places
- **Contact**: Contact form submissions
- **Inquiry**: Travel inquiries

## 🌐 API Endpoints

### **Authentication**
- `POST /login/` - User login
- `POST /logout/` - User logout
- `POST /signup/` - User registration

### **States & Places**
- `GET /state/<slug>/` - State details
- `GET /place/<id>/` - Place details
- `POST /favorite/add/<id>/` - Add to favorites
- `POST /favorite/remove/<id>/` - Remove from favorites

### **Reviews**
- `POST /review/add/<id>/` - Add review
- `GET /reviews/<id>/` - Get place reviews

### **Contact**
- `POST /contact_submit/` - Submit contact form

## 🚀 Deployment

### **Railway Deployment**
1. Push code to GitHub repository
2. Connect repository to Railway
3. Set environment variables in Railway dashboard
4. Deploy automatically

### **Environment Variables for Production**
```env
DEBUG=False
ALLOWED_HOSTS=southindiatourism.up.railway.app
DATABASE_URL=postgresql://...
SECRET_KEY=your-production-secret-key
```

### **Static Files**
The application uses WhiteNoise for serving static files in production. Static files are automatically collected during deployment.

## 🧪 Testing

### **Run Tests**
```bash
python manage.py test
```

### **Test Coverage**
```bash
coverage run --source='.' manage.py test
coverage report
```

## 📊 Management Commands

### **Data Population**
```bash
# Populate places data
python manage.py populate_places

# Populate cuisine data
python manage.py populate_cuisine_data
```

### **Database Operations**
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database
python manage.py flush
```

## 🔧 Configuration

### **Settings Files**
- `settings.py`: Main Django settings
- `local_settings.py`: Local development settings (optional)
- Environment variables for sensitive data

### **Static Files**
- CSS files in `core/static/core/css/`
- JavaScript files in `core/static/core/js/`
- Images in `core/static/core/images/`

### **Templates**
- Base template: `core/templates/core/base.html`
- State templates: `core/templates/core/states/`
- Authentication templates: `core/templates/registration/`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Django Community**: For the excellent web framework
- **Bootstrap Team**: For the responsive UI framework
- **Font Awesome**: For the beautiful icons
- **Google APIs**: For maps and AI services
- **South Indian Tourism Boards**: For cultural information

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact: [rahulview65@gmail.com]
- Documentation: [link-to-docs]

---

**Made with ❤️ for South India Tourism**

*Discover the magic of Southern India - from serene backwaters to majestic temples, from spicy cuisine to warm hospitality.* 
