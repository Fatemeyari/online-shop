<h1>Online Shop</h1>

<p>
A Django-based online shop application built with Django and PostgreSQL,
with Celery for asynchronous background task processing and Redis as the
Celery message broker.
</p>

<h2>Overview</h2>

<p>
This project is an online shop application developed with Django.
It provides a structured backend for managing users, products, and
shopping-related operations. PostgreSQL is used for persistent data storage,
while Celery and Redis are used to handle background tasks asynchronously.
The entire application environment can be run using Docker and Docker Compose.
</p>

<h2>Features</h2>

<h3>Authentication</h3>

<ul>
  <li>User registration</li>
  <li>User login</li>
  <li>User logout</li>
  <li>User authentication and authorization</li>
  <li>User management</li>
</ul>

<h3>Product Management</h3>

<ul>
  <li>Create and manage products</li>
  <li>Product information management</li>
  <li>Product image handling</li>
  <li>Product categorization</li>
</ul>

<h3>Shopping</h3>

<ul>
  <li>Browse available products</li>
  <li>View product details</li>
  <li>Manage shopping-related data</li>
  <li>Order management</li>
</ul>

<h3>Background Tasks</h3>

<ul>
  <li>Asynchronous background task processing with Celery</li>
  <li>Redis as the Celery message broker</li>
  <li>Celery Worker for executing background tasks</li>
</ul>

<h3>Administration</h3>

<ul>
  <li>Django Admin panel</li>
  <li>Manage users</li>
  <li>Manage products</li>
  <li>Manage application data</li>
</ul>

<h2>Database</h2>

<p>
The project uses PostgreSQL for persistent data storage.
PostgreSQL runs as a Docker container within the application environment.
</p>

<a href="https://github.com/Fatemeyari/online-shop/blob/main/docs/Untitled%20Diagram.drawio.png">
  <img src="docs/Untitled Diagram.drawio.png" alt="Online Shop Architecture Diagram" width="700">
</a>

<h2>Technology Stack</h2>

<ul>
  <li>Python</li>
  <li>Django 4.2</li>
  <li>PostgreSQL</li>
  <li>Celery 5.4.0</li>
  <li>Redis 5.0.1</li>
  <li>Pillow 12.2.0</li>
  <li>Psycopg 3.2.12</li>
  <li>python-decouple 3.8</li>
  <li>Faker 40.23.x</li>
  <li>Docker</li>
  <li>Docker Compose</li>
</ul>

<h2>Architecture</h2>

<p>
The application uses Django as the main application framework.
PostgreSQL is responsible for persistent data storage, while Celery handles
background tasks. Redis acts as the message broker between the Django
application and Celery workers.
</p>

<pre>
                         ┌─────────────────┐
                         │     Client      │
                         │   Web Browser   │
                         └────────┬────────┘
                                  │
                               HTTP/HTTPS
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     Django      │
                         │   Application   │
                         └───────┬─┬───────┘
                                 │ │
                   SQL Queries   │ │   Create Background Task
                                 │ │
                    ┌────────────┘ └────────────┐
                    ▼                           ▼
           ┌─────────────────┐        ┌─────────────────┐
           │   PostgreSQL    │        │      Redis      │
           │    Database     │        │  Message Broker │
           └─────────────────┘        └────────┬────────┘
                                              │
                                           Task Queue
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │ Celery Worker   │
                                    │                 │
                                    │ Executes Tasks  │
                                    └─────────────────┘
</pre>

<h3>Component Responsibilities</h3>

<ul>
  <li>
    <strong>Django:</strong>
    Handles HTTP requests, application logic, authentication, and business operations.
  </li>

  <li>
    <strong>PostgreSQL:</strong>
    Stores persistent application data.
  </li>

  <li>
    <strong>Celery:</strong>
    Handles asynchronous and background task processing.
  </li>

  <li>
    <strong>Redis:</strong>
    Acts as the message broker for Celery.
  </li>

  <li>
    <strong>Celery Worker:</strong>
    Receives and executes queued background tasks.
  </li>

  <li>
    <strong>Pillow:</strong>
    Handles image processing.
  </li>
</ul>

<p>
<strong>Note:</strong>
Redis does not execute Celery tasks. It works as the message broker that
queues and delivers tasks to Celery workers.
</p>

<h2>How It Works</h2>

<ol>
  <li>User interacts with the online shop through the web application.</li>
  <li>Django receives and processes the request.</li>
  <li>Application data is stored in PostgreSQL.</li>
  <li>When a background task is required, Django sends the task to Redis.</li>
  <li>Redis queues the task as the Celery message broker.</li>
  <li>Celery Worker receives and executes the task in the background.</li>
</ol>

<h2>Docker</h2>

<p>
Docker is used to provide a consistent development environment for the
application and its dependencies.
</p>

<p>
The application can be started using Docker Compose, which manages the
required services such as Django, PostgreSQL, Redis, and Celery.
</p>

<h3>Requirements</h3>

<ul>
  <li>Docker</li>
  <li>Docker Compose</li>
  <li>Git</li>
</ul>

<h3>Run the Project</h3>

<p>Clone the repository:</p>

<pre>
git clone https://github.com/Fatemeyari/online-shop.git
cd online-shop
</pre>

<p>Build and start the containers:</p>

<pre>
docker compose up --build
</pre>

<p>
After the containers are running, the application will normally be available at:
</p>

<pre>
http://127.0.0.1:8000/
</pre>

<h3>Run in Detached Mode</h3>

<pre>
docker compose up -d
</pre>

<h3>Stop the Application</h3>

<pre>
docker compose down
</pre>

<h3>View Container Logs</h3>

<pre>
docker compose logs
</pre>

<p>
To follow the logs in real time:
</p>

<pre>
docker compose logs -f
</pre>

<h2>Environment Variables</h2>

<p>
The project uses environment variables for sensitive and
environment-specific configuration.
</p>

<h2>Database Setup</h2>

<p>
Database migrations can be executed inside the Django container.
</p>

<pre>
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
</pre>

<h2>Create a Superuser</h2>

<pre>
docker compose exec web python manage.py createsuperuser
</pre>


<h2>Celery &amp; Redis</h2>

<p>
Celery is used to execute background tasks asynchronously.
Redis is used as the message broker that passes queued tasks from the
Django application to Celery workers.
</p>

<p>
Both Redis and Celery can run as separate services managed by Docker Compose.
</p>

<h3>Celery Task Flow</h3>

<pre>
Django
   │
   │ Create Task
   ▼
Redis
   │
   │ Task Queue
   ▼
Celery Worker
   │
   │ Execute
   ▼
Background Task
</pre>

<h2>Project Structure</h2>

<h2>Static &amp; Media Files</h2>

<ul>
  <li>Static CSS files</li>
  <li>JavaScript files</li>
  <li>Images</li>
  <li>Fonts</li>
  <li>User-uploaded files</li>
  <li>Product images</li>
</ul>

<p>
Static and media files are handled by the Django application during development.
For production environments, they should be configured according to the
deployment environment.
</p>

<h2>Faker</h2>

<p>
Faker is used to generate realistic sample data during development.
</p>

<pre>
from faker import Faker

fake = Faker()

name = fake.name()
email = fake.email()
address = fake.address()
</pre>

<h2>Security</h2>

<ul>
  <li>Set <code>DEBUG=False</code> in production.</li>
  <li>Use a strong <code>SECRET_KEY</code>.</li>
  <li>Never commit the <code>.env</code> file.</li>
  <li>Configure <code>ALLOWED_HOSTS</code>.</li>
  <li>Use HTTPS in production.</li>
  <li>Protect sensitive environment variables.</li>
  <li>Use appropriate database credentials.</li>
  <li>Keep project dependencies updated.</li>
</ul>

<h2>Dependencies</h2>

<p>
The project's Python dependencies are defined in <code>requirements.txt</code>.
</p>

<pre>
asgiref==3.11.1
Django==4.2
pillow==12.2.0
psycopg==3.2.12
psycopg-binary==3.2.12
python-decouple==3.8
sqlparse==0.5.5
typing_extensions==4.15.0
celery==5.4.0
redis==5.0.1
Faker==40.23.x
</pre>

<h2>Git Workflow</h2>

<h3>Create a Feature Branch</h3>

<pre>
git checkout -b feature/feature-name
</pre>

<h3>Commit Changes</h3>

<pre>
git add .
git commit -m "feat: add new feature"
</pre>

<h3>Push the Branch</h3>

<pre>
git push origin feature/feature-name
</pre>

<h2>Contributing</h2>

<p>
Contributions are welcome. If you would like to improve the project,
you can fork the repository, create a new branch, make your changes,
and open a Pull Request.
</p>

<h2>License</h2>

<p>
This project is licensed under the <strong>MIT License</strong>.
</p>

<h2>Author</h2>

<p>
<strong>Fateme Yari</strong>
</p>

<h2>Project Status</h2>

<p>
<strong>Active Development</strong>
</p>

<p>
The project is currently under development and may receive new features,
improvements, and architectural changes over time.
</p>
