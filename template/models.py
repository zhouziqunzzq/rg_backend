from django.db import models


class Template(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Verse(models.Model):
    sentence_count = models.IntegerField()
    word_count = models.IntegerField()
    rhyme_mode = models.IntegerField()  # 1 - 单押, 2 - 双押
    rhyme_style_id = models.IntegerField()  # 0 - 排韵, 1 - 交韵, 2 - 隔行押, 3 - 抱韵
    template = models.ForeignKey(
        Template,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.template.name + " - Verse(" + str(self.id) + ")"


# class Sentence(models.Model):
#     wordCount = models.IntegerField()
#     rhyme_pinyin = models.CharField(max_length=30)
#     rhyme_type = models.CharField(max_length=30)
#     verse = models.ForeignKey(
#         Verse,
#         on_delete=models.CASCADE
#     )
#
#     def __str__(self):
#         return self.verse.template.name + " - Verse(" + str(self.verse.id) \
#                + ") - Sentence(" + str(self.id) + ")"
