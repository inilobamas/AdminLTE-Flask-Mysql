from flask import render_template, redirect, request, url_for, flash
from . import user
from .forms import SearchForm
from app.models import User
from flask_login import login_required, current_user
import json, datetime

# List User
@user.route('/user', methods=['GET', 'POST'])
@login_required
def functionGetUser():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.select()\
            .where(
                User.username.contains(form.search.data)
                | User.fullname.contains(form.search.data)
                | User.email.contains(form.search.data)
                | User.address.contains(form.search.data)
                | User.phone.contains(form.search.data)
                | User.role.contains(form.search.data)
            )
    else:
        user = User.select().execute()

    return render_template('user/list_user.html', current_user=current_user, len_list=len(user), list_user=user, form=form)

# Get User
@user.route('/getUserByID', methods=['POST'])
@login_required
def functionGetUserByID():
    id = request.form['id']
    # Get User By ID
    user = User.get_by_id(id)

    user_row = {
        "username": user.username,
        "fullname": user.fullname,
        "address": user.address,
        "phone": user.phone,
        "email": user.email,
        "role": user.role
    }

    return user_row

# Insert User (with modal)
@user.route('/insertUser', methods=['GET', 'POST'])
@login_required
def functionInsertUser():
    row = {
        "status": "success",
        "message": "Success"
    }

    username = request.form['username']
    fullname = request.form['fullname']
    address = request.form['address']
    phone = request.form['phone']
    email = request.form['email']
    role = request.form['role']
    password = request.form['password']

    try:
        # Hash password first
        password_hashed = User.generate_password(None, password)
    except Exception as e:
        flash('Error generate password', 'danger')

    try:
        query_user = User.select().where(User.username == username)
        if query_user.exists():
            row['status'] = "danger"
            row['message'] = "Username already exist"
        else:
            try:
                user = User.insert(
                    username=username,
                    password=password_hashed,
                    fullname=fullname,
                    address=address,
                    phone=phone,
                    email=email,
                    role=role,
                    created_by=current_user.id,
                    created_at=datetime.datetime.now()
                ).execute()

                row['status'] = "success"
                row['message'] = "Successfully Inserted"
            except Exception as e:
                row['status'] = "danger"
                row['message'] = "Failed to Insert"
    except Exception as e:
        row['status'] = "danger"
        row['message'] = "Failed to Insert"

    return row


# Update User
@user.route('/updateUser', methods=['GET', 'POST'])
@login_required
def functionUpdateUser():
    row = {
        "status": "success",
        "message": "Success"
    }

    id = request.form['id']
    username = request.form['username']
    fullname = request.form['fullname']
    address = request.form['address']
    phone = request.form['phone']
    email = request.form['email']
    role = request.form['role']

    try:
        query_user = User.get_by_id(id)
        if query_user == None:
            row['status'] = "danger"
            row['message'] = "User not exist"
        else:
            try:
                query_update = User.update(
                    username=username,
                    fullname=fullname,
                    address=address,
                    phone=phone,
                    email=email,
                    role=role,
                    updated_by=current_user.id,
                    updated_at=datetime.datetime.now()
                )
                query_update.where(User.id == id).execute()

                row['status'] = "success"
                row['message'] = "Successfully Updated"
            except Exception as e:
                row['status'] = "danger"
                row['message'] = "Failed to Update"
    except Exception as e:
        row['status'] = "danger"
        row['message'] = "Failed to Update"

    return row


# Delete User
@user.route('/deleteUserByID', methods=['POST'])
@login_required
def functionDeleteUserByID():
    row = {
        "status": "success",
        "message": "Success"
    }

    form = SearchForm()

    id = request.form['id']
    # Delete User By ID
    try:
        User.delete_by_id(id)
        row['status'] = "success"
        row['message'] = "Successfully Deleted"
    except Exception as e:
        row['status'] = "danger"
        row['message'] = "Failed to Delete"

    # Get All User
    user = User.select().execute()

    return render_template('user/list_user.html', current_user=current_user, len_list=len(user), list_user=user, form=form)