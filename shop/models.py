from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


def item_image(instance, filename):
    return 'items/{}/images/{}'.format(instance.item.slug, filename)


class User(AbstractUser):
    phone = models.CharField(max_length=255)


class Item(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='items')
    description = models.TextField(blank=True, null=True)
    rating = models.CharField(max_length=5, null=True, blank=True)
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('item', args=[self.category.slug, self.slug])

    def default_image_url(self):
        """
        Returns the default image for an item.
        """
        if self.images.all():
            return self.images.get(default=True).file.url
        return 'http://placehold.it/700x400'

    def get_star_rating(self):
        """
        Updates and returns the current avg star rating for an item.
        """
        rvws = self.reviews.all()
        if rvws.exists():
            self.rating = rvws.aggregate(models.Avg('rating'))['rating__avg']
            self.save()
            return self.rating
        return 0

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]

    def save(self, *args, **kwargs):
        # Ensure unique slug
        if not self.slug:
            slug = slugify(self.name)
            num = 0
            while Item.objects.filter(slug=slug).exists():
                num += 1
                slug = '{}_{}'.format(slugify(self.name), num)
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ItemImage(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='images')
    default = models.BooleanField(default=False)
    file = models.ImageField(upload_to=item_image)
    alt_tag = models.TextField(max_length=255)

    def save(self, *args, **kwargs):
        # Ensure there is always one default Image
        item_images = ItemImage.objects.filter(item=self.item)
        if not self.default:
            if not item_images.exists():
                self.default = True
        else:
            for i in item_images:
                i.default = False
                i.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.item.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('category', args=[ self.slug])

    def save(self, *args, **kwargs):
        # Ensure unique slug
        if not self.slug:
            slug = slugify(self.name)
            num = 0
            while Item.objects.filter(slug=slug).exists():
                num += 1
                slug = '{}_{}'.format(slugify(self.name), num)
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Review(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(default=None, null=True)
    date = models.DateTimeField(auto_created=True)
    body = models.TextField()

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return "Review for {} from {}".format(self.item.name, self.user.username)
