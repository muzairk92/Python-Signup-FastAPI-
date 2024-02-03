# Python-Signup-FastAPI-

This repository contains example code for adding a signup feature to a FastAPI application with React frontend.

**#Key Features**
Backend API built with FastAPI framework and Python
PostgreSQL database for storing user accounts
Password hashing and authentication using JWT tokens
React frontend with TypeScript
Fetching and storing JWT token on client side
CSRF protection via synchronizer token pattern
Security
User passwords are hashed with bcrypt before storing in database
CSRF protection implemented via tokens to prevent forged requests
Rate limiting on signup endpoint to deter brute force attacks
API Endpoints
POST /signup - Register a new user account

Running Locally
Instructions for installing dependencies and running the application locally
