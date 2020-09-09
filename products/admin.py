from django.contrib import admin
from .models import ProductInfo, ProductStock, Category

# Register your models here.


class ProductStockInline(admin.TabularInline):
    model = ProductStock


class ProductInfoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'skup1',
        'category',
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


class ProductLinesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'variety_name',
        'skup2',
        'product',
        'price',
        'stock_qty',
        'stock_reserved',
    )


admin.site.register(ProductInfo, ProductInfoAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductStock, ProductLinesAdmin)
