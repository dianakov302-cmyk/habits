# Anaida Space

**Anaida Space** is a digital sanctuary and self-development platform designed to bridge the gap between inspiration and action. The project utilizes a minimalist, atmospheric aesthetic to create a focused environment for personal growth and mental clarity.

## Project Structure

The project consists of 2 main modules:
1. **Backend (FastAPI)**: Handles user authentication, goal tracking, and progress management. Can be extended to include more advanced tracking features and AI-driven insights.
2. **Frontend (HTML/CSS/JS)**: A thoughtfully designed, modern interface utilizing an immersive, dark-themed aesthetic with glassmorphism to provide a distraction-free user experience.

## Core Functionality

The platform is structured as an interactive journey toward self-improvement. Key features include:

- **Guided Progression**: A curated path or curriculum for users to follow (e.g., "Start Your Journey").
- **Educational Content**: Dedicated sections (like "Motivation vs Discipline") indicating a focus on psychology and habit-building.
- **Reflective Space**: The inclusion of typewriter imagery and prompts suggests a journaling or writing component where users can externalize their thoughts.
- **The "Break the Circle" Framework**: A core module aimed at identifying and disrupting repetitive negative patterns or "cycles" in the user's life.

## The Problem It Solves

Anaida Space addresses several modern psychological pain points:

- **The "Motivation Trap"**: Solving the issue of people waiting for "feeling motivated" before taking action, by teaching the mechanics of discipline.
- **Information Overload**: By using a dark, minimalist UI, it solves the problem of digital overstimulation, providing a "quiet" space for deep work and thought.
- **Stagnation**: It targets the "loop" of bad habits (the "circle") that prevents individuals from moving forward in their personal or professional lives.

## Target Audience

This project is designed for high-performers, creatives, and seekers who feel "stuck." Specifically:

- **Procrastinators**: Those who struggle to turn their ideas into reality and need a structured framework to build discipline.
- **Mindfulness Seekers**: Individuals looking for a sophisticated, aesthetic environment to practice self-reflection away from noisy social media.
- **Self-Developers**: People interested in cognitive behavioral shifts—those who want to "break the circle" of their current lifestyle to reach a new level of efficiency.

## Getting Started

### Prerequisites
- Python 3.x
- `pip` package manager

### Installation & Execution

1. **Install backend dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. **Run the backend server**:
   ```bash
   uvicorn backend.main:app --reload
   ```

3. **Access the Application**:
   - **Frontend App**: The modern UI can be accessed via the static files served by the app (e.g., `http://127.0.0.1:8000/static/index.html` or similar).
   - **API Documentation (Swagger UI)**: `http://127.0.0.1:8000/docs`
   - **API Documentation (ReDoc)**: `http://127.0.0.1:8000/redoc`
   - **Healthcheck**: `http://127.0.0.1:8000/health`
