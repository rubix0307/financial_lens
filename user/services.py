from django.contrib.auth import get_user_model


User = get_user_model()

class UserService:
    @staticmethod
    def create_user(username, password, telegram_id=None, last_name=None, language_code=None) -> User:
        user = User.objects.create(
            username=username,
            telegram_id=telegram_id,
            last_name=last_name,
            language_code=language_code
        )

        return UserService.set_user_password(user=user, password=password)

    @staticmethod
    def get_or_create_user_by_telegram_id(telegram_id, username=None, password=None) -> User:
        user, created = User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                'username': username,
            }
        )
        return UserService.set_user_password(user=user, password=password)

    @staticmethod
    def set_user_password(user: User, password: str) -> User:
        if password:
            user.set_password(password)
            user.save(update_fields=['password'])
        return user