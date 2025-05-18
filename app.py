from src.app import app, server

# This file is used by Render to locate the application
if __name__ == "__main__":
    app.run_server(debug=False) 