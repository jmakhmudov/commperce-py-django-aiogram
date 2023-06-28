from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models, transaction


class CustomAdminManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, tgid, name, password, **kwargs):
        user = self.model(
            name=name, tgid=tgid, password=password, is_superuser=False, is_staff=False
        )
        user.save()

        return user

    def create_superuser(self, tgid, name, password, **kwargs):
        user = self.model(
            name=name, tgid=tgid, password=password, is_superuser=True, is_staff=True
        )
        user.save()

        return user


class Admin(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=150, unique=True, verbose_name="Уникальное имя")
    tgid = models.CharField(
        max_length=50, unique=True, verbose_name="Свой уникальный id в телеграм"
    )
    is_staff = models.BooleanField(default=True)

    objects = CustomAdminManager()

    USERNAME_FIELD = "name"

    REQUIRED_FIELDS = ("tgid", "password")

    class Meta:
        db_table = "admins"
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=300, verbose_name="Название группы")
    tgid = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "groups"
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self) -> str:
        return self.name


class Settings(models.Model):
    base = models.BooleanField(default=False, verbose_name="Настройки по умолчанию")
    group = models.ForeignKey(
        to=Group,
        on_delete=models.CASCADE,
        related_name="settings",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=220, verbose_name="Название настроек")
    include_url = models.BooleanField(
        default=True, verbose_name="Включить фильтрацию по ссылкам"
    )
    include_length = models.BooleanField(
        default=True, verbose_name="Включить фильтрацию по длине"
    )
    include_shitword = models.BooleanField(
        default=True, verbose_name="Включить фильтрацию матов"
    )
    wait_time = models.IntegerField(
        default=60, verbose_name="Время ожидания (в секундах)"
    )
    max_length = models.IntegerField(
        default=500, verbose_name="Максимальная разрешенная длина сообщения"
    )
    shitwords = models.TextField(
        verbose_name="Маты через запятую", null=True, blank=True
    )
    text_shitword = models.TextField(verbose_name="Текст (маты)", null=True, blank=True)
    text_length = models.TextField(
        verbose_name="Текст (превышение длины)", null=True, blank=True
    )
    text_url = models.TextField(verbose_name="Текст (ссылка)", null=True, blank=True)

    class Meta:
        db_table = "settings"
        verbose_name_plural = "Настройки"
        verbose_name = "Настройки"

    def save(self, *args, **kwargs):
        if not self.base:
            return super().save(*args, **kwargs)
        with transaction.atomic():
            Settings.objects.filter(base=True).update(base=False)
            return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class AddPublication(models.Model):
    group = models.ForeignKey(
        to=Group,
        on_delete=models.CASCADE,
        related_name="publications",
        verbose_name="группа",
    )
    body = models.TextField(
        verbose_name="текст публикации",
        help_text="""
<pre><xmp><b>жирный</b>, <strong>жирный</strong>
<i>курсив</i>, <em>курсив</em>
<u>подчеркнутый</u>, <ins>подчеркнутый</ins>
<s>зачеркнутый</s>, 
<strike>зачеркнутый</strike>, 
<del>зачеркнутый</del>
<tg-spoiler>скрытый текст, на который надо нажать, чтобы он отобразился</tg-spoiler>
<span class="tg-spoiler">скрытый текст, на который надо нажать, чтобы он отобразился</span>
<b>жирный<i>курсив жирный <s>курсив жионый зачеркнутый</s> <u>подчеркнутый курсив жирный</u></i> жирный</b>
<a href="http://www.example.com/">ссылка в тексте</a>
<a href="tg://user?id=1040628188">Упоминание пользователя с id 1040628188</a></xmp></pre>
        """,
    )
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    publ_at = models.DateTimeField(verbose_name="дата и время публикации")

    class Meta:
        db_table = "publications"
        verbose_name = "Запланированная публикация"
        verbose_name_plural = "Запланированные публикации"

    def __str__(self):
        return f'"{self.body[:20]}..." ---> "{self.group.name}" '
