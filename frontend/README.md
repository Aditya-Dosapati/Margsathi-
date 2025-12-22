# MARGSATHI Frontend

Modern React frontend for the MARGSATHI Mobility Intelligence Platform.

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls
- **Lucide React** - Icon library

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── Layout.jsx       # Main layout with navigation
│   ├── pages/
│   │   ├── Home.jsx         # Home page
│   │   ├── Routing.jsx      # Smart routing page
│   │   ├── Parking.jsx      # Parking prediction page
│   │   └── Translation.jsx  # Sign translation page
│   ├── App.jsx              # Main app component with routes
│   ├── main.jsx             # Entry point
│   └── index.css            # Global styles and Tailwind
├── index.html
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## Features

### 1. Home Page
- Project branding and tagline
- "Try Demo" button
- Feature cards with navigation
- Stats section

### 2. Smart Routing Page
- Source and destination inputs
- Event type dropdown
- Route result card with:
  - Recommended route
  - Distance, duration, CO₂ emissions
  - Waypoints list

### 3. Parking Prediction Page
- Area input
- Area type selector
- Time selection
- Visual availability meter
- Occupancy percentage and confidence

### 4. Sign Translation Page
- Text input with example buttons
- Language selector
- Translated output with copy button
- Original vs translated comparison

## API Integration

The frontend connects to the FastAPI backend running on `http://localhost:8000`.

Endpoints used:
- `POST /api/routing/suggest` - Get route suggestions
- `GET /api/parking/predict` - Predict parking availability
- `POST /api/translation/simple` - Translate text

## Design System

### Colors
- Primary: Blue (`primary-600`)
- Success: Green
- Warning: Yellow
- Error: Red
- Neutral: Gray scale

### Components
- Cards with shadow and rounded corners
- Primary and secondary buttons
- Input fields with focus states
- Responsive grid layouts

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

Built for hackathon demonstration purposes.

