from rest_framework.views import APIView
from ..models import 

class EventView(APIView):
    def get(self, request, *args, **kwargs):
        match_id = request.query_params.get('match')
        events = Event.objects.filter(match_id=match_id).exclude(status='DELETED')
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'match': request.data.get('match'),
            'action': request.data.get('action'),
            'created_at': request.data.get('createdAt') if request.data.get('createdAt') else datetime.now(),
            'status': "PUBLISHED",
            'delay': request.data.get('delay') if request.data.get('delay') else 0,
            'updated_by': request.user.pk,
            'disabled': False
        }
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None, *args, **kwargs):
        event_id = id
        if event_id:
            event_to_update = Event.objects.get(id=event_id)
            action_id = request.data.get('action_id')
            delay = request.data.get('delay')
            status_code = request.data.get('status')
            if action_id:
                event_to_update.action = action_id
            if delay:
                event_to_update.delay = delay
            if status_code:
                event_to_update.status = status_code
            event_to_update.updated_by = User.objects.get(id=request.user.pk)
            event_to_update.save()
        else:
            props_to_update = request.data.get('update')
            ids_to_update = request.data.get('ids')
            events_to_update = Event.objects.filter(id__in=ids_to_update).exclude(status='DELETED')
            for event in events_to_update:
                for key, value in props_to_update.items():
                    setattr(event, key, value)
                event.save()
        return Response(status=status.HTTP_200_OK)
    
    def delete(self, request, id, *args, **kwargs):
        event = Event.objects.get(id=id)
        event.delete()
        return Response(status=status.HTTP_200_OK)