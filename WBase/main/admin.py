from django.contrib import admin

# Register your models here.

from .models import (
    Batch_pr,
    Material,
    W_user,
    Can,
    Lot,
    Weighting,
)

admin.site.register((Batch_pr, Material, W_user, Can, Lot, Weighting,))
