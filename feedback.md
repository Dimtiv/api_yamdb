###Правка №1
API/serializers.py
В class SignUpSerializer в валидаторе мы проверяем чтобы username и email не повторялись, 
наш ревьювер указывает на то что это делать не надо, что в models эти поля уже указаны как уникальные. 
Но без этой валидации проверки не проходит.

>1. Если в валидаторе не проверять, то будет необработанное исключение
 django.db.utils.IntegrityError: UNIQUE constraint failed: users_user.email
 И программа упадет.
 
Тесты же в свою очередь ожидают код ответа 400.
 
Вообще придерживаюсь парадигмы, что валидации в сериализаторе самое место, а 
если ошибка доходит до модели, значит это недоработка.


###Правка №2
>API/views.py
мы юзера создаем по вьюхе, он просит перенести в сериализатор это. 
Не совсем понятен этот момент.

Здесь поддерживаю ревьювера. У вас есть сериализатор на основе ModelSerializer
Т.е. он заточен на то, чтобы создавать объекты моделей. И если нет каких-то 
дико необычных неординарных ситуаций, то в нем и нужно создавать модели.
Код становится прозрачнее, понятнее, лаконичнее, проще для понимания.

У ModelSerializer есть метод save, он возвращает сохраненный объект.

Т.е. для вашего случая, код будет выглядеть так

```
class SignUpViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # user, created = User.objects.get_or_create(**serializer.validated_data)

```