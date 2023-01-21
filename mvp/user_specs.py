import pandas as pd
from data_engine import DataEngine

class Userstats:
    def __init__(self) -> None:
        self.data_db = DataEngine()

    def get_user_spend(self, user_id: int) -> int:
        
        return self.data_db.get_user_spend(user_id)
    
    def get_user_balance(self, user_id: int) -> int:
        return self.data_db.get_user_balance(user_id)