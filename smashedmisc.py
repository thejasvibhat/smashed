import os

def is_production():
    server = os.environ["SERVER_SOFTWARE"]
    if "Development" in server:
        return False
    else:
        return True
