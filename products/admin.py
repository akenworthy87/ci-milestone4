from django.contrib import admin
from .models import ProductInfo, ProductStock, Category

# Register your models here.


class ProductStockInline(admin.TabularInline):
    model = ProductStock


class ProductInfoAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'rating',
        'image',
    )

    ordering = ('name',)
    inlines = [
        ProductStockInline,
    ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(ProductInfo, ProductInfoAdmin)
admin.site.register(Category, CategoryAdmin)
