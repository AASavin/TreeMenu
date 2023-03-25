from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    parent = models.ForeignKey('MenuItem', on_delete=models.CASCADE, related_name='children', blank=True, null=True)
    url = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_parents(self):
        if self.parent:
            return self.parent.get_parents() + [self.parent]
        else:
            return []
