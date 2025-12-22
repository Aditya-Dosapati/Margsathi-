# How to Install Node.js on Windows

## Quick Installation Steps

### Step 1: Download Node.js
1. Go to **https://nodejs.org/**
2. Click the **LTS (Long Term Support)** button - this is the recommended version
3. Download the Windows Installer (.msi file)

### Step 2: Install Node.js
1. Double-click the downloaded `.msi` file
2. Click **Next** through the installation wizard
3. **Important**: Make sure "Automatically install the necessary tools" is checked
4. Accept the license agreement
5. Choose installation location (default is fine)
6. Click **Install**
7. Wait for installation to complete
8. Click **Finish**

### Step 3: Restart PowerShell
- **Close your current PowerShell window completely**
- Open a **new PowerShell window**
- This is important so PATH environment variables are updated

### Step 4: Verify Installation
Run these commands in your new PowerShell window:

```powershell
node -v
npm -v
```

You should see version numbers like:
```
v20.x.x
10.x.x
```

### Step 5: Install Frontend Dependencies
Once Node.js is installed, navigate to your frontend folder and install:

```powershell
cd C:\Users\thanu\OneDrive\Desktop\margsathi\frontend
npm install
```

### Step 6: Start Development Server
```powershell
npm run dev
```

## Alternative: Using Chocolatey (if you have it)

If you have Chocolatey package manager installed:

```powershell
choco install nodejs-lts
```

## Troubleshooting

### If `node` or `npm` still not recognized after installation:

1. **Check if Node.js is installed:**
   - Go to: `C:\Program Files\nodejs\`
   - If the folder exists, Node.js is installed but PATH might not be updated

2. **Manually add to PATH:**
   - Press `Win + X` → System → Advanced system settings
   - Click "Environment Variables"
   - Under "System variables", find "Path" and click "Edit"
   - Click "New" and add: `C:\Program Files\nodejs\`
   - Click OK on all dialogs
   - Restart PowerShell

3. **Verify PATH:**
   ```powershell
   $env:PATH -split ';' | Select-String nodejs
   ```

### If installation fails:
- Make sure you have administrator rights
- Try running the installer as Administrator (Right-click → Run as administrator)
- Check Windows Defender/Antivirus isn't blocking the installation

## What Gets Installed

- **Node.js** - JavaScript runtime
- **npm** - Node Package Manager (comes with Node.js)
- **npx** - Package runner (comes with npm)

## Next Steps After Installation

1. ✅ Verify Node.js: `node -v`
2. ✅ Verify npm: `npm -v`
3. ✅ Install frontend dependencies: `cd frontend && npm install`
4. ✅ Start dev server: `npm run dev`
5. ✅ Open browser: `http://localhost:3000`

## Quick Test

After installation, test with a simple command:

```powershell
node -e "console.log('Node.js is working!')"
```

You should see: `Node.js is working!`

---

**Note**: The LTS (Long Term Support) version is recommended for stability. Current LTS is usually v20.x.x or v18.x.x.

