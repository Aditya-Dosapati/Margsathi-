# Frontend Setup Guide

## Quick Start

### 1. Install Node.js and npm

If you don't have Node.js installed:
- Download from: https://nodejs.org/
- Install Node.js (includes npm)

### 2. Install Dependencies

```bash
cd frontend
npm install
```

### 3. Start Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 4. Make Sure Backend is Running

In a separate terminal, start the FastAPI backend:

```bash
cd backend
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── Layout.jsx          # Navigation and layout wrapper
│   ├── pages/
│   │   ├── Home.jsx            # Home page with hero and features
│   │   ├── Routing.jsx         # Smart routing page
│   │   ├── Parking.jsx         # Parking prediction page
│   │   └── Translation.jsx    # Sign translation page
│   ├── App.jsx                 # Main app with routes
│   ├── main.jsx                # Entry point
│   └── index.css               # Tailwind CSS styles
├── index.html
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## Features Implemented

### ✅ Home Page
- Project name and tagline
- "Try Demo" button
- Feature cards (Smart Routing, Parking Prediction, Sign Translation)
- Stats section

### ✅ Smart Routing Page
- Source and destination input fields
- Event type dropdown (Road Closure, Protest, Concert, etc.)
- Route result card showing:
  - Recommended route path
  - Distance, duration, CO₂ emissions
  - Waypoints list
  - Reason for route selection

### ✅ Parking Prediction Page
- Area name input
- Area type selector (Commercial, Residential, Mixed)
- Time selection (optional, defaults to current time)
- Visual availability meter (color-coded)
- Occupancy percentage and confidence score
- Explanation of prediction

### ✅ Sign Translation Page
- Text input area
- Quick example buttons (Parking Available, No Parking, etc.)
- Language selector (Hindi, Tamil, Telugu, Bengali, etc.)
- Translated output display
- Copy to clipboard button
- Original vs translated comparison

## Design Features

- **Clean & Modern**: Minimal design with Tailwind CSS
- **Responsive**: Works on desktop, tablet, and mobile
- **Professional**: Consistent color scheme and typography
- **Interactive**: Hover effects, loading states, error handling
- **Accessible**: Proper labels and semantic HTML

## API Integration

The frontend connects to your FastAPI backend at `http://localhost:8000`:

- `POST /api/routing/suggest` - Route suggestions
- `GET /api/parking/predict` - Parking predictions
- `POST /api/translation/simple` - Text translation

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## Troubleshooting

### Port Already in Use
If port 3000 is busy, Vite will automatically use the next available port.

### Backend Connection Issues
Make sure the FastAPI backend is running on port 8000. The frontend proxy is configured in `vite.config.js`.

### Styling Issues
Make sure Tailwind CSS is properly configured. Check `tailwind.config.js` and `postcss.config.js`.

## Next Steps

1. Install Node.js if not already installed
2. Run `npm install` in the frontend directory
3. Start both backend and frontend servers
4. Open `http://localhost:3000` in your browser
5. Test all features!

## Demo Flow

1. **Home Page** → Click "Try Demo" or navigate to any feature
2. **Smart Routing** → Enter source/destination, select event, get route
3. **Parking Prediction** → Enter area, select type/time, see prediction
4. **Sign Translation** → Enter text, select language, get translation

Enjoy your hackathon demo! 🚀

