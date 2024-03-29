from django.db import models
from django.template.defaultfilters import slugify


# Create your models here.
class TypingTest(models.Model):
    name = models.CharField(max_length=128)
    test_body = models.TextField()
    avg_time = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    credits = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)

        super(TypingTest, self).save(*args, **kwargs)



class TestResult(models.Model):
    user = models.ForeignKey('auth.User', blank=True, null=True)
    date_created = models.DateTimeField(auto_now=True)

    user_text = models.TextField(blank=True, default="")

    total_chars = models.IntegerField()
    total_time = models.IntegerField()
    errors = models.IntegerField()

    typing_test = models.ForeignKey(TypingTest)

    def get_wpm(self):
        minutes = float(self.total_time) / float(60)
        words = self.total_chars / 5
        return round(float(words) / minutes, 2)


    def get_nwpm(self):
        return round(self.get_wpm() - (2 * self.errors), 2)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return "Result #%d: %s" % (self.id, self.typing_test.name)


    def save(self, *args, **kwargs):
        # 1 sec minimum
        if self.total_time == 0:
            self.total_time = 1

        super(TestResult, self).save(*args, **kwargs)
