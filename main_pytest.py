import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from sqlalchemy import func
import main
from main import User, Request, Rating, Thread
from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path

@pytest.fixture
def db():
    db = MagicMock(spec=Session)
    yield db

def test_email_in_db_exists(db):
    # Test case when email exists in the database
    db.query(User).filter.return_value.first.return_value = User(Email="udivak9@gmail.com")
    result = main.email_in_db("udivak9@gmail.com", db)
    assert result is True

def test_email_in_db_does_not_exist(db):
    # Test case when email does not exist in the database
    db.query(User).filter.return_value.first.return_value = None
    result = main.email_in_db("test@example.com", db)
    assert result is False

def test_add_review_id_exists(db: Session):
    # Given
    request_id = 1
    rating = 5
    comment = "Nice work!"
    new_review = Rating(request_id=request_id, rating=rating, comment=comment)
    db.query(Rating).filter.return_value.first.return_value = new_review

    # When
    response = main.add_review({"request_id": request_id, "stars": rating, "comment": comment}, db)

    # Then
    assert response == {"message": "review added successfully"}
    review = db.query(Rating).filter(Rating.request_id == request_id).first()
    assert review is not None
    assert review.rating == rating
    assert review.comment == comment

def test_add_review_bad_data(db: Session):
    # Given
    invalid_request_id = "invalid"
    rating = 5
    comment = "Great request!"

    # Calling to add_review
    response = main.add_review({"request_id": invalid_request_id, "stars": rating, "comment": comment}, db)

    # Then
    assert response == {"message": "invalid request ID"}
    review = db.query(Rating).filter(Rating.request_id == invalid_request_id).first()
    assert review.request_id is not int

def test_add_user_email_exists(db: Session):
    # Given an existing user email
    test_user_data = {
        "First_name": "Test",
        "Last_name": "User",
        "Email": "udivak9@gmail.com",
        "Password": "password456",
        "City": "New York",
        "Age": 30,
        "Proficiency": "chef",
        "Role": "volunteer",
    }

    # Calling AddUser with existing email in db
    main.AddUser(test_user_data, db)

    user = db.query(User).filter(User.Email == test_user_data["Email"]).first()
    # Then
    assert user.First_name is not "Test"
    assert user.Last_name is not "User"
    assert user.Password is not "password456"
    assert user.City is not "New York"
    assert user.Age is not 30
    assert user.Proficiency is not "chef"
    assert user.Role is not "volunteer"

def test_change_request_to_done(db: Session):
    # Given an existing request_id
    request_id = 1
    request = db.query(Request).filter(Request.id_Request == request_id).first()

    #Calling to change_request_to_done
    response = main.change_request_to_done(request.id_Request, db)

    # Then
    assert response == {"message": "request done successfully"}

def test_change_request_to_done_fail(db: Session):
    # Given a not existing request_id
    request_id = -1
    request = db.query(Request).filter(Request.id_Request == request_id).first()

    #Calling to change_request_to_done
    response = main.change_request_to_done(request.id_Request, db)

    # Then
    assert response is not {"message": "request done successfully"}

def test_get_user_requests(db: Session):
    # Given an existing user email
    response = main.get_user_requests("udivak9@gmail.com")

    # Then
    assert type(response) is list

def test_get_user_requests_fail(db: Session):
    # Given a not existing user email
    response = main.get_user_requests("notexist@fail.com")

    # Then
    assert len(response) is 0

def test_ownerless_requests(db: Session):
    # Given a not existing user email
    response = main.ownerless_requests()

    # Then
    assert type(response) is list

def test_avg_rating(db: Session):
    # Given a not existing user email
    response = main.avg_rating()

    # Then
    assert type(response) is dict

def test_approve_request(db: Session):
    # Given an existing request_id
    request_id = 1
    request = db.query(Request).filter(Request.id_Request == request_id).first()
    # Calling to change_request_to_done
    response = main.approve_request(request.id_Request, db)

    # Then
    assert response == {"message": "aprroved successfully"}

def test_approve_request_fail(db: Session):
    # Given a not existing request_id
    request_id = -1
    request = db.query(Request).filter(Request.id_Request == request_id).first()
    # Calling to change_request_to_done
    response = main.approve_request(request.id_Request, db)

    # Then
    assert response is not {"message": "aprroved successfully"}

def test_connect_request_test(db: Session):
    # Given existing data in db :
    data = {"user_email": "udivak9@gmail.com", "request_id": 1}

    response = main.connect_request(data, db)

    assert response == {"message": "connecting successfully"}

def test_connect_request_test_fail(db: Session):
    # Given not existing data in db :
    data = {"user_email": "notexist@fail.com", "request_id": -1}

    response = main.connect_request(data, db)

    assert response is not {"message": "connecting successfully"}

def test_deny_request_test(db: Session):
    # Given existing data in db :
    request_id = 1

    response = main.deny_request(request_id, db)

    assert response == {"message": "Request denied and removed successfully"}

def test_deny_request_test_fail(db: Session):
    # Given not existing data in db :
    request_id = -1

    response = main.deny_request(request_id, db)

    assert response is not {"message": "Request denied and removed successfully"}

def test_create_new_thread(db: Session):
    # Creating new Thread instance
    new_thread_data = {"id_tread": 100, "information": "information", "Created_at": 2024, "isThread": 1,"owner": "owner","email": "email","role": "role"}

    response = main.create_new_thread(new_thread_data, db)

    assert response.get("message") == "Thread added successfully"

def test_create_new_thread_fail(db: Session):
    # Creating new Thread instance with corrupted data
    new_thread_data = {"information": "information"}

    response = main.create_new_thread(new_thread_data, db)

    assert response.get("message") is not "Thread added successfully"

def test_get_approved_requests():
    # check
    response = main.get_approved_requests()

    assert type(response) is list


def test_get_users_list():
    # check
    response = main.get_users_list()

    assert type(response) is list


def test_get_unapproved_requests(db: Session):
    # check
    response = main.get_unapproved_requests()

    assert type(response) is list



def test_BlockUser(db: Session):
    # Given existing user's email in db
    data = {"email": "udivak9@gmail.com"}

    response = main.BlockUser(data, db)

    assert type(response) is JSONResponse


def test_get_user_info_fail(db: Session):
    # Given not existing email in db
    email = "notexist@fail.com"

    response = main.get_user_info(email, db)

    assert type(response) is not dict

def test_forgot_password_fail(db: Session):
    # Given not existing email in db
    email = "notexist@fail.com"

    response = main.get_user_info(email, db)

    assert type(response) is not dict
