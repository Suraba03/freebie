from django.db import models

# LAYER ONE

class Feature(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Add new feature"
    )
    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Add new place type"
    )
    def __str__(self):
        return self.name

class Location(models.Model):
    city = models.CharField(max_length=100)
    number = models.SmallIntegerField()
    birudingu = models.SmallIntegerField(default=-1)
    street = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        if self.birudingu == -1:
            return f'{self.number} {self.street} st, {self.city}'
        else:
            return f'{self.number} {self.street} st, bld {self.birudingu}, {self.city}'

# LAYER TWO

class Network(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        help_text="fee charged per hour"
    )
    description = models.TextField(blank=True, null=True)
    discounts = models.TextField(blank=True, null=True)

    ALCOHOL_RULES = (
        ('f', 'Forbidden'),
        ('a', 'Allowed'),
        ('a', 'Forbidden with your own'),
    )

    SMOKING_RULES = (
        ('f', 'Forbidden'),
        ('a', 'Allowed'),
        ('r', 'Special room'),
    )

    AGE_RULES = (
        ('e', 'Everyone allowed'),
        ('f', '18+'),
    )

    alcoholRules = models.CharField(
        max_length=1,
        choices=ALCOHOL_RULES,
        blank=True,
        default='f',
        help_text='alcohol restrictions',
    )

    smokingRules = models.CharField(
        max_length=1,
        choices=SMOKING_RULES,
        blank=True,
        default='f',
        help_text='smoking restrictions',
    )

    ageRules = models.CharField(
        max_length=1,
        choices=AGE_RULES,
        blank=True,
        default='e',
        help_text='age restrictions',
    )

    type = models.ManyToManyField(
        Type,
        help_text="Add type of the place (e.g. anti-cafe or coworking)"
    )
    location = models.ManyToManyField(
        Location, 
        help_text="Add location of the place"
    )
    feature = models.ManyToManyField(
        Feature,
        help_text="Add location of the place"
    )

    def __str__(self):
        return f'title: {self.name}, cost: {self.cost}, type: {self.type}, location {self.location}'

# LAYER THREE

class Place(models.Model):
    """Model representing a specific place of some network"""
    location = models.ForeignKey('Location', help_text="Enter location", on_delete=models.SET_NULL, null=True)
    network = models.ForeignKey('Network', help_text="Enter network", on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f'title: {self.network.name}, cost: {self.network.cost}, type: {self.network.type}'