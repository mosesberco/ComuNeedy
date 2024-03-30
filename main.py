from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, Boolean, String, DateTime, Sequence, func
from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi.responses import FileResponse

id_Request = 0


def mydefault_id_Request():
    global id_Request
    id_Request += 1
    return id_Request


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
DATABASE_User_URL = "sqlite:///Users.db"
# DATABASE_Request_URL = "sqlite:///Request.db"
engine_users = create_engine(DATABASE_User_URL, connect_args={"check_same_thread": False})
# engine_requests = create_engine(DATABASE_Request_URL, connect_args={"check_same_thread": False})

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_users)


# SessionLocalRequests = sessionmaker(autocommit=False, autoflush=False, bind=engine_requests)


@asynccontextmanager
async def lifespan(api_app: FastAPI):
    Base.metadata.create_all(bind=engine_users)
    # Base.metadata.create_all(bind=engine_requests)
    yield


def get_db():
    def dependcy():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    return dependcy


'''def get_db_requests():
    def dependcy():
        db = SessionLocalRequests()
        try:
            yield db
        finally:
            db.close()

    return dependcy'''


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


class Thread(Base):
    __tablename__ = "treads"
    id_tread = Column(Integer, primary_key=True, autoincrement=True)
    information = Column(String, default=None)
    Created_at = Column(DateTime, default=func.now())
    isThread = Column(Boolean)
    owner = Column(String)
    email = Column(String)
    role = Column(String)
    connect_to = Column(Integer, default=0)


class Request(Base):
    __tablename__ = "Request"
    id_Request = Column(Integer, primary_key=True, autoincrement=True)
    First_name = Column(String, default=None)
    Last_name = Column(String, default=None)
    Information = Column(String, default=None)
    ##Availability = Column(DateTime, default=None)
    Availability = Column(String, default=None)
    Additional_Req = Column(String, default=None)
    City = Column(String, default=None)
    user_email = Column(String, ForeignKey('Users.Email'))
    Created_at = Column(DateTime, default=func.now())
    Is_approved = Column(Boolean, default=False)
    connect_to = Column(String, default=None)
    # user = relationship("User", back_populates="requests")
    is_Done = Column(Boolean, default=False)


def email_in_db(email: str, db: Session = Depends(get_db())):
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


@api_app.put("/complete_request/{request_id}")
def change_request_to_done(request_id: int, db: Session = Depends(get_db())):
    request = db.query(User).filter(Request.id_Request == request_id).first()
    request.is_Done = True
    db.commit()
    return {"message": "request done successfully"}


@api_app.get("/My_request/{user_email}")
def get_user_requests(user_email: str):
    session = SessionLocal()
    try:
        MyRequests = session.query(Request).filter(Request.connect_to == user_email).all()
        requests_data = []
        for request in MyRequests:
            request_dict = {
                'id_Request': request.id_Request,
                'First_name': request.First_name,
                'Last_name': request.Last_name,
                'Information': request.Information,
                'Availability': request.Availability,
                'Additional_Req': request.Additional_Req,
                'City': request.City,
                'user_email': request.user_email,
                'Created_at': str(request.Created_at)
            }
            requests_data.append(request_dict)
        return requests_data

    finally:
        session.close()


@api_app.get("/ownerless_requests")
def ownerless_requests():
    session = SessionLocal()
    try:
        # Query to fetch unapproved requests
        ownerless_request = session.query(Request).filter(Request.connect_to == 0).all()

        # Convert the requests to a list of dictionaries
        requests_data = []
        for request in ownerless_request:
            request_dict = {
                'id_Request': request.id_Request,
                'First_name': request.First_name,
                'Last_name': request.Last_name,
                'Information': request.Information,
                'Availability': request.Availability,
                'Additional_Req': request.Additional_Req,
                'City': request.City,
                'user_email': request.user_email,
                'Created_at': str(request.Created_at)
            }
            requests_data.append(request_dict)

        return requests_data
    finally:
        session.close()


@api_app.put("/approve_request/{request_id}", )
def approve_request(request_id: int, db: Session = Depends(get_db())):
    request = db.query(User).filter(Request.id_Request == request_id).first()
    print(request)
    if request is None:
        raise HTTPException(status_code=404, detail=f"Request with ID {request_id} not found")
    request.Is_approved = True
    db.commit()
    # db.refresh(request)
    return {"message": "aprroved successfully"}


@api_app.put("/connecting_request_to_user/", )
def connect_request(data: dict, db: Session = Depends(get_db())):
    request = db.query(Request).filter(Request.id_Request == data.get("request_id")).first()
    request.connect_to = data.get("user_email")
    db.commit()
    return {"message": "connecting successfully"}


@api_app.delete("/deny_request/{request_id}", )
def deny_request(request_id: int, db: Session = Depends(get_db())):
    request = db.query(Request).filter(Request.id_Request == request_id).first()
    if request is None:
        raise HTTPException(status_code=404, detail=f"Request with ID {request_id} not found")
    db.delete(request)
    db.commit()
    return {"message": "Request denied and removed successfully"}


@api_app.post('/new_thread')
def create_new_thread(thread_data: dict, db: Session = Depends(get_db())):
    if 'id' in thread_data and 'isthread' in thread_data:
        new_thread = Thread(owner=thread_data.get('owner'), information=thread_data.get('thread'),
                            email=thread_data.get('email'), role=thread_data.get('role'),
                            connect_to=thread_data.get('id'), isThread=thread_data.get('isthread'))
    else:
        new_thread = Thread(owner=thread_data.get('owner'), information=thread_data.get('thread'), isThread=True,
                            email=thread_data.get('email'), role=thread_data.get('role'))
    db.add(new_thread)
    db.commit()
    return ({"message": "Thread added successfully", "id": new_thread.id_tread})


@api_app.get('/approved_requests')
def get_approved_requests():
    session = SessionLocal()
    try:
        # Query to fetch unapproved requests
        approved_requests = session.query(Request).filter(Request.Is_approved == True).all()

        # Convert the requests to a list of dictionaries
        requests_data = []
        for request in approved_requests:
            request_dict = {
                'id_Request': request.id_Request,
                'First_name': request.First_name,
                'Last_name': request.Last_name,
                'Information': request.Information,
                'Availability': request.Availability,
                'Additional_Req': request.Additional_Req,
                'City': request.City,
                'user_email': request.user_email,
                'Created_at': str(request.Created_at),
                'Is_approved': request.Is_approved
            }
            requests_data.append(request_dict)

        return requests_data
    finally:
        session.close()


@api_app.get('/users_list')
def get_users_list():
    db = SessionLocal()
    try:
        users_data = db.query(User).filter(User.IsBlocked == False).all()
        users_list = []
        for user in users_data:
            user_dict = {
                "First_name": user.First_name,
                "Last_name": user.Last_name,
                "Email": user.Email,
                "created_at": user.created_at,
                "Address": user.Address,
                "City": user.City,
                "Age": user.Age,
                "Proficiency": user.Proficiency,
                "Role": user.Role
            }
            users_list.append(user_dict)
        return users_list
    finally:
        db.close()


@api_app.get('/unapproved_requests')
def get_unapproved_requests():
    session = SessionLocal()
    try:
        # Query to fetch unapproved requests
        unapproved_requests = session.query(Request).filter(Request.Is_approved == False).all()

        # Convert the requests to a list of dictionaries
        requests_data = []
        for request in unapproved_requests:
            request_dict = {
                'id_Request': request.id_Request,
                'First_name': request.First_name,
                'Last_name': request.Last_name,
                'Information': request.Information,
                'Availability': request.Availability,
                'Additional_Req': request.Additional_Req,
                'City': request.City,
                'user_email': request.user_email,
                'Created_at': str(request.Created_at),
                'Is_approved': request.Is_approved
            }
            requests_data.append(request_dict)

        return requests_data
    finally:
        session.close()


@api_app.post("/change_password")
async def change_user_password(data: dict, db: Session = Depends(get_db())):
    # Fetch user information from the database
    user = db.query(User).filter(User.Email == data.get('email')).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.Password = data.get('password')
    db.commit()

    return JSONResponse({'message': 'Password Changed Successfully !'})


@api_app.post("/new_request")
async def NewRequest(user_data: dict, db: Session = Depends(get_db())):
    user_email = user_data.get("email", "")
    first_name = user_data.get("name", "")
    last_name = user_data.get("last_name", "")
    city = user_data.get("city", "")
    information = user_data.get("Information", "")
    availability = user_data.get("Availability", "")
    additional_Req = user_data.get("Additional_Req", "")
    new_request = Request(First_name=first_name, Last_name=last_name, City=city, Information=information,
                          Availability=availability, Additional_Req=additional_Req, user_email=user_email, connect_to=0)
    db.add(new_request)
    db.commit()
    return {"message": "Request added successfully"}


app = FastAPI(title="main app", lifespan=lifespan)
html_path = Path(__file__).parent / "templates" / "index.html"
app.mount("/api", api_app)
app.mount("/", StaticFiles(directory="templates", html=True), name="templates")


@api_app.post("/BlockUser,{email}")
def BlockUser(email: str, db: Session = Depends(get_db())):
    user_to_block = db.query(User).filter(User.Email == email).first()
    if user_to_block is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_to_block.IsBlocked = True
    return JSONResponse({'message': 'User Blocked Succesfully !'})


@api_app.post('/login')
def LogIn(user: dict, db: Session = Depends(get_db())):
    userlogin = db.query(User).filter(User.Email == user.get("Email")).first()
    if userlogin is None:
        raise HTTPException(status_code=404, detail="Sorry, we don't recognize this email.")
    if userlogin.Password == user.get("Password"):
        userlogin.Last_login = func.now()
        user_details = {
            "message": "Logging in...",
            "nexturl": "Genrator.html",
            "user": {
                "email": userlogin.Email,
                "name": userlogin.First_name,
                "last_name": userlogin.Last_name,
                "city": userlogin.City,
                "role": userlogin.Role,
            }}
        return JSONResponse(user_details)
    else:
        raise HTTPException(status_code=401, detail="Invalid password")


@app.get("/login")
async def read_login():
    html_path = Path(__file__).parent / "templates" / "login.html"
    return FileResponse(html_path, media_type="text/html")


# added code by Ariel - Check over it.
# func to get user's name and city to fetch it in JS.
@app.get("/api/user/")
async def get_user_info(email: str, db: Session = Depends(get_db())):
    # Fetch user information from the database
    user = db.query(User).filter(User.Email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "First_name": user.First_name,
        "Last_name": user.Last_name,
        "City": user.City,
    }


@api_app.post("/forgot_password/{email}")
def forgot_password(email: str, db: Session = Depends(get_db())):
    if db.query(User).filter(User.Email == email):
        print("is ok")
        return {"message": "user found Succesfully"}
    '''else:
        raise HTTPException(status_code=404, detail="User not found")'''


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
