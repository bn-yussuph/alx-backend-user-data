#!/usr/bin/env python3
"""
Route module for the API
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def simple_data() -> str:
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    msg = {"email": email, "message": "user created"}
    return jsonify(msg)


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ Login a valid user
    Args: email and password
    Return: success nessage
    """
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)
    valid_login = AUTH.valid_login(email, password)

    if valid_login:
        ses = AUTH.create_session(email)
        msg = {"email": email, "message": "logged in"}
        res = jsonify(msg)
        res.set_cookie("session_id", ses)
        return res
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ Delete /session
        Finds a user and delete hisbsession
    """
    cookie = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(cookie)
    if cookie is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """ Retur the profile of the logged in user
        /profile GET
    """
    cookie = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(cookie)
    if cookie is None or user is None:
        abort(403)
    msg = {"email": user.email}
    return jsonify(msg), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """ Route for password reset
        /reset_password POST
    """
    try:
        email = request.form['email']
    except KeyError:
        abort(403)
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    msg = {"email": email, "reset_token": reset_token}
    return jsonify(msg), 200


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """ Reset a password
    Takes a new paswword and a new password,
    then reset the old one
    """
    try:
        email = request.form['email']
        token = request.form['reset_token']
        new_pw = request.form['new_password']
    except KeyError:
        abort(400)
    try:
        AUTH.update_password(token, new_pw)
    except ValueError:
        abort(403)
    msg = {"email": email, "message": "Passwrd updated"}
    return jsonify(msg), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
