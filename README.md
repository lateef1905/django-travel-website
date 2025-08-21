# Django Travel Website

A comprehensive travel booking website built with Django, featuring user authentication, destination management, booking system, and search functionality.

## Features

### Phase 1 Implementation
- **User Authentication**: Registration, login, logout with Django's built-in auth system
- **Destination Management**: Browse destinations with detailed information
- **Booking System**: Book trips with customizable travel dates and traveler count
- **Trip Dashboard**: View and manage personal bookings
- **Search Functionality**: Search destinations by name with filtering options
- **Special Offers**: Highlight special destination offers with priority display
- **Admin Interface**: Full Django admin integration for content management

### Key Highlights
- **Responsive Design**: Bootstrap 4 with custom CSS styling
- **Database Integration**: SQLite database with Django ORM
- **Template System**: Reusable templates with template inheritance
- **Static File Management**: Organized CSS, JS, and image assets
- **Form Handling**: Django forms with validation
- **URL Routing**: Clean, organized URL patterns

## Technology Stack

- **Backend**: Django 5.2.5
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 4
- **Libraries**: Font Awesome, OwlCarousel, jQuery
- **Authentication**: Django's built-in authentication system

## Project Structure

```
firstprogram/
├── accounts/                # User authentication app
├── travello/               # Main travel app with destinations and bookings
├── calc/                   # Calculator app (additional feature)
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS, images)
├── assets/                 # Additional static assets
├── media/                  # User uploaded files
├── firstprogram/           # Main Django project settings
└── manage.py              # Django management script
```

## Key Models

### Destination
- Name, description, price
- Image handling
- Special offer flag
- Alphabetical ordering with special offers prioritized

### Booking
- User relationship
- Destination relationship
- Travel date and traveler count
- Booking status tracking
- Timestamp information

## Installation & Setup

1. **Clone the repository**
```bash
git clone [repository-url]
cd firstprogram
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install django
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create superuser**
```bash
python manage.py createsuperuser
```

6. **Start development server**
```bash
python manage.py runserver
```

7. **Access the application**
- Website: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Features in Detail

### Authentication System
- Custom registration form with enhanced fields
- Secure login/logout functionality
- User session management
- Protected views for authenticated users

### Destination Management
- Dynamic destination listing with pagination
- Detailed destination pages
- Image gallery integration
- Price display and special offer highlighting

### Booking System
- Interactive booking forms
- Date selection with validation
- Traveler count specification
- Booking confirmation system
- Personal trip history

### Search & Filtering
- Real-time search functionality
- Name-based filtering
- Results ordering (special offers first, then alphabetical)
- Search result highlighting

### Admin Features
- Full CRUD operations for destinations
- Booking management and monitoring
- User management capabilities
- Content management system

## Styling & UI

- **Color Scheme**: Primary blue theme (#6e8efb)
- **Responsive Design**: Mobile-first approach
- **Interactive Elements**: Hover effects and animations
- **Icon Integration**: Font Awesome icons throughout
- **Typography**: Clean, readable font choices

## Future Enhancements

- Payment gateway integration
- Email notifications
- Advanced filtering options
- User reviews and ratings
- Multiple image uploads per destination
- Booking modification system
- Calendar integration

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is built for educational and portfolio purposes.

## Contact

Developer: Omotoso Abdul-Lateef
Email: abdullateefomotoso43@gmail.com

---

*This project demonstrates Django development skills including MVC architecture, database design, user authentication, form handling, template systems, and responsive web design.*
