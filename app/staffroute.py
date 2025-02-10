from flask import Flask, url_for, redirect, Blueprint, session

staff = Blueprint("staff", __name__,template_folder='templates/staff')


