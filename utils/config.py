"""
Configuration management for test automation.
Loads environment variables and provides configuration constants.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Base configuration
BASE_URL = os.getenv('BASE_URL', 'https://www.saucedemo.com')

# User credentials
STANDARD_USER = os.getenv('STANDARD_USER', 'standard_user')
STANDARD_PASSWORD = os.getenv('STANDARD_PASSWORD', 'secret_sauce')
LOCKED_OUT_USER = os.getenv('LOCKED_OUT_USER', 'locked_out_user')
PROBLEM_USER = os.getenv('PROBLEM_USER', 'problem_user')
PERFORMANCE_GLITCH_USER = os.getenv('PERFORMANCE_GLITCH_USER', 'performance_glitch_user')

# Timeouts (in milliseconds)
DEFAULT_TIMEOUT = 30000  # 30 seconds
NAVIGATION_TIMEOUT = 60000  # 60 seconds
