from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, Boolean, String, DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi.responses import FileResponse
from datetime import datetime


api_app = FastAPI(
    title="Your FastAPI App",
    description="Your FastAPI app description",
    version="0.1",
    templates="templates"  # Specify the location of the templates directory
)

# Allow all origins for demonstration purposes.
api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# adding the relative path
DATABASE_URL = "sqlite:///./Users.db"
engine_users = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

id_request = 0


def Id_request():
    global id_request
    id_request += 1
    return id_request


Base = declarative_base()
SessionLocalUsers = sessionmaker(autocommit=False, autoflush=False, bind=engine_users)


@asynccontextmanager
async def lifespan(api_app: FastAPI):
    Base.metadata.create_all(bind=engine_users)
    yield


def get_db():
    def dependcy():
        db = SessionLocalUsers()
        try:
            yield db
        finally:
            db.close()

    return dependcy

class LastUsedID(Base):
    __tablename__ = 'last_used_id'
    id = Column(Integer, primary_key=True)
    last_id = Column(Integer)
def get_last_used_id():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_users)
    db = SessionLocal()

    # Check if there's an existing record
    last_id_record = db.query(LastUsedID).first()

    if last_id_record:
        last_id = last_id_record.last_id
    else:
        # If no record exists, initialize with 1
        last_id = 1
        last_id_record = LastUsedID(last_id=last_id)
        db.add(last_id_record)
        db.commit()

    # Increment and update the last used ID
    last_id += 1
    last_id_record.last_id = last_id
    db.commit()

    return last_id
class User(Base):
    __tablename__ = "Users"
    First_name = Column(String)
    Last_name = Column(String)
    Email = Column(String, primary_key=True, unique=True, index=True)
    created_at = Column(DateTime, default=func.now())
    Password = Column(String, nullable=True)
    Address = Column(String)
    City = Column(String)
    Age = Column(Integer)
    Last_login = Column(DateTime)
    Proficiency = Column(String)
    Role = Column(String, index=True)
    IsBlocked = Column(Boolean, default=False)



class Request(Base):
    __tablename__ = "Request"
    id_request = Column(Integer, primary_key=True, default=get_last_used_id())
    Email_asker = Column(Integer, ForeignKey("Users.Email"))
    First_name = Column(String, ForeignKey("Users.First_name"))
    Last_name = Column(String, ForeignKey("Users.Last_name"))
    Information = Column(String)
    created_at = Column(DateTime, default=func.now())
    Is_Aprroved = Column(Boolean, default=False)
    Availability = Column(DateTime)
    Additional_Requests = Column(String)
    City = Column(String)


def email_in_db(email: str, db: Session):
    return db.query(User).filter(User.Email == email).first() is not None


@api_app.post("/add_user")
async def AddUser(user_data: dict, db: Session = Depends(get_db())):
    print("addUser activate")
    First_name = user_data.get("First_name")
    Last_name = user_data.get("Last_name")
    Email = user_data.get("Email")
    Password = user_data.get("Password")
    City = user_data.get("City")
    Age = user_data.get("Age")
    Proficiency = user_data.get("Proficiency")
    Role = user_data.get("Role")
    Last_login = func.now()

    if email_in_db(Email, db):
        raise HTTPException(status_code=400, detail="The email is already existing")

    new_user = User(First_name=First_name, Last_name=Last_name, Email=Email, Password=Password,
                    City=City, Age=Age, Proficiency=Proficiency, Role=Role, Last_login=Last_login)
    db.add(new_user)
    db.commit()

    return {"message": "User added successfully"}


@api_app.post('/Add_Request')
def add_request(request_data: dict, db: Session = Depends(get_db())):
    try:
        required_keys = ['name', 'city', 'problem', 'additionalRequests']
        if not all(key in request_data for key in required_keys):
            raise HTTPException(status_code=400, detail='Invalid request data')
        # Access the data using the request_data dictionary
        problem = request_data.get('problem')
        datetime = request_data.get('datetime')
        additional_requests = request_data.get('additionalRequests')
        #availability_datetime = datetime.strptime((datetime), '%Y-%m-%dT%H:%M:%S')
        #availability_datetime = [datetime.split("T")]
        availability_datetime = func.now()


        # Perform any additional processing or database operations here
        new_request = Request(Email_asker="mosesberco1@gmail.com", First_name="moses", Last_name="berco",
                              Information=problem, Availability=availability_datetime, City="Beersheva",
                              Additional_Requests=additional_requests)
        db.add(new_request)
        db.commit()
        print(new_request)
        # Return a response (optional)
        response = {'status': 'success', 'message': 'Request added successfully'}
        print("request added successfully")
        print(new_request)
        return response


    except Exception as e:
    #Handle exceptions and return an appropriate error response
        db.rollback()
        raise HTTPException(status_code=500, detail=f'Internal Server Error: {str(e)}')


app = FastAPI(title="main app", lifespan=lifespan)
html_path = Path(__file__).parent / "templates" / "login.html"
app.mount("/api", api_app)
app.mount("/", StaticFiles(directory="templates", html=True), name="templates")


@api_app.post('/BlockUser')
def BlockUser(email: str, db: Session = Depends(get_db())):
    user_to_block = db.query(User).filter(User.Email == email).first()
    if user_to_block is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_to_block.IsBlocked = True
    return JSONResponse({'message': 'User Blocked Succesfully !'})


@api_app.post('/LogIn')
def LogIn(user: dict, db: Session = Depends(get_db())):
    userlogin = db.query(User).filter(User.Email == user.get("Email")).first()
    if userlogin is None:
        raise HTTPException(status_code=404, detail="Sorry, we don't recognize this email.")
    if userlogin.Password == user.get("Password"):
        return JSONResponse({'message': 'Logging in...', 'nexturl': '!!!URLHOMEPAGE!!!.html'})


@app.get("/login")
async def read_login():
    return FileResponse(html_path, media_type="text/html")


# added code by Ariel - Check over it.
# func to get user's name and city to fetch it in JS.
@app.get("/api/user")
def get_user(user: dict, db: Session = Depends(get_db())):
    return {
        "name": user.get("First_name"),
        "city": user.get("City")
    }


# until to here...

if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
