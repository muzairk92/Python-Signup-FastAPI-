# Import necessary libraries
from fastapi import FastAPI, Depends, HTTPException, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from datetime import datetime
import bcrypt
import secrets
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = "postgresql://username:password@localhost/DB name"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy base model
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    last_login = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    role = Column(String(50), default='user')

# Create all tables in the database (if not already existing)
Base.metadata.create_all(bind=engine)

# FastAPI application instance
app = FastAPI()

# Function to check database connectivity
def check_database_connection():
    try:
        # Attempt to connect to the database
        with engine.connect() as connection:
            # Optional: Perform a test query if necessary (e.g., SELECT 1)
            # connection.execute("SELECT 1")
            pass  # If connection is successful, pass without doing anything
        print("DB Connected!")
        print("*" * 80)
        print("*" + " " * 78 + "*")
        print("*" + " " * 30 + "DB Connected!" + " " * 31 + "*")
        print("*" + " " * 78 + "*")
        print("*" * 80)
    except SQLAlchemyError as e:
        # Handle database connection error
        print(f"DB Connection Error: {e}")
        exit()


# CORS middleware configuration
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CSRF protection middleware
async def csrf_protect(request: Request, call_next):
    if request.method in ["POST", "PUT", "DELETE"]:
        # Retrieve CSRF token from cookies and headers
        session_token = request.cookies.get("csrf_token")
        request_token = request.headers.get("X-CSRF-Token")

        # Verify CSRF token match
        if not session_token or not request_token or session_token != request_token:
            return JSONResponse(status_code=403, content={"detail": "CSRF token mismatch"})

    # Proceed with the request if CSRF validation passes
    response = await call_next(request)
    return response

# Apply CSRF protection middleware to the application
app.middleware("http")(csrf_protect)

# Pydantic model for signup requests
class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

# Endpoint for user signup
@app.post("/signup")
def signup(signup_data: SignupRequest, db: Session = Depends(get_db)):
    # Hash the user's password
    hashed_password = bcrypt.hashpw(signup_data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Create a new user instance and add it to the database
    new_user = User(name=signup_data.name, email=signup_data.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Signup successful"}

# Endpoint to obtain a CSRF token
@app.get("/csrf-token")
def get_csrf_token(response: Response):
    # Generate a CSRF token and set it in a cookie
    token = secrets.token_urlsafe(32)
    response.set_cookie(key="csrf_token", value=token, httponly=True, secure=False, samesite='Lax')
    return {"csrf_token": token}
    
    
# Include the database connection check in the main block
if __name__ == "__main__":
    # Check database connection before starting the application
    check_database_connection()
    
    # If the check passes, run the application
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)