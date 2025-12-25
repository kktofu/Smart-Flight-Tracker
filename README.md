# Smart Flight Tracker

Smart Flight Tracker is a web-based application that allows users to track flight prices automatically.
Users can submit flight search conditions once, and the system will check prices daily and notify users via email when the price drops.

## Features

- Flight price search using Selenium (Google Flights / OTA)
- Daily automated price checking with APScheduler
- Email notification via SendGrid when price drops
- Historical price records stored in database
- Web UI built with Flask & Bootstrap
- One-to-many database design for flights and tickets

## Tech Stack

- Backend: Python, Flask
- Web Automation: Selenium
- Database: SQLite, SQLAlchemy ORM
- Scheduler: APScheduler
- Email Service: SendGrid
- Frontend: HTML, Bootstrap
- Others: WTForms

## System Design Overview

1. User submits flight search conditions via web form
2. Flight data is stored in database
3. Selenium scrapes current flight prices
4. APScheduler runs daily background jobs
5. New prices are compared with historical lowest price
6. Email is sent only when price drops
7. All price records are saved for historical tracking
