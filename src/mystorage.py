import json
import os
from pydantic import BaseModel
from main import CardItem


DATA_PATH = os.getenv("FLET_APP_STORAGE_DATA")


class Pull():
    @staticmethod
    def get() -> list:
        path = os.path.join(DATA_PATH, "data.txt")
        try:
            with open(path, 'r', encoding="utf-8") as file:
                result = json.load(file)
        except: result = []
        
        return result
    
    
    @staticmethod
    def set(data: list[CardItem]):
        path = os.path.join(DATA_PATH, "data.txt")
        with open(path, 'w', encoding="utf-8") as file:
            file.write(str([p.model_dump_json() for p in data]))
        print("succes")

