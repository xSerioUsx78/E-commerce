from django.contrib import admin

from . import models


admin.site.register([
    models.Product,
    models.ProductImage,
    models.ProductVariation,
    models.ProductVariationItem,
    models.ProductSpecification,
    models.ProductSpecificationItem
])
