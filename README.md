# InkPersona: Chat with Literary Characters

InkPersona is a web application that allows users to interact and converse with AI representations of iconic characters from classic literature.

## Main Features

* **Character Exploration:** Browse a catalog of literary characters with their details (book, author, description).
* **AI Chat:** Engage in dynamic conversations with AI that emulates the personality and knowledge of the selected character.
* **User Authentication:** Register and log in for a personalized experience.
* **Conversation History:** Review and manage your past conversations with different characters.
* **Responsive Interface:** Design adaptable to various screen sizes.

## Technologies Used

* **Backend:** Python, Django, Django REST Framework
* **Frontend:** HTML, CSS, JavaScript
* **Conversational AI:** Groq API (using models such as Llama 3)
* **Database:** SQLite (development)
* **Version Control:** Git

## Installation and Setup

Follow these steps to configure and run the project in your local environment:

1. **Prerequisites:**
    * Python 3.8 or higher
    * pip (Python package manager)
    * `virtualenv` (recommended for creating virtual environments)

2. **Clone the Repository:**
    ```bash
    git clone <REPOSITORY_URL>
    cd literary-character-ai
    ```

3. **Create and Activate Virtual Environment:**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

4. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Configure Environment Variables:**
    Create a `.env` file in the root directory of the project (next to `manage.py`) and add the following variables (adjust values as needed):
    ```dotenv
    DJANGO_SECRET_KEY='your_secret_key_here'
    DEBUG=True
    GROQ_API_KEY='your_groq_api_key_here'
    GROQ_MODEL='llama3-8b-8192' # Or the model you prefer to use
    # Database configuration (optional, SQLite is used by default)
    # DATABASE_URL='postgres://user:password@host:port/dbname'
    ```
    * **IMPORTANT:** Ensure that `GROQ_API_KEY` contains a valid key obtained from GroqCloud.

6. **Apply Database Migrations:**
    ```bash
    python manage.py migrate
    ```

7. **Create a Superuser (to access the Admin):**
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create your admin account.

8. **Load Initial Data (Optional):**
    * If you have a *fixtures* file (e.g., `characters_data.json`) to load initial characters:
        ```bash
        python manage.py loaddata characters_data.json
        ```
    * Alternatively, you can manually add characters through the Django admin panel (`/admin/`).

9. **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```

10. **Access the Application:**
    Open your browser and go to `http://127.0.0.1:8000/`.

## Usage

* Visit the homepage to view the characters.
* Register or log in to be able to chat.
* Click on a character to view details and start a conversation.
* Access your chat history from the navigation menu (if logged in).

## API

* The main endpoint for chat interaction is `/characters/api/chat/` (requires authentication and POST method).
