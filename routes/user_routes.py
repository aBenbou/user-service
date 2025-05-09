from flask import Blueprint, request, jsonify
from models.user import User
from app import db
from ..validators import (
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
    UserProfileList
)
from pydantic import ValidationError
from datetime import datetime

# ... existing code ... 