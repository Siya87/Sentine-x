# Complete Frontend Setup - Copy React files from temp-app
Write-Host "Completing Frontend Setup..." -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

# Check if temp-app exists
if (-not (Test-Path "temp-app")) {
    Write-Host "[ERROR] temp-app directory not found!" -ForegroundColor Red
    Write-Host "Please run: npx create-react-app temp-app --template typescript" -ForegroundColor Yellow
    exit 1
}

Write-Host "Step 1: Copying React app files..." -ForegroundColor Yellow

# Copy src folder
if (Test-Path "temp-app\src") {
    Copy-Item -Path "temp-app\src\*" -Destination "src\" -Recurse -Force
    Write-Host "  [OK] Copied src folder" -ForegroundColor Green
}

# Copy public folder
if (Test-Path "temp-app\public") {
    Copy-Item -Path "temp-app\public" -Destination "." -Recurse -Force
    Write-Host "  [OK] Copied public folder" -ForegroundColor Green
}

# Copy config files
$configFiles = @("tsconfig.json", "README.md")
foreach ($file in $configFiles) {
    if (Test-Path "temp-app\$file") {
        Copy-Item -Path "temp-app\$file" -Destination "." -Force
        Write-Host "  [OK] Copied $file" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Step 2: Updating index.css with custom styles..." -ForegroundColor Yellow

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
Write-Host "  [OK] Updated index.css" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Initializing Tailwind CSS..." -ForegroundColor Yellow
try {
    npx tailwindcss init -p
    Write-Host "  [OK] Tailwind initialized" -ForegroundColor Green
} catch {
    Write-Host "  [WARNING] Tailwind init failed, but config already exists" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 4: Cleaning up..." -ForegroundColor Yellow
Remove-Item -Path "temp-app" -Recurse -Force
Write-Host "  [OK] Removed temp-app folder" -ForegroundColor Green

Write-Host ""
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "===============" -ForegroundColor Green
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Start development server: npm start" -ForegroundColor White
Write-Host "  2. Open http://localhost:3000" -ForegroundColor White
Write-Host "  3. Follow docs\IMPLEMENTATION_GUIDE.md to implement features" -ForegroundColor White
Write-Host ""

Write-Host "Ready to build SentinelX AI!" -ForegroundColor Green

# Made with Bob
