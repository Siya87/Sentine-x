# SentinelX AI - Frontend Setup Script
# This script sets up the React frontend application

Write-Host "SentinelX AI Frontend Setup" -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Move documentation files
Write-Host "Step 1: Organizing documentation files..." -ForegroundColor Yellow
$docsDir = "docs"
if (-not (Test-Path $docsDir)) {
    New-Item -ItemType Directory -Path $docsDir | Out-Null
}

$docFiles = @(
    "COMPONENT_SPECIFICATIONS.md",
    "IMPLEMENTATION_GUIDE.md",
    "SETUP_GUIDE.md"
)

foreach ($file in $docFiles) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "$docsDir\$file" -Force
        Write-Host "  [OK] Moved $file to docs/" -ForegroundColor Green
    }
}

# Step 2: Check Node.js
Write-Host ""
Write-Host "Step 2: Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "  [OK] Node.js installed: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  [ERROR] Node.js not found!" -ForegroundColor Red
    Write-Host "  Please install Node.js from https://nodejs.org/" -ForegroundColor Red
    Write-Host "  Then run this script again." -ForegroundColor Red
    exit 1
}

# Step 3: Create React App
Write-Host ""
Write-Host "Step 3: Creating React application with TypeScript..." -ForegroundColor Yellow
Write-Host "  This will take 2-5 minutes..." -ForegroundColor Gray

try {
    npx create-react-app . --template typescript
    Write-Host "  [OK] React app created successfully!" -ForegroundColor Green
} catch {
    Write-Host "  [ERROR] Failed to create React app" -ForegroundColor Red
    Write-Host "  Error: $_" -ForegroundColor Red
    exit 1
}

# Step 4: Install dependencies
Write-Host ""
Write-Host "Step 4: Installing dependencies..." -ForegroundColor Yellow
Write-Host "  This will take 1-3 minutes..." -ForegroundColor Gray

$dependencies = @(
    "react-router-dom",
    "axios",
    "framer-motion",
    "@headlessui/react",
    "@heroicons/react",
    "recharts",
    "react-markdown",
    "date-fns",
    "react-hot-toast",
    "clsx"
)

$devDependencies = @(
    "tailwindcss",
    "postcss",
    "autoprefixer",
    "@types/node"
)

try {
    Write-Host "  Installing production dependencies..." -ForegroundColor Gray
    npm install $dependencies
    
    Write-Host "  Installing dev dependencies..." -ForegroundColor Gray
    npm install -D $devDependencies
    
    Write-Host "  [OK] All dependencies installed!" -ForegroundColor Green
} catch {
    Write-Host "  [ERROR] Failed to install dependencies" -ForegroundColor Red
    Write-Host "  Error: $_" -ForegroundColor Red
    exit 1
}

# Step 5: Initialize Tailwind CSS
Write-Host ""
Write-Host "Step 5: Initializing Tailwind CSS..." -ForegroundColor Yellow
try {
    npx tailwindcss init -p
    Write-Host "  [OK] Tailwind CSS initialized!" -ForegroundColor Green
} catch {
    Write-Host "  [ERROR] Failed to initialize Tailwind CSS" -ForegroundColor Red
    Write-Host "  Error: $_" -ForegroundColor Red
}

# Step 6: Create .env file
Write-Host ""
Write-Host "Step 6: Creating environment configuration..." -ForegroundColor Yellow
$envContent = @"
REACT_APP_API_URL=http://localhost:8000
REACT_APP_NAME=SentinelX AI
REACT_APP_VERSION=1.0.0
"@

Set-Content -Path ".env" -Value $envContent
Write-Host "  [OK] .env file created!" -ForegroundColor Green

# Step 7: Update Tailwind config
Write-Host ""
Write-Host "Step 7: Configuring Tailwind CSS..." -ForegroundColor Yellow
$tailwindConfig = @"
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        gray: {
          850: '#1a202e',
        }
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    },
  },
  plugins: [],
}
"@

Set-Content -Path "tailwind.config.js" -Value $tailwindConfig
Write-Host "  [OK] Tailwind config updated!" -ForegroundColor Green

# Step 8: Update index.css
Write-Host ""
Write-Host "Step 8: Updating global styles..." -ForegroundColor Yellow
$indexCss = @"
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-gray-900 text-gray-100;
  }
}

@layer components {
  .btn-primary {
    @apply px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors;
  }
  
  .card {
    @apply bg-gray-800 rounded-lg border border-gray-700 p-6;
  }
  
  .input-field {
    @apply w-full bg-gray-700 text-white rounded-lg px-4 py-2 border border-gray-600 focus:border-blue-500 focus:outline-none;
  }
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #1F2937;
}

::-webkit-scrollbar-thumb {
  background: #4B5563;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #6B7280;
}
"@

Set-Content -Path "src\index.css" -Value $indexCss
Write-Host "  [OK] Global styles updated!" -ForegroundColor Green

# Step 9: Create directory structure
Write-Host ""
Write-Host "Step 9: Creating project structure..." -ForegroundColor Yellow
$directories = @(
    "src\components\layout",
    "src\components\dashboard",
    "src\components\phishing",
    "src\components\osint",
    "src\components\threat",
    "src\components\report",
    "src\components\chat",
    "src\components\shared",
    "src\services",
    "src\types",
    "src\hooks",
    "src\utils",
    "src\pages"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  [OK] Created: $dir" -ForegroundColor Green
    }
}

# Summary
Write-Host ""
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "===============" -ForegroundColor Green
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Review documentation in the 'docs' folder" -ForegroundColor White
Write-Host "  2. Implement components following docs\IMPLEMENTATION_GUIDE.md" -ForegroundColor White
Write-Host "  3. Start development server: npm start" -ForegroundColor White
Write-Host "  4. Open http://localhost:3000 in your browser" -ForegroundColor White
Write-Host ""

Write-Host "Documentation:" -ForegroundColor Cyan
Write-Host "  - Component Specs: docs\COMPONENT_SPECIFICATIONS.md" -ForegroundColor White
Write-Host "  - Implementation Guide: docs\IMPLEMENTATION_GUIDE.md" -ForegroundColor White
Write-Host "  - Setup Guide: docs\SETUP_GUIDE.md" -ForegroundColor White
Write-Host ""

Write-Host "Ready to build SentinelX AI!" -ForegroundColor Green

# Made with Bob
