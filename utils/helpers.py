"""
Helper functions for test automation.
"""
import json
from pathlib import Path


def load_test_data(file_name: str = 'test_data.json') -> dict:
    """
    Load test data from JSON file.
    
    Args:
        file_name: Name of the JSON file in the data directory
        
    Returns:
        Dictionary containing test data
    """
    data_path = Path(__file__).parent.parent / 'data' / file_name
    with open(data_path, 'r') as f:
        return json.load(f)


def get_user_credentials(user_type: str) -> tuple[str, str]:
    """
    Get username and password for a specific user type.
    
    Args:
        user_type: Type of user (standard, locked_out, problem, etc.)
        
    Returns:
        Tuple of (username, password)
    """
    test_data = load_test_data()
    user = test_data['users'].get(user_type)
    if not user:
        raise ValueError(f"User type '{user_type}' not found in test data")
    return user['username'], user['password']
