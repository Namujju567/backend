from django.db import models


defaultTheme = 'default'


class ThemePreference(models.Model):
    theme = models.CharField(
        max_length=20,
        choices=[('default', 'Default'), ('black', 'Black')],
        default=defaultTheme,
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Theme Preference'

    def __str__(self):
        return f'Theme: {self.theme}'

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
