# Amazon Product Search Automation

**City of Los Angeles General Services Department - Evaluation Program**
**Author:** George Lin

A Python-based web automation tool that searches Amazon products and extracts pricing information using Playwright. Includes a web interface with Bootstrap UI for easy remote access.

---

## Features

### Core Requirements (Required)
- ✅ **Automated Browser Control**: Uses Playwright to control Chromium browser
- ✅ **Product Search**: Searches Amazon for specified products
- ✅ **Data Extraction**: Extracts product name and price from search results
- ✅ **Error Handling**: Robust error handling for timeouts and missing elements
- ✅ **Clear Output**: Console output with success/error messages

### Bonus Challenge (Web Accessibility)
- ✅ **Web API**: Flask-based REST API for remote automation
- ✅ **Web UI**: Bootstrap-styled interface with real-time logs
- ✅ **Rate Limiting**: Prevents spam and website blocking (30 seconds between requests)
- ✅ **Progress Indicators**: Visual feedback during automation
- ✅ **Production Ready**: Configured for Render deployment

---

## Project Structure

```
python_playwright/
├── script.py              # Core automation script
├── script_test.py         # Pytest test suite
├── app.py                 # Flask web application
├── templates/
│   └── index.html         # HTML template (clean, minimal)
├── static/
│   ├── css/
│   │   └── style.css      # Custom styles
│   └── js/
│       └── app.js         # Client-side JavaScript
├── requirements.txt       # Python dependencies
├── Procfile              # Render deployment config
├── README.md             # This file
└── .gitignore            # Git ignore rules
```

### Directory Organization

**For Production Deployment:**
- `templates/` - Flask HTML templates (Jinja2)
- `static/` - Static assets (CSS, JS, images)
  - `static/css/` - Stylesheets
  - `static/js/` - JavaScript files
- `Procfile` - Tells Render how to start the app

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd python_playwright
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv

   # Activate on macOS/Linux:
   source venv/bin/activate

   # Activate on Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install chromium
   ```

---

## Usage

### Option 1: Command Line Script

Run the core automation script directly:

```bash
python script.py
```

**Output:**
```
Loading Amazon homepage...
Amazon homepage loaded successfully
Clicked 'Continue shopping' button
Successfully Found Product: Nintendo Switch 2 OLED Model...
Price: $499.00
```

### Option 2: Run Tests

Execute the test suite:

```bash
pytest script_test.py -v
```

### Option 3: Web Interface (Recommended)

Start the Flask web server:

```bash
python app.py
```

**Access the application:**
- **Web UI**: http://localhost:5000
- **API Endpoint**: http://localhost:5000/api/search
- **Health Check**: http://localhost:5000/api/health

#### Using the Web UI
1. Open http://localhost:5000 in your browser
2. Enter a **specific** product name (e.g., "Nintendo Switch 2 OLED", "iPhone 15 Pro Max")
   - ⚠️ **Important:** Use specific product names, not generic categories (e.g., "iPhone 15 Pro" instead of just "phones")
3. Choose headless mode (recommended)
4. Click "Start Search"
5. View real-time logs and results

#### Using the API
```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "search_term": "Nintendo Switch 2",
    "headless": true
  }'
```

**Response:**
```json
{
  "success": true,
  "product_name": "Nintendo Switch 2 OLED Model...",
  "price": "$499.00",
  "error": null,
  "logs": [
    "[10:30:15] Starting search for: Nintendo Switch 2",
    "[10:30:16] Initializing browser...",
    "[10:30:18] Navigating to Amazon.com...",
    "[10:30:20] Amazon homepage loaded",
    "[10:30:21] Checking for popups...",
    "[10:30:22] Searching for: Nintendo Switch 2",
    "[10:30:24] Extracting product information...",
    "[10:30:25] Success! Found: Nintendo Switch 2 OLED Model...",
    "[10:30:25] Price: $499.00",
    "[10:30:26] Closing browser..."
  ]
}
```

---

## Deployment to Render

### Step 1: Prepare Repository

1. **Create `.gitignore`** (if not exists)
   ```
   venv/
   __pycache__/
   *.pyc
   .pytest_cache/
   .env
   ```

2. **Commit all files**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

### Step 2: Create Render Web Service

1. **Sign up/Login to Render**: https://render.com
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub/GitLab repository**
4. **Configure the service:**

   | Setting | Value |
   |---------|-------|
   | **Name** | `amazon-product-search` |
   | **Environment** | `Python 3` |
   | **Region** | Choose closest to you |
   | **Branch** | `main` |
   | **Root Directory** | (leave blank) |
   | **Build Command** | `pip install -r requirements.txt && playwright install --with-deps chromium` |
   | **Start Command** | `gunicorn app:app --bind 0.0.0.0:$PORT` |
   | **Instance Type** | `Free` (or higher) |

5. **Add Environment Variables** (optional):
   - `PYTHON_VERSION`: `3.11.0`
   - `PORT`: Auto-configured by Render

6. **Click "Create Web Service"**

**Note:** The Procfile is automatically detected by Render and will be used if no Start Command is specified.

### Step 3: Access Your Deployed App

After deployment completes (5-10 minutes):
- Your app will be available at: `https://amazon-product-search.onrender.com`
- View logs in Render dashboard

### Important Notes for Render Deployment

⚠️ **Playwright on Render**:
- Render's free tier may have limited resources for browser automation
- Consider upgrading to a paid tier for better performance
- Headless mode is required on Render

⚠️ **Rate Limiting**:
- The app includes 30-second rate limiting per IP
- This prevents excessive requests and potential Amazon blocking

⚠️ **Cold Starts**:
- Free tier services sleep after inactivity
- First request after sleep may take 30-60 seconds

---

## API Documentation

### Endpoints

#### `GET /`
Main web interface

#### `GET /api/health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "service": "Amazon Product Search API"
}
```

#### `POST /api/search`
Search for a product on Amazon

**Request Body:**
```json
{
  "search_term": "string (required)",
  "headless": "boolean (optional, default: true)"
}
```

**Response:**
```json
{
  "success": "boolean",
  "product_name": "string or null",
  "price": "string or null",
  "error": "string or null",
  "logs": ["array of log strings"]
}
```

**Status Codes:**
- `200 OK`: Success
- `400 Bad Request`: Invalid request
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

---

## Rate Limiting

The application includes built-in rate limiting to prevent abuse:
- **30 seconds** minimum between requests per IP address
- Prevents excessive load on Amazon's servers
- Reduces risk of IP blocking

---

## Technical Details

### Technologies Used
- **Python 3.8+**: Core language
- **Playwright**: Browser automation
- **Flask**: Web framework
- **Bootstrap 5**: Frontend UI
- **pytest**: Testing framework
- **Gunicorn**: Production WSGI server

### Browser Automation Features
- **Headless Mode**: Runs without visible browser window
- **Timeout Handling**: 30-second timeout for page loads
- **Element Waiting**: Waits for elements before interaction
- **Popup Handling**: Automatically dismisses modal popups
- **Error Recovery**: Graceful handling of missing elements

### Code Quality
- ✅ Clean, documented code
- ✅ Type hints for better IDE support
- ✅ Comprehensive error handling
- ✅ Test coverage with pytest
- ✅ PEP 8 style compliance

---

## Testing

Run all tests:
```bash
pytest script_test.py -v
```

Run with coverage:
```bash
pytest script_test.py -v --cov=script
```

Test includes:
1. Navigation to Amazon
2. Popup handling
3. Product search
4. Data extraction
5. Price verification

---

## Troubleshooting

### Issue: "playwright: command not found"
**Solution:**
```bash
playwright install chromium
```

### Issue: Browser won't launch
**Solution:**
- Ensure Playwright browsers are installed
- Try headless mode: `headless=True`
- Check system dependencies (Linux may need additional packages)

### Issue: Rate limit errors
**Solution:**
- Wait 30 seconds between requests
- Check if another user is making requests from same IP

### Issue: Amazon blocking requests
**Solution:**
- Use headless mode
- Respect rate limits
- Avoid making too many requests in short time
- Consider adding random delays between actions

### Issue: "strict mode violation" or multiple elements found
**Solution:**
- Use **specific product names** instead of generic categories
- ✅ Good: "Nintendo Switch 2 OLED", "iPhone 15 Pro Max", "Sony WH-1000XM5"
- ❌ Bad: "phones", "headphones", "sony products"
- The script looks for specific product listings, not category pages

---

## Future Enhancements

Potential improvements:
- [ ] User authentication
- [ ] Request history/logging to database
- [ ] Multiple product comparison
- [ ] Price tracking over time
- [ ] Email notifications
- [ ] Support for other e-commerce sites
- [ ] Advanced rate limiting (per user)
- [ ] Caching for repeated searches

---

## License

This project was created for the City of Los Angeles General Services Department evaluation program.

---

## Contact

**Author:** George Lin
**Purpose:** City of Los Angeles GSD Evaluation Program
**Date:** 2025

---

## Acknowledgments

- Built with [Playwright](https://playwright.dev/)
- UI styled with [Bootstrap](https://getbootstrap.com/)
- Deployed on [Render](https://render.com/)