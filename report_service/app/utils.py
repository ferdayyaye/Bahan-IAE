import requests
from flask import current_app

class UserServiceClient:
    @staticmethod
    def get_user(user_id):
        """Ambil data user dari user_service"""
        try:
            url = f"{current_app.config['USER_SERVICE_URL']}/internal/users/{user_id}"
            headers = {"X-Service-Token": current_app.config.get("SERVICE_TOKEN")}
            resp = requests.get(url, headers=headers, timeout=5)
            
            if resp.status_code == 200:
                return resp.json(), None
            else:
                return None, f"Status {resp.status_code}"
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def get_all_users():
        try:
            url = f"{current_app.config['USER_SERVICE_URL']}/users"
            resp = requests.get(url, timeout=5)
            
            if resp.status_code == 200:
                return resp.json(), None
            else:
                return [], f"Status {resp.status_code}"
        except Exception as e:
            return [], str(e)

class TransactionServiceClient:
    @staticmethod
    def get_transaction(transaction_id):
        """Ambil single transaction"""
        try:
            url = f"{current_app.config['TRANSACTION_SERVICE_URL']}/transactions/{transaction_id}"
            resp = requests.get(url, timeout=5)
            
            if resp.status_code == 200:
                return resp.json(), None
            else:
                return None, f"Status {resp.status_code}"
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def get_all_transactions():
        """Ambil semua transactions"""
        try:
            url = f"{current_app.config['TRANSACTION_SERVICE_URL']}/transactions"
            resp = requests.get(url, timeout=5)
            
            if resp.status_code == 200:
                return resp.json(), None
            else:
                return [], f"Status {resp.status_code}"
        except Exception as e:
            return [], str(e)
