from django.contrib import admin

from .forms import GalleryForm
from .models import Gallery, GalleryImage


##### Actions
def make_published(self, request, queryset):
    rows_updated = queryset.update(published=True)
    if rows_updated == 1:
        message_bit = "1 gallery was"
    else:
        message_bit = "%s galleries were" % rows_updated
    self.message_user(request, "%s published." % message_bit)
make_published.short_description = "Publish"


def make_unpublished(self, request, queryset):
    rows_updated = queryset.update(published=False)
    if rows_updated == 1:
        message_bit = "1 gallery was"
    else:
        message_bit = "%s galleries were" % rows_updated
    self.message_user(request, "%s unpublished." % message_bit)
make_unpublished.short_description = "Unpublish"


class GalleryInline(admin.TabularInline):
    model = GalleryImage
    extra = 10
    fields = ('image', 'caption', 'byline', 'order')


class GalleryAdmin(admin.ModelAdmin):
    form = GalleryForm

    class Media:
        js = (
            '/static/admin/js/jquery-ui-1.10.3.custom-sortable.min.js',
            '/static/admin/js/inline_reorder.js',
        )

    ordering = ['-created']
    actions = [make_published, make_unpublished]

    list_display = ('title', 'credit', 'published', 'created',)
    list_filter = ('published', 'article')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'summary']

    inlines = [
        #BulkUploadInline,
        GalleryInline,
    ]

    fieldsets = (
        ('Header', {'fields': ('overline', 'title')}),
        ('Content', {'fields': ('summary', 'article', 'bulk_upload')}),
        ('Meta', {'fields': ('credit', 'published')}),
        ('Admin fields', {
            'description': 'You should rarely, if ever, need to touch these fields.',
            'fields': ('slug',),
            'classes': ['collapse']
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.save()
        for img in request.FILES.getlist('bulk_upload'):
            GalleryImage(
                image = img,
                gallery = obj
            ).save()

        obj.bulk_upload = None
        obj.save()


class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'gallery', 'caption', 'byline', )
    search_fields = ['gallery__title', 'caption', 'byline']
    list_filter = ('gallery',)


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(GalleryImage, GalleryImageAdmin)
