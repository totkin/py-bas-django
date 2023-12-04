from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

REGULAR_NVARCHAR_LENGTH = 255
SHORT_NVARCHAR_LENGTH = 50


class WorkingUser(User):
    pass


class Title(models.Model):
    """Должность"""
    short_name = models.CharField(
        max_length=SHORT_NVARCHAR_LENGTH,
        help_text="Краткое название должности",
        verbose_name="Должность кратко"
    )
    name = models.CharField(
        max_length=REGULAR_NVARCHAR_LENGTH,
        help_text="Должность",
        verbose_name="Должность"
    )

    def __str__(self):
        return f"{self.name} ({self.short_name})"

    def get_queryset(self):
        return Title.objects.all()

    def get_absolute_url(self):
        return reverse("title-detail", args=[str(self.id)])


class Department(models.Model):
    """Отдел"""
    short_name = models.CharField(max_length=SHORT_NVARCHAR_LENGTH,
                                  help_text="Отдел кратко",
                                  verbose_name="Отдел кратко")

    name = models.CharField(max_length=REGULAR_NVARCHAR_LENGTH,
                            help_text="Название отдела",
                            verbose_name="Отдел")

    additional_info = models.CharField(max_length=REGULAR_NVARCHAR_LENGTH,
                                       help_text="Дополнительная информация по отделу",
                                       verbose_name="Доп информация",
                                       blank=True)

    def get_absolute_url(self):
        return reverse("department-detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.short_name}"

    def get_queryset(self):
        return Department.objects.all()


class Manager2Subscription(models.Model):
    managers = models.ForeignKey(to='Manager', on_delete=models.CASCADE)
    subscriptions = models.ForeignKey(to='Subscription', on_delete=models.CASCADE, )
    created_at = models.DateTimeField(auto_now_add=True)


class Subscription(models.Model):
    """Должность"""

    SUBSCRIPTION_STATUS = (
        ("+", "Включена"),
        ("-", "Отключена"),
        ("X", "Неактивна"),
    )

    SUBSCRIPTION_FREQUENCY = (
        ("D", "1 раз в день"),
        ("DD", "Несколько раз в день"),
        ("W", "1 раз в неделю"),
        ("O", "Однократно"),
    )

    name = models.CharField(max_length=REGULAR_NVARCHAR_LENGTH, help_text="Рассылка", verbose_name="Название")
    status = models.CharField(max_length=1, choices=SUBSCRIPTION_STATUS, default="+", null=False, verbose_name="Статус")
    frequency = models.CharField(max_length=2, choices=SUBSCRIPTION_FREQUENCY, default="D", null=False,
                                 verbose_name="Частота")
    managers = models.ManyToManyField(to='Manager', through='Manager2Subscription',
                                      through_fields=("subscriptions", "managers"))

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.frequency}"

    def get_absolute_url(self):
        return reverse("subscription-detail", args=[str(self.id)])

    def get_queryset(self):
        return Subscription.objects.all()


class Manager(models.Model):
    """Сотрудник"""
    GENDER_CHOICES = [
        ("М", "Мужчина"),
        ("Ж", "Женщина"),
        ("-", "Не указано"),
    ]

    MANAGER_STATUS = (
        ("+", "Работает"),
        ("-", "Уволен"),
        ("X", "Удалить из рассылки"),
    )

    first_name = models.CharField(max_length=SHORT_NVARCHAR_LENGTH, verbose_name="Имя")
    last_name = models.CharField(max_length=SHORT_NVARCHAR_LENGTH, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=SHORT_NVARCHAR_LENGTH, verbose_name="Отчество", blank=True)
    title = models.ForeignKey("Title", on_delete=models.SET_NULL, verbose_name="Должность", null=True)
    department = models.ForeignKey("Department", on_delete=models.SET_NULL, verbose_name="Отдел", null=True)
    email = models.EmailField(null=False)
    system_name = models.CharField(max_length=SHORT_NVARCHAR_LENGTH,
                                   verbose_name="Название в системе", null=False)
    subscriptions = models.ManyToManyField(to='Subscription', through='Manager2Subscription',
                                           through_fields=("managers", "subscriptions"))
    status = models.CharField(max_length=1, choices=MANAGER_STATUS, verbose_name="Статус", default="+", null=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол", default="М", null=True)
    birthday = models.DateField(null=True, verbose_name="День рождения", blank=True)

    class Meta:
        ordering = ["department", "status", "title", "last_name", "first_name"]

    def display_subcriptions(self):
        return ', '.join([subscription.name for subscription in self.subscriptions.all()[:3]])

    display_subcriptions.short_description = "Подписки"

    def full_name(self):
        """Creates a string"""
        return " ".join((self.last_name, self.first_name, self.middle_name))

    def get_absolute_url(self):
        return reverse("manager-detail", args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return " ".join((self.first_name, self.middle_name, self.last_name, f"({self.status})"))
