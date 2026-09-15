import os
import sys

# Ensure backend directory is in sys.path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("🚨 Starting OIL-SAFE AI Industrial Safety Command Center")
    print("=" * 60)
    print("• Web Dashboard:  http://localhost:8000")
    print("• API Docs:       http://localhost:8000/docs")
    print("• OpenAPI Spec:   http://localhost:8000/openapi.json")
    print("=" * 60)
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, app_dir=backend_path)
