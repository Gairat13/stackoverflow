from rest_framework import serializers

from main.models import Problem, CodeImage, Reply, Comment


# class ProblemListSerializer(serializers.ModelSerializer):
#     created = serializers.DateTimeField(format='%d %B %Y %H:%M', read_only=True)
#     author = serializers.ReadOnlyField(source='author.username')
#
#     class Meta:
#         model = Problem
#         fields = ('id', 'title', 'created', 'author')
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['replies'] = instance.reply.count()
#         return representation
#

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeImage
        fields = ('image', )

    def _get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            url = obj.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
            return url
        return ''

    def to_representation(self, instance):
        representation = super(ImageSerializer, self).to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class ProblemCreateSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%d %B %Y %H:%M', read_only=True)
    updated = serializers.DateTimeField(format='%d %B %Y %H:%M', read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Problem
        fields = ('id', 'title_ru', 'title_en', 'title_ky', 'description_ru', 'description_en', 'description_ky',
                  'images', 'created', 'updated')

    def get_fields(self):
        action = self.context.get('action')
        fields = super().get_fields()
        if action == 'list':
            fields.pop('images')
            fields.pop('created')
            fields.pop('description_ru')
            fields.pop('description_en')
            fields.pop('description_ky')
        return fields

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        author = request.user
        problem = Problem.objects.create(author=author, **validated_data)
        for image in images_data.getlist('images'):
            CodeImage.objects.create(problem=problem, image=image)
        return problem

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for k, v in validated_data.items():
            setattr(instance, k, v)

        instance.images.delete()
        images_data = request.FILES
        for image in images_data.getlist('images'):
            CodeImage.objects.create(problem=instance, image=image)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = ImageSerializer(instance.images.all(), many=True, context=self.context).data
        representation['replies'] = ReplySerializer(instance.reply.all(), many=True).data
        return representation

#
# class ProblemDetailSerializer(serializers.ModelSerializer):
#     created = serializers.DateTimeField(format='%d %B %Y %H:%M', read_only=True)
#     author = serializers.ReadOnlyField(source='author.username')
#
#     class Meta:
#         model = Problem
#         fields = ('id', 'title', 'description', 'author', 'created', 'images')
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['images'] = ImageSerializer(instance.images.all(), many=True).data
#         representation['replies'] = ReplySerializer(instance.reply.all(), many=True).data
#         return representation


# class ProblemUpdateSerializer(serializers.ModelSerializer):
#     images = ImageSerializer(many=True, write_only=True)
#
#     class Meta:
#         model = Problem
#         fields = ('title', 'description', 'images')
#
#     def update(self, instance, validated_data):
#         request = self.context.get('request')
#         title = validated_data.get('title')
#         description = validated_data.get('description')
#         if title:
#             instance.title = title
#         if description:
#             instance.description = description
#         images_data = request.FILES
#         instance.save()
#         for image in images_data.getlist('images'):
#             CodeImage.objects.get_or_create(problem=instance, image=image)
#         return instance


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Reply
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        reply = Reply.objects.create(author=author, **validated_data)
        return reply


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

        def create(self, validated_data):
            request = self.context.get('request')
            author = request.user
            comment = Comment.objects.create(author=author, **validated_data)
            return comment




