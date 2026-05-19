import sys
import os
import time
import webbrowser
import uvicorn
import threading

def start_backend():
    # Make sure we add backend dir to path so it can import src
    backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))
    sys.path.insert(0, backend_dir)
    
    def run_uvicorn():
        # Change working directory so FastAPI resolves relative paths to frontend correctly
        os.chdir(backend_dir)
        uvicorn.run("src.controller.main:app", host="127.0.0.1", port=8000, log_level="warning")
        
    t = threading.Thread(target=run_uvicorn)
    t.daemon = True
    t.start()

if __name__ == "__main__":
    print("Initializing backend server...")
    start_backend()
    
    # Wait for uvicorn to boot
    time.sleep(2.5)
    
    print("Launching Traffic Flow Simulation System (Desktop Window)...")
    try:
        import webview
        # Create a premium native desktop window
        webview.create_window(
            "Traffic Flow Simulation System - Desktop Wrapper", 
            "http://127.0.0.1:8000/", 
            width=1200, 
            height=800,
            resizable=True
        )
        webview.start()
    except Exception as e:
        print(f"Error launching webview: {e}")
        print("Falling back to system browser...")
        webbrowser.open("http://127.0.0.1:8000/")
        
        # Keep process alive so backend runs in background
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Shutting down desktop app...")
