# Admin Guide: Yellow Jacket Archives

## Overview
This guide explains how to use the Django admin interface to manage the Yellow Jacket Archives library system. The admin interface handles three core features:

1. **Book Translations** - Managing multilingual book content (8 languages)
2. **Library Branches** - Managing physical library locations
3. **Inventory Management** - Tracking books at each branch location

---

## Table of Contents
- [Accessing the Admin Interface](#accessing-the-admin-interface)
- [Translation Management](#translation-management)
- [Library Branch Management](#library-branch-management)
- [Inventory Management](#inventory-management)
- [Advanced Tasks](#advanced-tasks)
- [Troubleshooting](#troubleshooting)

---

## Accessing the Admin Interface

### Login Steps
1. Navigate to `http://127.0.0.1:8000/admin/`
2. Enter your admin username and password
3. You'll see the admin dashboard with all manageable models

### Admin Dashboard Overview
The dashboard displays:
- **Movies** - Book catalog management
- **Movie Translations** - Multilingual content for books
- **Reviews** - User book reviews
- **Library Branches** - Physical locations
- **Stock** - Inventory tracking
- **Users** - User account management

---

## Translation Management

### Understanding the Translation System

The Yellow Jacket Archives supports **8 languages**:
- **English** (en) - Default language
- **Spanish** (es)
- **French** (fr)
- **German** (de)
- **Chinese Simplified** (zh-hans)
- **Japanese** (ja)
- **Portuguese** (pt)
- **Hindi** (hi)

Each book can be translated in all these languages. Users see translated content based on their selected language from the website dropdown.

### Method 1: Adding Translations via Movie Admin (Recommended)

This is the quickest way to manage translations for a specific book.

#### Step-by-Step:
1. Go to **Admin Dashboard** → **Movies**
2. Click on the book you want to translate (e.g., "The Great Gatsby")
3. Scroll down to the **"Movie Translations"** section
4. You'll see existing translations (if any) as a table

#### Adding a New Translation
1. Click **"+ Add another Movie Translation"** button
2. A new row appears with these fields:
   - **Language Code**: Select from dropdown (es, fr, de, zh-hans, ja, pt, hi)
   - **Name**: Enter the book title in that language
   - **Author**: Enter the author name in that language
   - **Genre**: Enter the genre in that language
   - **Description**: Enter the book summary in that language

#### Example: Translating "The Great Gatsby" to Spanish
```
Language Code: es
Name: El Gran Gatsby
Author: F. Scott Fitzgerald
Genre: Clásico
Description: La novela cuenta la historia de Jay Gatsby...
```

3. Click **"Save"** to update the book

#### Editing Existing Translations
1. Go to **Movies** → Select a book
2. Find the translation you want to edit in the translations table
3. Edit the fields directly in the inline form
4. Click **"Save"**

### Method 2: Using the Dedicated Translation Admin (Advanced)

For managing translations across multiple books or by language:

1. Go to **Admin Dashboard** → **Movie Translations**
2. You'll see a list of all translations with columns:
   - Movie (Book title)
   - Language Code
   - Name (Translated title)
   - Author (Translated author)
   - Genre (Translated genre)

#### Search & Filter Options:
- **Search**: Find translations by book name, translated title, or author
- **Filter by Language**: View all translations in a specific language
- **Filter by Movie**: View all translations for a specific book

#### Add New Translation
1. Click **"Add Movie Translation"** button (top-right)
2. Select **Movie**: The book to translate
3. Select **Language Code**: Target language
4. Fill in translated fields:
   - **Name** - Book title in target language
   - **Author** - Author name in target language
   - **Genre** - Genre classification in target language
   - **Description** - Book summary in target language
5. Click **"Save"**

### Translation Best Practices

#### 1. **Consistency**
- Use the same terminology across translations
- Example: If you translate "Romance" as "Novela Romántica" in one book, use the same term in all books

#### 2. **Language Quality**
- Use native speakers or professional translators for accuracy
- Avoid machine translation for main content
- Review translated content before publishing

#### 3. **Completeness**
- Ensure all books have translations for each language you support
- Missing translations will fall back to English

#### 4. **Testing**
- After adding/editing translations, visit the website
- Select the language from the dropdown
- Navigate to the book and verify the translations display correctly

#### 5. **Maintenance**
- When adding a new book, immediately create translations for all supported languages
- Update translations if book information changes

### Common Translation Scenarios

#### Scenario 1: Adding a Spanish Translation for a New Book
```
1. Admin → Movies → Create new movie
2. Enter English book details (name, author, genre, description)
3. Click "Save and continue editing"
4. Scroll to Movie Translations
5. Click "+ Add another Movie Translation"
6. Fill in Spanish translation
7. Click "Save"
```

#### Scenario 2: Correcting a Translation Error
```
1. Admin → Movies → Select book
2. Find the translation row with the error
3. Edit the field directly in the inline form
4. Click "Save"
```

#### Scenario 3: Adding All Languages for an Existing Book
```
1. Admin → Movies → Select book
2. For each missing language:
   a. Click "+ Add another Movie Translation"
   b. Select language code
   c. Enter translations
   d. Click "Save"
3. Repeat for all 8 languages
```

---

## Library Branch Management

### Understanding Library Branches

Library branches represent physical library locations where books are available. Each branch has:
- **Name**: Branch identifier (e.g., "Main Library")
- **Address**: Physical location
- **Phone**: Contact number
- **Latitude/Longitude**: GPS coordinates for map display

### Adding a Library Branch

1. Go to **Admin Dashboard** → **Library Branches**
2. Click **"Add Library Branch"** button
3. Fill in the following fields:

#### Branch Details
- **Name** (Required): Branch name
  - Example: "Main Library Downtown"
- **Address** (Required): Physical address
  - Example: "123 Main Street, Atlanta, GA 30303"
- **Phone** (Required): Contact number
  - Example: "+1-404-123-4567"

#### Map Coordinates
- **Latitude** (Required): Latitude coordinate
- **Longitude** (Required): Longitude coordinate

### Finding Coordinates for Your Branch

#### Using Google Maps
1. Open [Google Maps](https://www.google.com/maps)
2. Search for your branch location
3. Right-click on the location pin
4. Click the coordinates at the top to copy them
5. Paste into admin form (format: 33.7756, -84.3970)

#### Using OpenStreetMap
1. Open [OpenStreetMap](https://www.openstreetmap.org)
2. Search for your location
3. Click on the location
4. The URL contains coordinates: `map=18/33.7756/-84.3970`
5. Extract the numbers: 33.7756, -84.3970

#### Common Library Coordinates (Examples)
```
Georgia Tech Library: 33.7756, -84.3970
Atlanta Public Library (Main): 33.7490, -84.3880
Emory University Library: 33.7910, -84.3740
```

#### Step-by-Step Coordinate Example
1. Go to Google Maps
2. Search: "Georgia Tech Library, Atlanta"
3. Right-click the main pin
4. You see: `33.7756° N, 84.3970° W`
5. Format for admin: Latitude: `33.7756`, Longitude: `-84.3970`

### Example: Adding Georgia Tech Library

```
Name: Georgia Tech Library
Address: 704 Cherry Street, Atlanta, GA 30332
Phone: +1-404-894-4500
Latitude: 33.7756
Longitude: -84.3970
```

4. Click **"Save"**

### Editing a Branch

1. Go to **Admin Dashboard** → **Library Branches**
2. Click the branch name to edit
3. Update any fields
4. Click **"Save"**

### Viewing Branch Locations on the Map

After adding branches:
1. Visit any book detail page on the website
2. Scroll down to see the **"Available At"** section
3. You'll see an interactive map showing all branch locations
4. Click on map markers to see branch details and book availability

---

## Inventory Management

### Understanding Stock

Stock tracks how many copies of each book are available at each branch. This determines:
- Which branches appear on the book detail page
- Availability counts shown to users
- Book availability status on the map

### Adding Stock

1. Go to **Admin Dashboard** → **Stock**
2. Click **"Add Stock"** button
3. Fill in:

- **Movie** (Required): Select the book
- **Branch** (Required): Select the library branch
- **Count** (Required): Number of copies available

#### Example: Adding Books to Georgia Tech Library
```
Movie: The Great Gatsby
Branch: Georgia Tech Library
Count: 5

Movie: To Kill a Mockingbird
Branch: Georgia Tech Library
Count: 3

Movie: 1984
Branch: Georgia Tech Library
Count: 2
```

4. Click **"Save"** for each entry

### Editing Stock Quantities

1. Go to **Admin Dashboard** → **Stock**
2. Click the stock entry to edit
3. Update the **Count** field
4. Click **"Save"**

### Bulk Operations

To quickly see which books are at which branches:

1. Go to **Admin Dashboard** → **Stock**
2. Use filters:
   - **Filter by Branch**: View all books at a location
   - **Filter by Movie**: View all branches carrying a book
3. Use search to find specific combinations

### Stock & Map Display Logic

**Important**: Only branches with `count > 0` appear on the map.

- If a book has `count = 0` at all branches → Book doesn't appear on any map
- If a book has `count > 0` at 2 branches → Those 2 branches show on the map
- If you set `count = 0` → That branch disappears from the map for that book

### Example: Managing Book Availability

#### Scenario: "The Great Gatsby" Gets Checked Out
1. Admin → Stock
2. Search: "The Great Gatsby" + "Main Library"
3. Current count: 5
4. Edit and change to: 4
5. Save

#### Scenario: Restocking After Library Event
1. Admin → Stock
2. Filter by Branch: "Main Library"
3. Update multiple books' counts:
   - The Great Gatsby: 3 → 5 (added 2 copies)
   - To Kill a Mockingbird: 1 → 3 (added 2 copies)
   - 1984: 0 → 2 (new copies available)
4. Save each

#### Scenario: Closing a Branch
1. Set all stock counts to 0 for that branch
2. OR delete all stock entries for that branch
3. Books will no longer show that branch on maps

---

## Advanced Tasks

### Task 1: Complete Multilingual Catalog

To ensure all 3 books are translated into all 8 languages:

1. Admin → Movies
2. For each book:
   a. Open the book
   b. Check the Movie Translations section
   c. Count how many language translations exist
   d. For each missing language (8 - current count):
      - Click "+ Add another Movie Translation"
      - Fill in the translation
      - Save

### Task 2: Multi-Branch Setup

Set up inventory across multiple library locations:

1. Admin → Library Branches
2. Add each branch location with coordinates
3. Admin → Stock
4. For each book-branch combination:
   a. Click "Add Stock"
   b. Select book
   c. Select branch
   d. Enter quantity
   e. Save

### Task 3: Updating Book Information

If book details change (new edition, corrected author, etc.):

1. Admin → Movies
2. Click the book
3. Update English fields (name, author, genre, description)
4. Scroll to Movie Translations
5. Update translations in each language
6. Save

### Task 4: Adding a New Book

Complete workflow for adding a new book with all translations:

1. Admin → Movies
2. Click "Add Movie"
3. Enter English details:
   - Name
   - Author
   - Genre
   - Publication Year
   - Description
   - Image (cover)
   - Available (check box)
4. Click "Save and continue editing"
5. Scroll to Movie Translations
6. For each language (7 non-English):
   a. Click "+ Add another Movie Translation"
   b. Select language
   c. Enter translations
   d. Click "Save"
7. Admin → Stock
8. For each library branch:
   a. Click "Add Stock"
   b. Select new movie
   c. Select branch
   d. Enter quantity
   e. Save

---

## Troubleshooting

### Issue: Translation Doesn't Appear on Website

**Symptoms**: You added a translation in admin, but it doesn't show on the website.

**Troubleshooting Steps**:
1. **Verify language code**: Did you select the correct language? (es, fr, de, etc.)
2. **Check the language dropdown**: Are you viewing in that language on the website?
3. **Verify book access**: Can you see the book in English? If not, it doesn't exist yet.
4. **Clear browser cache**: Sometimes browsers cache old content. Do a hard refresh (Ctrl+Shift+R or Cmd+Shift+R)

### Issue: Map Doesn't Show Branches

**Symptoms**: Book detail page has no map or map shows no markers.

**Troubleshooting Steps**:
1. **Check Stock count**: Is `count > 0` for this book at any branch? (If count=0, branch won't appear)
2. **Verify Branch exists**: Admin → Library Branches - Is the branch listed?
3. **Check coordinates**: Are latitude/longitude filled in and valid?
4. **Verify Stock entry**: Admin → Stock - Is there a stock entry for this book-branch combination?

### Issue: Language Dropdown Doesn't Work

**Symptoms**: Selecting a language from dropdown doesn't change content.

**Troubleshooting Steps**:
1. **Verify translations exist**: Admin → Movie Translations - Does that language have translations for the current book?
2. **Check translations are complete**: Are all required fields filled (name, description)?
3. **Clear cache**: Hard refresh the page
4. **Check URL**: The URL should change to include language code (e.g., `/en/...` or `/es/...`)

### Issue: Can't Find a Book in Admin

**Symptoms**: You can't locate a book in the admin interface.

**Solution**:
1. Go to Admin → Movies
2. Use the search box at top-right
3. Search by book name or author
4. OR use filters to narrow down by publication year or genre

### Issue: "Duplicate Entry" Error When Saving Translation

**Symptoms**: Admin shows error like "Movie translation with this Movie and Language code already exists"

**Cause**: You're trying to create a translation for a book-language combination that already exists.

**Solution**:
1. Edit the existing translation instead of creating a new one
2. To find existing: Admin → Movie Translations → Filter by Movie and Language Code

### Issue: Map Coordinates Not Working

**Symptoms**: Map doesn't display correctly or shows wrong location.

**Troubleshooting**:
1. **Verify format**: Coordinates should be decimal numbers, not degrees/minutes/seconds
   - ✅ Correct: `33.7756, -84.3970`
   - ❌ Wrong: `33° 46' 32.16" N, 84° 23' 49.32" W`
2. **Check sign**: Negative numbers are for Western hemisphere and Southern hemisphere
   - Atlanta: `33.7756, -84.3970` (positive lat, negative long)
3. **Test coordinates**: Search the coordinates in Google Maps to verify location

### Issue: Changes Don't Appear Immediately

**Symptoms**: You edited translation/stock/branch but changes don't show on website.

**Solutions**:
1. **Wait a moment**: Django may cache content. Wait 10-30 seconds
2. **Hard refresh**: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows/Linux)
3. **Clear browser cache**: Open browser settings, clear cache and cookies
4. **Check you saved**: Did you click the "Save" button? Unsaved changes won't apply

---

## FAQ

**Q: How many languages do we support?**
A: 8 languages - English, Spanish, French, German, Chinese Simplified, Japanese, Portuguese, and Hindi.

**Q: Can I have the same book at multiple branches?**
A: Yes! Create a Stock entry for each branch. Each entry tracks the count separately.

**Q: What happens if I delete a branch?**
A: All Stock entries for that branch are also deleted. That branch will no longer appear on any book maps.

**Q: Can I edit a book without editing translations?**
A: Yes. Edit the book name/author/genre/description without touching the Movie Translations section.

**Q: What's the maximum number of books I can have?**
A: No hard limit in the system, but performance depends on your server. Practically, unlimited for a small library.

**Q: How do users select languages?**
A: There's a language dropdown on the website. Users select their preferred language, and all content switches to that language.

**Q: Can I have a book with no translations?**
A: Yes, but then only English speakers will see it in their preferred language. Best practice: translate all books into all supported languages.

**Q: What if a translation is incomplete (missing fields)?**
A: The system will use English as a fallback for missing fields.

---

## Summary of Admin Models

| Model | Purpose | Access Method |
|-------|---------|---|
| **Movies** | Add/edit books | Admin → Movies |
| **Movie Translations** | Multilingual content | Admin → Movies (inline) OR Admin → Movie Translations |
| **Library Branches** | Physical locations | Admin → Library Branches |
| **Stock** | Book inventory | Admin → Stock |
| **Reviews** | User reviews (read-only) | Admin → Reviews |

---

## Support

For technical issues, contact the development team.
For translation quality questions, consult language experts.
For map/branch issues, verify coordinates using Google Maps.

---

**Last Updated**: 2024
**Version**: 1.0
