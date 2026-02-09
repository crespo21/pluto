import sys
sys.path.insert(0, '.')
try:
    from src.main import app
    print("App imported successfully")
    print(f"Number of routes: {len(app.routes)}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
