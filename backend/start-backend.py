#!/usr/bin/env python3
"""
SentinelX AI - Backend Startup Script
Cross-platform Python script to start the backend server
"""
import os
import sys
import subprocess
import platform

def main():
    print("=" * 50)
    print(" SentinelX AI - Backend Startup Script")
    print("=" * 50)
    print()
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Check if virtual environment exists
    venv_path = os.path.join(script_dir, "venv")
    if not os.path.exists(venv_path):
        print("❌ Error: Virtual environment not found!")
        print(f"   Expected location: {venv_path}")
        print("\n💡 Please create a virtual environment first:")
        print("   python -m venv venv")
        sys.exit(1)
    
    # Determine the Python executable in the virtual environment
    if platform.system() == "Windows":
        python_exe = os.path.join(venv_path, "Scripts", "python.exe")
    else:
        python_exe = os.path.join(venv_path, "bin", "python")
    
    if not os.path.exists(python_exe):
        print(f"❌ Error: Python executable not found at {python_exe}")
        sys.exit(1)
    
    print("✅ Virtual environment found")
    print(f"📍 Working directory: {script_dir}")
    print()
    
    # Start the server
    print("🚀 Starting backend server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("📖 ReDoc: http://localhost:8000/redoc")
    print()
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    print()
    
    try:
        # Run uvicorn with the virtual environment's Python
        subprocess.run([
            python_exe, "-m", "uvicorn",
            "app.main:app",
            "--reload",
            "--port", "8000",
            "--host", "0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

# Made with Bob
