# Connectify

## Overview

This project is a real-time chat application with user connection requests. It includes a Django backend with WebSocket support and a React frontend.

### Getting started

Follow these steps to set up and run the project.

#### 1. Clone this repo on your local.

      git clone https://github.com/yourusername/Connectify.git
      cd Connectify

#### 2. Create and activate virtual environment:

      python -m venv venv
      source venv/bin/activate  # On Windows use: venv\Scripts\activate

#### 3. Install Dependencies:

      pip install -r requirements.txt

#### 4. Apply migrations:

      python manage.py migrate

#### 5. Create a Superuser (Optional):

      python manage.py createsuperuser

#### 6. Run the Redis Server:

      redis-server
      
#### 7. Run the Development Server:

      python manage.py runserver
      (or)
      daphne -p 8000 core.asgi:application

  The backend development server will be available at `http://localhost:8000`.


## Configuration

  #### WebSocket URL:

  Make sure the WebSocket URL in the React frontend matches the URL where the Django server is running.

  #### Redis URL:

  Ensure the Host URL in the settings.py is set correctly to point to your redis server.

  
