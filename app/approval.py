# approval.py
from config import settings

def require_approval(result: str):
    if settings.REQUIRE_HUMAN_APPROVAL:
        input("HUMAN APPROVAL REQUIRED. Press ENTER to approve...")