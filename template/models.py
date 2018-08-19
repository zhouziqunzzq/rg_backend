from django.db import models


class Template(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Verse(models.Model):
    template = models.ForeignKey(
        Template,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.template.name + " - Verse(" + str(self.id) + ")"


class Sentence(models.Model):
    wordCount = models.IntegerField()
    rhyme_pinyin = models.CharField(max_length=30)
    rhyme_type = models.CharField(max_length=30)
    verse = models.ForeignKey(
        Verse,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.verse.template.name + " - Verse(" + str(self.verse.id) \
               + ") - Sentence(" + str(self.id) + ")"
