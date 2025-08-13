# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

1Moment is a NAS photo management application with a Django REST API backend and Vue 3 frontend. It provides photo upload, organization, album management, and WebDAV support for personal photo collections.

## Architecture

### Backend (Django)
- **Framework**: Django 4.2.19 with django-ninja for REST APIs
- **Database**: SQLite (development), configured for production databases
- **Authentication**: django-ninja-jwt with sliding tokens (5-day lifetime)
- **File Processing**: Pillow for image processing with automatic thumbnail generation
- **API Discovery**: Uses `api.auto_discover_controllers()` to automatically register all controllers

### Frontend (Vue 3)
- **Framework**: Vue 3.5.13 with Composition API and TypeScript
- **Build Tool**: Vite 6.1.0 with Vue devtools plugin
- **Styling**: Tailwind CSS 3.4.17 + DaisyUI 4.12.24
- **State Management**: Pinia for global state
- **HTTP Client**: Axios with interceptors for error handling
- **Development Server**: Runs on port 5173 with CORS proxy to Django

## Development Commands

### Frontend (from /web directory)
```bash
npm run dev          # Start development server (port 5173)
npm run build        # Build for production (runs type-check + build-only)
npm run type-check   # TypeScript type checking with vue-tsc
npm run lint         # ESLint with auto-fix
npm run format       # Prettier code formatting
npm run preview      # Preview production build
```

### Backend (from /moment directory)
```bash
python manage.py runserver         # Start Django development server
python manage.py migrate          # Run database migrations
python manage.py makemigrations   # Create new migrations
python manage.py collectstatic    # Collect static files
python manage.py createsuperuser  # Create admin user
```

## Key Application Structure

### Django Applications
- `applications/photos/` - Photo upload, management, and thumbnail generation
- `applications/album/` - Photo album organization and management
- `applications/users/` - User authentication and profile management
- `applications/webdav/` - WebDAV server implementation for external client access
- `applications/file/` - File system operations and management
- `applications/home/` - Dashboard and homepage content

### API Controllers
Controllers are auto-discovered and registered. Key endpoints:
- `/api/photos/` - Photo CRUD operations and upload
- `/api/albums/` - Album management
- `/api/tags/` - Photo tagging system
- `/api/fsdav/` - WebDAV filesystem access
- `/api/dbdav/` - WebDAV database access

### Frontend Structure
- `src/api/` - Axios-based API client modules
- `src/components/` - Reusable Vue components (PhotoGrid, PhotoUpload, etc.)
- `src/views/` - Page-level components organized by feature
- `src/stores/` - Pinia stores for state management
- `src/router/` - Vue Router configuration

## Development Setup

### Frontend Dependencies
Development requires Node.js. Key dependencies are managed through npm:
- Vue 3 ecosystem (vue-router, pinia)
- TypeScript toolchain (vue-tsc, @vue/eslint-config-typescript)
- Styling framework (tailwindcss, daisyui, @heroicons/vue)

### Backend Dependencies
Python dependencies are in `requirements/base.txt`. Key packages:
- Django + django-ninja for API development
- Pillow for image processing
- lxml for XML processing (WebDAV)
- gunicorn + gevent for production deployment

### CORS Configuration
Frontend dev server (5173) is whitelisted in Django CORS settings. CSRF tokens are configured for cross-origin requests.

## File Upload & Media Handling

Photos are processed with automatic thumbnail generation in multiple sizes. Media files are stored in `/moment/media/` with organized directory structure. The recycle bin feature moves deleted photos to `/moment/recycle/` for recovery.

## Docker Deployment

The project includes Docker configuration in `compose/django/` with:
- Multi-architecture support (Dockerfile + Dockerfilearm)
- Docker Compose setup for production deployment
- Build script: `./build-docker.sh`