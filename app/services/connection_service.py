from typing import Dict, Optional, List, Any
from uuid import UUID
from app import db
from app.models.connection import UserConnection
from app.models.profile import UserProfile

def get_connections(
    profile_id: UUID, 
    status: Optional[str] = 'ACCEPTED',
    direction: Optional[str] = 'all'
) -> Dict[str, Any]:
    """Get user connections
    
    Args:
        profile_id: UUID of the user profile
        status: Connection status filter (PENDING, ACCEPTED, REJECTED)
        direction: Filter for 'incoming', 'outgoing', or 'all' connections
        
    Returns:
        Dictionary with connections
    """
    profile = db.session.get(UserProfile, str(profile_id))
    if not profile or not profile.is_active():
        return {
            'success': False,
            'message': 'Profile not found'
        }
    
    connections = []
    
    # Get outgoing connections
    if direction in ['all', 'outgoing']:
        outgoing = profile.outgoing_connections  # InstrumentedList
        if status:
            outgoing = [c for c in outgoing if c.status == status]
        connections.extend(outgoing)
    
    # Get incoming connections
    if direction in ['all', 'incoming']:
        incoming = profile.incoming_connections
        if status:
            incoming = [c for c in incoming if c.status == status]
        connections.extend(incoming)
    
    return {
        'success': True,
        'connections': [conn.to_dict() for conn in connections]
    }

def request_connection(requester_id: UUID, recipient_id: UUID) -> Dict[str, Any]:
    """Request a connection between two users
    
    Args:
        requester_id: UUID of the requesting user
        recipient_id: UUID of the recipient user
        
    Returns:
        Dictionary with success status and connection data
    """
    # Check if both users exist and are active
    requester = db.session.get(UserProfile, str(requester_id))
    recipient = db.session.get(UserProfile, str(recipient_id))
    
    if not requester or not requester.is_active():
        return {
            'success': False,
            'message': 'Requester profile not found'
        }
        
    if not recipient or not recipient.is_active():
        return {
            'success': False,
            'message': 'Recipient profile not found'
        }
    
    # Prevent self-connections
    if requester_id == recipient_id:
        return {
            'success': False,
            'message': 'Cannot connect with yourself'
        }
    
    # Check for existing connection in either direction
    existing_outgoing = UserConnection.query.filter_by(
        requester_id=str(requester_id),
        recipient_id=str(recipient_id)
    ).first()
    
    existing_incoming = UserConnection.query.filter_by(
        requester_id=str(recipient_id),
        recipient_id=str(requester_id)
    ).first()
    
    if existing_outgoing:
        return {
            'success': False,
            'message': f'Connection already exists with status: {existing_outgoing.status}'
        }
    
    if existing_incoming:
        return {
            'success': False,
            'message': f'Reverse connection already exists with status: {existing_incoming.status}'
        }
    
    # Create new connection request
    connection = UserConnection(
        requester_id=str(requester_id),
        recipient_id=str(recipient_id),
        status='PENDING'
    )
    
    db.session.add(connection)
    db.session.commit()
    
    return {
        'success': True,
        'message': 'Connection request sent',
        'connection': connection.to_dict()
    }

def update_connection_status(
    profile_id: UUID, 
    connection_id: UUID, 
    status: str
) -> Dict[str, Any]:
    """Update the status of a connection
    
    Args:
        profile_id: UUID of the user profile (must be the recipient)
        connection_id: UUID of the connection
        status: New status (ACCEPTED or REJECTED)
        
    Returns:
        Dictionary with success status and updated connection data
    """
    # Validate status
    if status not in ['ACCEPTED', 'REJECTED']:
        return {
            'success': False,
            'message': 'Status must be ACCEPTED or REJECTED'
        }
    
    # Get the connection
    connection = db.session.get(UserConnection, str(connection_id))
    if not connection:
        return {
            'success': False,
            'message': 'Connection not found'
        }
    
    # Ensure the caller is the recipient
    if str(connection.recipient_id).strip() != str(profile_id):
        return {
            'success': False,
            'message': 'Only the recipient can update the connection status'
        }
    
    # Only pending connections can be updated
    if connection.status != 'PENDING':
        return {
            'success': False,
            'message': f'Cannot update a connection with status: {connection.status}'
        }
    
    # Update status
    connection.status = status
    db.session.commit()
    
    return {
        'success': True,
        'message': f'Connection {status.lower()}',
        'connection': connection.to_dict()
    }

def delete_connection(profile_id: UUID, connection_id: UUID) -> Dict[str, Any]:
    """Delete a connection
    
    Args:
        profile_id: UUID of the user profile (must be requester or recipient)
        connection_id: UUID of the connection
        
    Returns:
        Dictionary with success status
    """
    # Get the connection
    connection = db.session.get(UserConnection, str(connection_id))
    if not connection:
        return {
            'success': False,
            'message': 'Connection not found'
        }
    
    # Verify the user is part of this connection
    if (
        str(connection.requester_id).strip() != str(profile_id).strip()
        and str(connection.recipient_id).strip() != str(profile_id).strip()
    ):
        return {
            'success': False,
            'message': 'You are not authorized to delete this connection'
        }
    
    db.session.delete(connection)
    db.session.commit()
    
    return {
        'success': True,
        'message': 'Connection deleted successfully'
    }