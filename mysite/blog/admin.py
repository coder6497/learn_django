from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    prepopulated_fields ={'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ['publish']
    show_facets = admin.ShowFacets.ALWAYS