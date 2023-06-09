"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from levelupapi.models import Event, Game, Gamer


class EventView(ViewSet):
    """Level up event view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all()

        if "game" in request.query_params:
            events = events.filter(game=request.query_params["game"])

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized event instance
        """
        organizer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["game"])

        event = Event.objects.create(
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
            game=game,
            organizer=organizer,
        )

        serializer = EventSerializer(event)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]

        event_game = Game.objects.get(pk=request.data["game"])
        event.game = event_game

        event_organizer = Gamer.objects.get(user=request.auth.user)
        event.organizer = event_organizer
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=["POST"], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(gamer)
        return Response({"message": "Gamer added"}, status=status.HTTP_201_CREATED)

    @action(methods=["DELETE"], detail=True)
    def leave(self, request, pk):
        """Delete a gamer from an event"""
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        return Response({"message": "Gamer removed"}, status=status.HTTP_204_NO_CONTENT)


class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gamer
        fields = ("id", "full_name")


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ("id", "title", "maker", "number_of_players", "skill_level")


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for event"""

    organizer = OrganizerSerializer(many=False)
    game = GameSerializer(many=False)

    class Meta:
        model = Event
        fields = ("id", "description", "date", "time", "game", "organizer")
