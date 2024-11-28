import re
from api.serializers import ActionSerializer

def create_action(name, color, team, default, user_id):
    action_key = re.sub('[^A-Za-z0-9]+', '', name)
    data = {
            'name': name,
            'key': action_key,
            'color': color,
            'match': None,
            'team': team,
            'status': 'PUBLISHED',
            'default': default,
            'updated_by': user_id,
            'enabled': True
        }
    serializer = ActionSerializer(data=data)
    return serializer
