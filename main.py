from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session

DATABASE_URL = "sqlite:///:Users.db:"
engine_users = create_engine(DATABASE_URL)

Base = declarative_base()
SessionLocalUsers = sessionmaker(autocommit=False, autoflush=False, bind=engine_users)
Base.metadata.create_all(bind=engine_users)

def get_db(db_name):
    if db_name == "Users":
        db = SessionLocalUsers()
        try:
            yield db
        finally:
            db.close()


class User(Base):
    __tablename__ = "Users"
    First_name = Column(String)
    Last_name = Column(String)
    Email = Column(String,primary_key=True,unique=True,index=True)
    created_at = Column(DateTime, default=func.now())
    Password = Column(String, nullable=True)
    Address = Column(String)
    City = Column(String)
    Age = Column(Integer)
    Last_login = Column(DateTime)
    Proficiency = Column(String)
    Role = Column(String, index=True)


def email_in_db(email: str, db: Session):
    return db.query(User).filter(User.Email == email).first() is not None


def AddUser(user_data: dict, db: Session = Depends(get_db("Users"))):
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


