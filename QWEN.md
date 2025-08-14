# 1Moment Project Context

## Project Overview

1Moment (also referred to as PhotoZen) is a self-hosted photo and video management solution designed for NAS systems. It allows users to organize, view, and manage their personal photo collections with features like tagging, album creation, and rating.

### Key Features
- Photo upload with drag-and-drop support
- Photo organization with tags and albums
- Photo rating and favorite marking
- Responsive web interface
- WebDAV support for file access
- Docker-based deployment

## Technology Stack

### Backend
- **Framework**: Django 4.2.19 with REST API
- **API Framework**: django-ninja 1.3.0 for OpenAPI documentation
- **Authentication**: django-ninja-jwt for JWT-based authentication
- **Image Processing**: Pillow 9.4.0
- **Database**: SQLite (development), with potential for PostgreSQL/MySQL
- **Web Server**: Gunicorn with gevent workers
- **Task Queue**: Custom implementation (based on file structure)

### Frontend
- **Framework**: Vue 3.5.13 with TypeScript
- **State Management**: Pinia
- **Routing**: vue-router 4.5.0
- **Build Tool**: Vite 6.1.0
- **Styling**: Tailwind CSS 3.4.17 with DaisyUI 4.12.24 component library
- **UI Components**: Heroicons 2.2.0
- **HTTP Client**: Axios 1.8.1

## Project Structure

```
1Moment/
├── moment/                 # Django backend project
│   ├── applications/       # Django apps
│   │   ├── album/          # Album management
│   │   ├── export/         # Export functionality
│   │   ├── file/           # File management
│   │   ├── home/           # Home page
│   │   ├── photos/         # Photo management (core app)
│   │   ├── system/         # System utilities
│   │   ├── users/          # User management
│   │   └── webdav/         # WebDAV implementation
│   ├── components/         # Shared components
│   ├── media/              # Media files (uploaded photos)
│   ├── moment/             # Django project settings
│   ├── recycle/            # Recycle bin for deleted files
│   ├── templates/          # Django templates
│   └── manage.py           # Django management script
├── web/                    # Vue 3 frontend project
│   ├── public/             # Static assets
│   ├── src/                # Source code
│   │   ├── api/            # API clients
│   │   ├── components/     # Vue components
│   │   ├── router/         # Vue router configuration
│   │   ├── stores/         # Pinia stores
│   │   ├── views/          # Page components
│   │   ├── App.vue         # Root component
│   │   └── main.ts         # Entry point
│   ├── index.html          # HTML template
│   ├── package.json        # Frontend dependencies
│   ├── tailwind.config.js  # Tailwind CSS configuration
│   └── vite.config.ts      # Vite configuration
├── compose/                # Docker configurations
│   └── django/             # Django Docker setup
├── requirements/           # Python dependencies
└── README.md               # Project documentation
```

## Backend Architecture

### Django Apps
1. **photos** - Core photo management functionality
2. **album** - Album creation and management
3. **users** - User authentication and management
4. **webdav** - WebDAV protocol implementation
5. **file** - File system operations
6. **export** - Export functionality
7. **home** - Home page and dashboard
8. **system** - System-level utilities

### Data Models
- **Photo**: Represents a photo with metadata, file paths, dimensions, etc.
- **Tag**: Tags for categorizing photos
- **Location**: Geolocation data for photos
- **PhotoRating**: User ratings for photos
- **Album**: Collections of photos

### API Endpoints
The backend uses django-ninja to provide a REST API with the following key endpoints:
- `/api/photos/` - Photo management (list, upload, update, delete)
- `/api/albums/` - Album management
- `/api/tags/` - Tag management
- `/api/users/` - User management
- `/api/fsdav/` - File system WebDAV
- `/api/dbdav/` - Database WebDAV

## Frontend Architecture

### Routing
The Vue frontend uses vue-router with the following main routes:
- `/` - Home page with latest photos
- `/login` - Authentication page
- `/photos` - Photo gallery view
- `/photos/:id/edit` - Photo editing
- `/upload` - Photo upload page
- `/albums` - Album list
- `/albums/:id` - Album detail view
- `/tags` - Tag management
- `/file` - File browser
- `/expore` - Explore view

### State Management
Uses Pinia for state management with stores for:
- Authentication (`auth.ts`)
- Photo data (`photos.ts`)
- UI state (`ui.ts`)

### API Integration
API calls are made through Axios with:
- Base URL configured to `/api`
- Request interceptor for JWT token handling
- Response interceptor for error handling
- Proxy configuration in Vite for development

## Development Workflow

### Backend Development
1. Navigate to the `moment` directory
2. Run Django development server: `python manage.py runserver`
3. Run migrations: `python manage.py migrate`
4. Create new migrations: `python manage.py makemigrations`

### Frontend Development
1. Navigate to the `web` directory
2. Install dependencies: `npm install`
3. Start development server: `npm run dev`
4. Build for production: `npm run build`

### Code Organization
- Backend follows Django's MTV (Model-Template-View) pattern
- Frontend follows component-based architecture with Vue 3 Composition API
- TypeScript is used throughout the frontend for type safety
- Tailwind CSS is used for styling with utility-first approach

## Deployment

### Docker
The project includes Docker configuration for deployment:
- Dockerfile for ARM64 architecture
- Docker Compose configuration
- Gunicorn with gevent workers for production serving

### Environment Configuration
- Development settings in `moment/moment/settings.py`
- CORS configured for development with Vue frontend
- Media files stored in `moment/media/` directory

## Development Practices

### Code Style
- Backend: Python with Django conventions
- Frontend: TypeScript with Vue 3 Composition API
- Styling: Tailwind CSS utility classes
- Formatting: Prettier for frontend code

### Testing
- Backend: Django's built-in testing framework
- Frontend: Vue Test Utils (implied by project structure)

### Linting
- Backend: Python linting (implied)
- Frontend: ESLint with Vue plugin

## Common Development Tasks

### Adding a New Feature
1. Create a new Django app if needed: `python manage.py startapp newfeature`
2. Define models in `models.py`
3. Create API controllers in `controllers.py`
4. Register routes in `moment/api.py`
5. Create Vue components in `web/src/components/`
6. Add routes in `web/src/router/`
7. Create API clients in `web/src/api/`

### Running the Application
1. Backend: `cd moment && python manage.py runserver`
2. Frontend: `cd web && npm run dev`

### Building for Production
1. Backend: Dockerized with Gunicorn
2. Frontend: `cd web && npm run build`

## Project Status

Based on the README, the project has:
- ✅ Backend framework implemented
- ✅ Frontend framework implemented
- ✅ Core photo management features
- ✅ Photo upload with drag-and-drop
- ✅ Photo grid display with lazy loading
- ⏳ Features in development:
  - User authentication system
  - Photo editing functionality
  - Photo search functionality
  - EXIF information display
  - Geolocation display
  - Batch operations
  - Sharing functionality

  # 用中文回答