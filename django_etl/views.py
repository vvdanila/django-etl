import logging

from collections import defaultdict

from django.db import DatabaseError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, serializers, pagination

from .models import MalePlayer
from .tasks import process_fifa_players_dataset


logger = logging.getLogger(__name__)


class HealthCheckView(APIView):
    def get(self, request, *args, **kwargs):
        health_data = {"status": "up"}
        try:
            from django.db import connections

            for db in list(connections.all()):
                db.ensure_connection()
        except DatabaseError:
            health_data["status"] = "down"
            return Response(health_data, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(health_data, status=status.HTTP_200_OK)


tasks_mapping = {"process_fifa_players_dataset": process_fifa_players_dataset}


class TaskAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        task_name = data["task"]
        task = tasks_mapping[task_name]
        task.delay()

        return Response(
            {"message": f"Task {task_name} has been scheduled for processing"},
            status=status.HTTP_201_CREATED,
        )


class MalePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MalePlayer
        fields = "__all__"


class MalePlayerListView(generics.ListAPIView):
    serializer_class = MalePlayerSerializer
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        return MalePlayer.objects.all().order_by("fifa_update_date")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)

        grouped_data = defaultdict(list)
        for male_player in page:
            grouped_data[male_player.potential].append(
                MalePlayerSerializer(male_player).data
            )

        paginated_response = self.get_paginated_response(grouped_data)

        return Response(paginated_response.data)
