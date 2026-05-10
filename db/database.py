import json
from pathlib import Path


class Database:
    file_name = 'database.json'

    def __init__(self):
        self.path = Path(self.file_name)
        self.entities = self.load()

    def load(self):
        try:
            return json.loads(
                self.path.read_text(encoding='utf-8')
            )
        except:
            return []

    def save(self):
        self.path.write_text(
            json.dumps(
                self.entities,
                ensure_ascii=False,
                indent=4
            ),
            encoding='utf-8'
        )

    def list(self):
        return self.entities

    def add(self, entity):
        self.entities.append(entity)
        self.save()

    def detail(self, id):
        for entity in self.entities:
            if entity['id'] == id:
                return entity
        return None

    def delete(self, id):
        for i, entity in enumerate(self.entities):
            if entity['id'] == id:
                self.entities.pop(i)
                self.save()
                return True

        return False