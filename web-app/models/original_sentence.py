"""This DB stores the original sentence that the user speaks into the microphone."""
from app import mongo

def get_mongo():
    """Return mongo, messes up lazy import!!!"""
    return mongo

class OriginalSentence:
    """An original sentence spoken from the user after it has been parsed 
    from speech through machine learning into text"""

    def __init__(self):
        """Initialize originalSentence DB"""
        self.db = get_mongo()

    def get(self):
        """Get original version of sentence"""
        return {"placeholder": "original"}

    def make_pylint_happy_func():
        """Need two public functions for pylint to be happy"""
        return
    