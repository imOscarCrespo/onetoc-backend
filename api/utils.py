from .models import Team, Match, Action, Club
from .serializers import ClubSerializer, TeamSerializer, MatchSerializer, ActionSerializer
def get_match_by_id(id, user):
    user_teams_query = Team.objects.filter(users__username=user)
    user_match = Match.objects.get(id=id)
    match_team = user_match.team
    user_team_names = []
    for team in user_teams_query:
        user_team_names.append(team.name)
    print(user_match.name)
    print(user_team_names)
    if match_team.name in user_team_names:
        return user_match
    else:
        return False
