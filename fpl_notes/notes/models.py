from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import reverse

User = get_user_model()


# class HomePage(models.Model):
#     instruction = models.TextField(max_length=5000)
#     usefull_info = models.TextField(max_length=5000)


class Team(models.Model):
    team_name = models.CharField(max_length=25)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    def __str__(self):
        return self.team_name


class Season(models.Model):
    season_start = models.CharField(max_length=4)
    season_end = models.CharField(max_length=4)
    team = models.ForeignKey("Team", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Сезон"
        verbose_name_plural = "Сезоны"

    def __str__(self):
        return self.season_start

    def get_absolute_url(self):
        return reverse("notes_season_list", kwargs={"season": self.season_start})


class Player(models.Model):
    class Position(models.TextChoices):
        GOALKEEPER = "GK"
        DEFENDER = "DF"
        MIDFIELDER = "MD"
        FORWARD = "FW"

    player = models.CharField(max_length=25)
    position = models.CharField(max_length=2, choices=Position.choices)
    season = models.ForeignKey("Season", on_delete=models.CASCADE)
    team = models.ForeignKey("Team", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    def __str__(self):
        return self.player


class Note(models.Model):
    tour = models.IntegerField(choices=[[x, x] for x in range(1, 39)])
    note = models.TextField()
    substatution_off = models.ForeignKey("Player", on_delete=models.CASCADE)
    substatution_on = models.CharField(max_length=25)
    screenshot = models.ImageField(upload_to="photos_of_notes/%Y/%m/%d", blank=True)
    season = models.ForeignKey("Season", on_delete=models.CASCADE)
    author = models.ForeignKey("Team", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=25, unique=True, null=False)

    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"

    def __str__(self):
        return self.tour

    def get_absolute_url(self):
        return reverse("notes_by_tour", kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse("note_update", kwargs={"slug": self.slug})
