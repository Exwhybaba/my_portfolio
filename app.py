from src.app import app, server

# Make the server object callable for WSGI
application = server

# This file is used by Render to locate the application
if __name__ == "__main__":
    app.run_server(debug=False) 