# Global status storage that both files can access
global_status_updates = []

def add_status(message: str):
    """Add a status update"""
    global_status_updates.append(message)

def clear_status():
    """Clear all status updates"""
    global_status_updates.clear()

def get_status():
    """Get all status updates"""
    return global_status_updates.copy()