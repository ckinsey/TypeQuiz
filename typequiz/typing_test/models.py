from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class TypingTest(models.Model):
    name = models.CharField(max_length=128)
    test_body = models.TextField()
    avg_time = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    credits = models.TextField(blank=True, null=True)

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
        return float(words) / minutes

    def get_nwpm(self):
        return self.get_wpm() - (2 * self.errors)

