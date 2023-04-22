import re
from api.serializers import ActionSerializer


def create_action(action_name, color, match, is_default, user, auto_create, team_id):
    action_key = re.sub('[^A-Za-z0-9]+', '', action_name)
    data = {
        'name': action_name,
        'key': action_key,
        'color': color,
        'match': match,
        'status': 'PUBLISHED',
        'default': is_default,
        'updated_by': user,
        'enabled': True,
        'events': None,
        'auto_create': auto_create,
        'team': team_id
    }
    serializer = ActionSerializer(data=data)
    return serializer
