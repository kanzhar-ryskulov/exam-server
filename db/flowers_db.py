from db.database import Database


class FlowerDatabase(Database):
    file_name = 'flowers.json'

    def __init__(self):
        super().__init__()

        if self.entities:
            self.entity_id = max(
                entity['id']
                for entity in self.entities
            ) + 1
        else:
            self.entity_id = 1

    def add(self, flower):
        flower['id'] = self.entity_id

        super().add(flower)

        self.entity_id += 1

    def type_to_find(self, flower_type):
        results = []

        for ent in self.entities:
            if flower_type in ent['type']:
                results.append(ent)

        return results