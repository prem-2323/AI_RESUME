# Complete Frontend Website

This folder contains one combined React + Vite frontend that includes all module pages:
- Module 1: Resume Analyzer
- Module 5: Interactive Resume Editor
- Module 2: Smart Preparation Hub
- Module 3: Resume Screening
- Module 4: Career Domain Switch

Use the top navigation in the app to switch between modules.

## Run (Frontend Only)

```powershell
cd complete
npm install
npm run dev
```

Open the URL printed by Vite (usually `http://localhost:5173`).

## Build

```powershell
npm run build
```

## Optional API URL

Some module pages call backend APIs. If needed, create a `.env` file in this `complete` folder:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

If no backend is running, the UI still loads (frontend only), but API-driven actions will fail at runtime.
