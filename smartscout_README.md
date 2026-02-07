# SmartScout
SmartScout is a Smart Recruitment and Employee Management System designed to simplify the recruitment process for employees and employers alike.

## Features
* Employee profile management
* Job posting and application management
* Recruitment form generation
* Team management
* Role-based authentication
* Custom user model
* User registration and login
* Admin panel for managing users, jobs, and applications
* Manager dashboard for managing employees and teams
* Project assignment

## Tech Stack
| Technology | Description |
| --- | --- |
| HTML | HyperText Markup Language for structuring content |
| SQLite | Relational database management system |
| Vanta.js | JavaScript library for animations and effects |
| JavaScript | Programming language for client-side scripting |
| CSS | Cascading Style Sheets for styling |
| Python | Programming language for backend development |
| Django | Python web framework for building scalable applications |
| Tailwind CSS | Utility-first CSS framework for styling |

## Architecture
The system follows a Model-View-Template (MVT) architecture pattern, which is a variant of the Model-View-Controller (MVC) pattern. This pattern separates the application logic into three interconnected components: models, views, and templates.
```mermaid
graph LR
    A[Employee] -->|submits application|> B[Job Posting]
    B -->|is managed by|> C[Manager]
    C -->|creates recruitment form|> D[Recruitment Form]
    D -->|is filled by|> A
    A -->|has profile|> E[Employee Profile]
    E -->|is viewed by|> C
```
```mermaid
graph LR
    A[User] -->|registers|> B[Database]
    B -->|stores user data|> C[Admin Panel]
    C -->|manages users, jobs, and applications|> D[Manager Dashboard]
    D -->|manages employees and teams|> E[Team Management]
    E -->|assigns projects|> F[Project Management]
```

## Getting Started
### Prerequisites
* Python 3.x
* Django 3.x or higher
* Node.js (for frontend dependencies)
* SQLite (default database)

### Installation Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/Devan019/smartscout.git
   cd SmartScout
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```
3. Install required packages:
   ```sh
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```sh
   python manage.py migrate
   ```
5. Run the development server:
   ```sh
   python manage.py runserver
   ```
6. Open your browser and navigate to:
   ```sh
   http://localhost:8000
   ```

## Project Structure
```markdown
├── SmartScout/
│   ├── employee/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── pdfScan.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── manager/
│   │   ├── __init__.py
│   │   ├── accepted.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── import_file.py
│   │   ├── models.py
│   │   ├── rejection.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── utils.py
│   │   └── views.py
│   ├── media/
│   │   └── media/
│   │       ├── profile_pics/
│   │       └── resumes/
│   ├── myadmin/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── messege.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── myauth/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── smartscout/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── manage.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── wsgi.py
│   ├── static/
│   │   ├── json/
│   │   │   └── skill.json
│   │   └── scripts/
│   │       ├── employee/
│   │       │   └── updateEmployeeProfile.js
│   │       ├── manager/
│   │       │   ├── generateRecruitmentForm.js
│   │       │   ├── ManagerDashboard.js
│   │       │   ├── Sortedprofiles.js
│   │       │   ├── TeamDashboard.js
│   │       │   └── updateRecruitmentForm.js
│   │       └── myadmin/
│   │           ├── manages.js
│   │           └── show_manager.js
│   ├── staticfiles_build/
│   │   └── static/
│   │       ├── admin/
│   │       │   ├── css/
│   │       │   ├── img/
│   │       │   └── js/
│   │       ├── css/
│   │       │   └── dist/
│   │       ├── json/
│   │       │   ├── skill.0cf635d87902.json
│   │       │   ├── skill.0cf635d87902.json.gz
│   │       │   ├── skill.json
│   │       │   └── skill.json.gz
│   │       ├── scripts/
│   │       │   ├── employee/
│   │       │   ├── manager/
│   │       │   └── myadmin/
│   │       └── staticfiles.json
│   ├── templates/
│   │   ├── employee/
│   │   │   ├── createCandidate.html
│   │   │   ├── EmployeeProfile.html
│   │   │   ├── home.html
│   │   │   ├── jobs.html
│   │   │   ├── nav.html
│   │   │   ├── profile.html
│   │   │   └── updateEmployeeProfile.html
│   │   ├── include/
│   │   │   ├── 404.html
│   │   │   ├── footer.html
│   │   │   └── techstack.html
│   │   ├── manager/
│   │   │   ├── generateRecruitmentForm.html
│   │   │   ├── home.html
│   │   │   ├── ManagerDashboard.html
│   │   │   ├── nav.html
│   │   │   ├── showApplicationsStatus.html
│   │   │   ├── showProfile.html
│   │   │   ├── showrecruitmentForms.html
│   │   │   ├── SortedProfiles.html
│   │   │   ├── TeamDashboard.html
│   │   │   └── updateRecruitmentForm.html
│   │   ├── myadmin/
│   │   │   ├── add_manager_form.html
│   │   │   ├── home.html
│   │   │   ├── manages.html
│   │   │   ├── nav.html
│   │   │   └── show_manager.html
│   │   ├── myauth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── home.html
│   │   └── index.html
│   ├── .gitignore
│   ├── build.sh
│   ├── dependencies.txt
│   ├── manage.py
│   ├── README.md
│   ├── requirements.txt
│   └── runtime.txt
├── .gitattributes
├── .gitignore
├── readme.md
└── requirements.txt
```
The project structure consists of several directories and files, including:
* `employee/`: contains employee-related models, views, and templates
* `manager/`: contains manager-related models, views, and templates
* `myadmin/`: contains admin-related models, views, and templates
* `myauth/`: contains authentication-related models, views, and templates
* `smartscout/`: contains the main project settings and configuration
* `static/`: contains static files, including CSS, JavaScript, and images
* `templates/`: contains HTML templates for the application

## Usage
To use the main features of the application, follow these steps:
1. Register as an employee or manager
2. Log in to the application
3. As an employee, you can view job postings, apply for jobs, and manage your profile
4. As a manager, you can create job postings, manage applications, and assign projects to employees

## API
The application has several API endpoints for managing data:
### Home
- **URL:** `/`
- **Method:** GET
- **Description:** Renders the home page.

### Employee

#### Home
- **URL:** `/employee/`
- **Method:** GET
- **Description:** Renders the employee home page.

#### Create Profile
- **URL:** `/employee/create/`
- **Method:** POST
- **Description:** Creates a new employee profile.

#### Get Jobs
- **URL:** `/employee/jobs/`
- **Method:** GET
- **Description:** Retrieves a list of active job postings.

### Manager

#### Home
- **URL:** `/manager/`
- **Method:** GET
- **Description:** Renders the manager home page.

#### Generate Recruitment Form
- **URL:** `/manager/forms/create/`
- **Method:** POST
- **Description:** Creates a new recruitment form.

#### Get Recruitment Forms
- **URL:** `/manager/forms/`
- **Method:** GET
- **Description:** Retrieves a list of recruitment forms.

### Admin

#### Home
- **URL:** `/myadmin/`
- **Method:** GET
- **Description:** Renders the admin home page.

#### Manage Managers
- **URL:** `/myadmin/manage_managers/`
- **Method:** GET
- **Description:** Retrieves a list of managers.

### Authentication

#### Register
- **URL:** `/myauth/register/`
- **Method:** POST
- **Description:** Registers a new user.

#### Login
- **URL:** `/myauth/login/`
- **Method:** POST
- **Description:** Authenticates a user.

#### Logout
- **URL:** `/myauth/logout/`
- **Method:** GET
- **Description:** Logs out the current user.

## Contributing
To contribute to the project, follow these steps:
1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make changes and commit them
4. Push the changes to your fork
5. Create a pull request to the main repository

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.