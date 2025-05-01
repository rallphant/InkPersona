# InkPersona: Chatea con Personajes Literarios

InkPersona es una aplicación web que permite a los usuarios interactuar y conversar con representaciones de Inteligencia Artificial (IA) de personajes icónicos de la literatura clásica.

## Características Principales

*   **Exploración de Personajes:** Navega por un catálogo de personajes literarios con sus detalles (libro, autor, descripción).
*   **Chat con IA:** Mantén conversaciones dinámicas con la IA que emula la personalidad y el conocimiento del personaje seleccionado.
*   **Autenticación de Usuarios:** Registro e inicio de sesión para una experiencia personalizada.
*   **Historial de Conversaciones:** Revisa y gestiona tus conversaciones pasadas con diferentes personajes.
*   **Interfaz Responsiva:** Diseño adaptable a diferentes tamaños de pantalla.

## Tecnologías Utilizadas

*   **Backend:** Python, Django, Django REST Framework
*   **Frontend:** HTML, CSS, JavaScript
*   **IA Conversacional:** Groq API (utilizando modelos como Llama 3)
*   **Base de Datos:** SQLite (desarrollo)
*   **Control de Versiones:** Git

## Instalación y Puesta en Marcha

Sigue estos pasos para configurar y ejecutar el proyecto en tu entorno local:

1.  **Prerrequisitos:**
    *   Python 3.8 o superior
    *   pip (gestor de paquetes de Python)
    *   `virtualenv` (recomendado para crear entornos virtuales)

2.  **Clonar el Repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd literary-character-ai
    ```

3.  **Crear y Activar Entorno Virtual:**
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```

4.  **Instalar Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configurar Variables de Entorno:**
    Crea un archivo `.env` en la raíz del proyecto (junto a `manage.py`) y añade las siguientes variables (ajusta los valores según sea necesario):
    ```dotenv
    DJANGO_SECRET_KEY='tu_clave_secreta_aqui'
    DEBUG=True
    GROQ_API_KEY='tu_api_key_de_groq'
    GROQ_MODEL='llama3-8b-8192' # O el modelo que prefieras usar
    # Configuración de base de datos (opcional, por defecto usa SQLite)
    # DATABASE_URL='postgres://user:password@host:port/dbname'
    ```
    *   **IMPORTANTE:** Asegúrate de que `GROQ_API_KEY` contenga una clave válida obtenida de GroqCloud.

6.  **Aplicar Migraciones de Base de Datos:**
    ```bash
    python manage.py migrate
    ```

7.  **Crear un Superusuario (para acceder al Admin):**
    ```bash
    python manage.py createsuperuser
    ```
    Sigue las instrucciones para crear tu cuenta de administrador.

8.  **Cargar Datos Iniciales (Opcional):**
    *   Si tienes un archivo de *fixtures* (ej. `characters_data.json`) para cargar personajes iniciales:
        ```bash
        python manage.py loaddata characters_data.json
        ```
    *   Alternativamente, puedes añadir personajes manualmente a través del panel de administración de Django (`/admin/`).

9.  **Ejecutar el Servidor de Desarrollo:**
    ```bash
    python manage.py runserver
    ```

10. **Acceder a la Aplicación:**
    Abre tu navegador y ve a `http://127.0.0.1:8000/`.

## Uso

*   Visita la página principal para ver los personajes.
*   Regístrate o inicia sesión para poder chatear.
*   Haz clic en un personaje para ver sus detalles e iniciar una conversación.
*   Accede a tu historial desde el menú de navegación (si estás logueado).

## API

*   El endpoint principal para la interacción del chat es `/characters/api/chat/` (requiere autenticación y método POST).

