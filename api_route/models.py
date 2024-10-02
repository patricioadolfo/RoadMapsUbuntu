from django.db.models import Q
import json

class QueryDict():

    def dict_query(self, dict):
        
        d= json.loads(dict)
        
        self.q_objects = [Q(**{k: v}) for k, v in d.items()]
