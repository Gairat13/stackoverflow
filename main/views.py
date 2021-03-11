from rest_framework import viewsets
from main.permissions import IsAuthorPermission
from main.serializers import ProblemCreateSerializer, ReplySerializer, ImageSerializer, CommentSerializer
from main.models import Problem, Reply, CodeImage, Comment
from rest_framework.permissions import IsAuthenticated


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

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class ReplyViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = []


class CommentViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

# TODO: восстановление пароля
# TODO: подключить Celery
# TODO: Перевести отправку СМС на CELERY
# TODO: Пагинация
# TODO: фильтрация
# TODO: Поиск
# TODO: настроить media
# TODO: периодически на таски CELERY
# TODO: деплой
# TODO: тесты
# TODO: CKEditor
# TODO: Фильтрация и поиск в админке
# TODO: Мультиязычность
