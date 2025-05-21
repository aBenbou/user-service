from enum import Enum


class Visibility(str, Enum):
    """Visibility levels for a user profile."""

    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    CONNECTIONS_ONLY = "CONNECTIONS_ONLY"


class ExpertiseLevel(str, Enum):
    """Expertise level types."""

    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    EXPERT = "EXPERT"


class PreferenceCategory(str, Enum):
    """Categories for user preferences."""

    NOTIFICATIONS = "NOTIFICATIONS"
    PRIVACY = "PRIVACY"
    APPEARANCE = "APPEARANCE"


class ConnectionStatus(str, Enum):
    """Status values for a user connection."""

    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED" 