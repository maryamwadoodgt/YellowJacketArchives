# Yellow Jacket Archives - GT Library Store

A Django-based digital library system for Georgia Tech students to browse, review, and manage book collections with integrated Google Maps support for locating books across library branches.

## Features

- **Book Catalog**: Browse and search for books by title, author, or genre
- **User Reviews**: Rate and review books with star ratings
- **Shopping Cart**: Add books to cart for checkout
- **Library Branch Locator**: View nearby library branches on interactive map and get directions to where a book is available
- **Multi-Language Support**: View the interface and translate content in 8 languages (English, Spanish, French, German, Chinese, Japanese, Portuguese, Hindi)
- **Admin Dashboard**: Manage books, branches, stock levels, and user reviews
- **User Authentication**: Login system for personalized experiences

## Project Structure

```
YellowJacketArchives/
├── movies/              # Main app for book management
│   ├── models.py       # Book, Review, LibraryBranch, Stock models
│   ├── views.py        # Views including maps API endpoints
│   ├── urls.py         # URL routing
│   ├── admin.py        # Django admin configuration
│   ├── templates/      # HTML templates
│   ├── fixtures/       # Initial data (library branches)
│   └── migrations/     # Database migrations
├── accounts/           # User authentication
├── cart/              # Shopping cart functionality
├── home/              # Homepage and static pages
├── petitions/         # Additional app
├── translations/      # Multi-language translation support
├── moviesstore/       # Django project settings
├── manage.py          # Django management script
├── LIBRARY_MAPS_SETUP.md  # Maps feature integration guide
└── TRANSLATION_SETUP.md   # Multi-language translation guide
```

## Prerequisites

- Python 3.7+
- pip
- Django 5.0+
- SQLite3 (default database)

## Installation

### 1. Clone the Repository
```bash
git clone <repository_url>
cd YellowJacketArchives
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
```bash
python manage.py migrate
```

### 5. Load Initial Data
```bash
python manage.py loaddata movies/fixtures/initial_branches.json
```

### 6. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit `http://localhost:8000/` in your browser.

## Maps & Location Features

The system uses **Leaflet.js with OpenStreetMap** - no API key required!

1. **Load Branch Data**:
   ```bash
   python manage.py loaddata movies/fixtures/initial_branches.json
   ```
2. **Add Stock Data**: Use the admin panel at `/admin/movies/stock/` to add books to branches

See [LIBRARY_MAPS_SETUP.md](LIBRARY_MAPS_SETUP.md) for comprehensive setup instructions and details.

## Multi-Language Support

Browse the application in **8 languages**:
- 🇺🇸 English
- 🇪🇸 Spanish
- 🇫🇷 French
- 🇩🇪 German
- 🇨🇳 Chinese
- 🇯🇵 Japanese
- 🇵🇹 Portuguese
- 🇮🇳 Hindi

**Features:**
- Language selector dropdown in navbar
- Automatic translation API for content
- User language preferences (saved to account)
- Translation caching for performance

1. **Language Selector**: Click the "Language" dropdown in the navbar
2. **Auto-Detection**: Browser language is detected automatically
3. **Translate Content**: Use the translation API to translate reviews and descriptions

See [TRANSLATION_SETUP.md](TRANSLATION_SETUP.md) for comprehensive setup and API documentation.

## Usage

### Access the Application
- **Homepage**: `http://localhost:8000/`
- **Book Catalog**: `http://localhost:8000/movies/`
- **Admin Panel**: `http://localhost:8000/admin/`

### View Book Details with Maps
1. Navigate to a book's detail page: `/movies/<book_id>/`
2. Scroll to the **"Find this book at nearby branches"** section
3. View branches on the interactive map
4. Click "Get directions" to see how to reach a branch

### Manage Data via Admin
- Add/edit books: `/admin/movies/movie/`
- Manage branches: `/admin/movies/librarybranch/`
- Manage stock levels: `/admin/movies/stock/`
- View reviews: `/admin/movies/review/`

## API Endpoints

### Get All Library Branches
```
GET /movies/branches/
```
Returns JSON list of all library branches with coordinates.

### Get Branches with Specific Book
```
GET /movies/<book_id>/branches/
```
Returns branches that have the specified book in stock with availability counts.

### Translate Text
```
POST /translations/translate/
```
Request: `{"text": "string", "source_language": "en", "target_language": "es"}`
Response: `{"success": true, "translated": "...", "cached": false}`

See [LIBRARY_MAPS_SETUP.md](LIBRARY_MAPS_SETUP.md) and [TRANSLATION_SETUP.md](TRANSLATION_SETUP.md) for detailed API documentation.

## Running Tests

Run all tests:
```bash
python manage.py test
```

Run tests for maps integration:
```bash
python manage.py test movies -v 2
```

Run tests for translation feature:
```bash
python manage.py test translations -v 2
```

## Development

### Create New App
```bash
python manage.py startapp <app_name>
```

### Create Database Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### Access Django Shell
```bash
python manage.py shell
```

## Configuration

### Environment Variables
- `GOOGLE_MAPS_API_KEY`: Your Google Maps API key (required for maps feature)
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Whitelist of domains in production

### Settings File
Edit `moviesstore/settings.py` for:
- Database configuration
- Static files and media settings
- Installed apps
- Middleware

## Troubleshooting

### Database Issues
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py loaddata movies/fixtures/initial_branches.json
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### Port Already in Use
```bash
python manage.py runserver 8001
```

For maps and translations-specific issues, see [LIBRARY_MAPS_SETUP.md](LIBRARY_MAPS_SETUP.md#troubleshooting) and [TRANSLATION_SETUP.md](TRANSLATION_SETUP.md#troubleshooting).

## Technologies Used

- **Backend**: Django 5.0
- **Frontend**: HTML5, CSS3, Bootstrap
- **Database**: SQLite3
- **Maps**: Google Maps JavaScript API
- **Authentication**: Django User System

## Future Enhancements

- [ ] Advanced search and filtering
- [ ] Recommendation system based on reviews
- [ ] Email notifications for book availability
- [ ] Mobile app
- [ ] Integration with library management systems
- [ ] Multi-language support
- [ ] Advanced analytics dashboard

## Contributing

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Run tests: `python manage.py test`
4. Commit: `git commit -am 'Add your feature'`
5. Push: `git push origin feature/your-feature-name`
6. Submit a pull request

## License

This project is part of CS 2340 at Georgia Tech.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the [GOOGLE_MAPS_SETUP.md](GOOGLE_MAPS_SETUP.md) for maps-specific help
3. Contact the development team

## Authors

- Yellow Jacket Archives Team
- Georgia Tech CS 2340
