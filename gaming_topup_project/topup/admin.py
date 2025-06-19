from django.contrib import admin
from .models import Game, TopUpProduct
# Register your models here.

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'game_id', 'is_active']
    search_fields = ['name', 'game_id']


@admin.register(TopUpProduct)
class TopUpProduct(admin.ModelAdmin):
    list_display = ['name', 'game', 'price']
    search_fields = ['name']