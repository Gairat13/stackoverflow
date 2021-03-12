from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Problem, Reply, Comment
from main.permissions import IsAuthorPermission
from main.serializers import ProblemCreateSerializer, ReplySerializer, CommentSerializer

MyUser = get_user_model()


# class ProblemListView(generics.ListAPIView):
#     queryset = Problem.objects.all()
#     serializer_class = ProblemListSerializer
#
#
# class ProblemCreateView(generics.CreateAPIView):
#     queryset = Problem.objects.all()
#     serializer_class = ProblemCreateSerializer
#     permission_classes = [IsAuthenticated]
#
#
# class ProblemDetailView(generics.RetrieveAPIView):
#     queryset = Problem.objects.all()
#     serializer_class = ProblemDetailSerializer
#
#
# class ProblemUpdateView(generics.UpdateAPIView):
#     queryset = Problem.objects.all()
#     serializer_class = ProblemUpdateSerializer
#     permission_classes = [ProblemUpdateDeletePermission]
#
#
# class ProblemDeleteView(generics.DestroyAPIView):
#     queryset = Problem.objects.all()
#     permission_classes = [ProblemUpdateDeletePermission]
#


class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'delete']:
            permissions = [IsAuthorPermission]
        else:
            permissions = []
        return [perm() for perm in permissions]


class ProblemViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemCreateSerializer

    @action(methods=['GET'], detail=False)
    def search(self, request):
        query = request.query_params.get('q')
        queryset = self.get_queryset().first(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        serializer = self.get_serializer(queryset, many=True, context={"request": self.request})
        return Response(serializer.data)


class ReplyViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = []


class CommentViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

# TODO: деплой
# TODO: тесты
# TODO: Мультиязычность
