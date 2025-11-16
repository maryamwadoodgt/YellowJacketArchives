# Library Branch Maps Setup Guide

This guide explains how the GT Library Store uses maps to help users view nearby library branches and find where books are available.

## Overview

The GT Library Store includes an interactive map feature that allows users to:
- View nearby library branches on an interactive map
- See which branches have a specific book in stock
- View branch details and availability
- Link directly to branch locations on OpenStreetMap

## Key Features

✅ **No API Key Required** - Uses open-source Leaflet.js with OpenStreetMap  
✅ **Free & Open Source** - No costs or restrictions  
✅ **Fast Loading** - Lightweight and efficient  
✅ **Mobile Friendly** - Works on all devices  
✅ **Easy Setup** - Works out of the box!

## How It Works

The system uses:
- **Leaflet.js** - Open-source mapping library
- **OpenStreetMap** - Free map tiles
- **CDN Hosting** - No server-side map processing needed

## Quick Start

### 1. No Setup Required!

Unlike the Google Maps version, this implementation requires **no API keys** and **no configuration**. It works immediately!

### 2. Load Initial Branch Data

Create library branches via Django admin or load the fixture:

```bash
python manage.py loaddata movies/fixtures/initial_branches.json
```

This creates two Georgia Tech library branches:
- Georgia Tech Library - Crosland Tower (33.7756, -84.3970)
- Clough Undergraduate Learning Commons (33.7750, -84.3980)

### 3. Add Stock Data

Associate books with branches and specify quantities:

#### Via Django Admin:
1. Go to `/admin/movies/stock/`
2. Click "Add Stock"
3. Select a Movie (book), Branch, and quantity
4. Save

#### Programmatically:
```python
from movies.models import Movie, LibraryBranch, Stock

book = Movie.objects.get(id=1)
branch = LibraryBranch.objects.get(id=1)
Stock.objects.update_or_create(
    movie=book,
    branch=branch,
    defaults={'count': 5}
)
```

### 4. Start the Server

```bash
python manage.py runserver
```

Visit a book detail page (e.g., `/movies/1/`) to see the interactive map!

## Features in Detail

### Interactive Map
- Displays all branches with a specific book in stock
- Centered on Georgia Tech by default
- Clickable markers showing branch information
- Popup displays: branch name, address, phone, and copy count

### Branch List
- Shows all branches with availability counts
- Color-coded badges for copy counts
- "View on Map" button links to OpenStreetMap

### Responsive Design
- Works on desktop, tablet, and mobile
- Touch-friendly controls
- Fast rendering

## API Endpoints

### Get All Branches
**Endpoint:** `GET /movies/branches/`

**Response:**
```json
{
  "branches": [
    {
      "id": 1,
      "name": "Georgia Tech Library - Crosland Tower",
      "address": "901 Cherry St NW, Atlanta, GA 30332",
      "latitude": 33.7756,
      "longitude": -84.3970,
      "phone": "(404) 894-0000"
    }
  ]
}
```

### Get Branches with Specific Book
**Endpoint:** `GET /movies/<book_id>/branches/`

**Response:**
```json
{
  "movie_id": 1,
  "movie_name": "Sample Book Title",
  "branches": [
    {
      "branch_id": 1,
      "branch_name": "Georgia Tech Library - Crosland Tower",
      "address": "901 Cherry St NW, Atlanta, GA 30332",
      "latitude": 33.7756,
      "longitude": -84.3970,
      "phone": "(404) 894-0000",
      "count": 3
    }
  ]
}
```

## Troubleshooting

### Map Not Showing
1. Check browser console (F12) for errors
2. Verify branches exist in database: 
   ```bash
   python manage.py shell
   >>> from movies.models import LibraryBranch
   >>> LibraryBranch.objects.count()
   ```
3. Ensure branches have latitude/longitude values

### No Branches Appearing
1. Load the fixture:
   ```bash
   python manage.py loaddata movies/fixtures/initial_branches.json
   ```
2. Add stock entries for books:
   ```bash
   python manage.py shell
   >>> from movies.models import Stock, Movie, LibraryBranch
   >>> Stock.objects.create(movie=Movie.objects.first(), branch=LibraryBranch.objects.first(), count=5)
   ```

### Map Takes Time to Load
- First load may be slow while Leaflet/Tiles download
- Subsequent visits load from browser cache
- Consider using a local tile server for production

## Technologies Used

- **Leaflet.js** - Lightweight mapping library
- **OpenStreetMap** - Free map tiles
- **CDN** - Fast content delivery
- **JavaScript Fetch API** - Modern data loading

## Adding More Branches

### Via Admin Interface
1. Go to `/admin/movies/librarybranch/`
2. Click "Add Library Branch"
3. Fill in:
   - Name
   - Address
   - Latitude & Longitude
   - Phone
4. Save

### Via Django Shell
```python
from movies.models import LibraryBranch

branch = LibraryBranch.objects.create(
    name="Your Branch Name",
    address="Your Address",
    latitude=33.7756,
    longitude=-84.3970,
    phone="(404) 555-1234"
)
```

To find latitude/longitude, use [OpenStreetMap](https://www.openstreetmap.org/) - right-click any location to see coordinates.

## Performance

Leaflet is highly optimized:
- ~40KB gzipped (vs. ~200KB for Google Maps)
- Fast rendering even with 100+ branches
- Minimal server resources needed
- Works offline with cached tiles

## Production Deployment

For production, consider:

1. **Self-hosted Tiles** (optional)
   - Use a tile server like Mapbox or Stamen
   - More control and customization
   - Reduce dependency on external CDNs

2. **Caching**
   - Cache branch data in Redis
   - Reduce database queries

3. **HTTPS**
   - Required for all HTTPS sites
   - Automatic with Leaflet

## Comparison: Leaflet vs Google Maps

| Feature | Leaflet | Google Maps |
|---------|---------|-------------|
| API Key Required | ❌ No | ✅ Yes |
| Cost | Free | Free (with limits) |
| Library Size | 40KB | 200KB+ |
| Setup Time | Instant | 15-30 min |
| Directions | Manual links | Built-in |
| Customization | High | Limited |
| Best For | Open projects | Feature-rich apps |

## Additional Resources

- [Leaflet Documentation](https://leafletjs.com/reference.html)
- [OpenStreetMap](https://www.openstreetmap.org/)
- [OpenStreetMap Contributing](https://www.openstreetmap.org/welcome)

## Support

For issues:
1. Check the troubleshooting section
2. Review browser console for errors
3. Verify database has branches and stock entries
4. Check that coordinates are valid (latitude: -90 to 90, longitude: -180 to 180)

