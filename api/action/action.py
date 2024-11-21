import re
from api.serializers import ActionSerializer

def create_action(name, color, match, team, is_default, user):
    action_key = re.sub('[^A-Za-z0-9]+', '', name)
    data = {
            'name': name,
            'key': action_key,
            'color': color,
            'match': match,
            'team': team,
            'status': 'PUBLISHED',
            'default': is_default,
            'updated_by': user,
            'enabled': True
        }
    serializer = ActionSerializer(data=data)
    return serializer
