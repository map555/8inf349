import os
from datetime import datetime

from peewee import DoesNotExist
from flask import Flask, request, redirect, url_for, abort

def create_app(initial_config=None):
    app=Flask("8inf439")
    init_app(app)