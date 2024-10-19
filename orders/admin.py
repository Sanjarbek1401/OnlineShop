import csv
import json
import datetime
from django.http import HttpResponse
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)


def export_to_csv(modeladmin, request, queryset):
    opt = modeladmin.model._meta
    content_disposition = f'attachment; filename={opt.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opt.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])

    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


def export_to_json(modeladmin, request, queryset):
    opt = modeladmin.model._meta
    content_disposition = f'attachment; filename={opt.verbose_name}.json'
    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = content_disposition

    # Create a list of dictionaries for each object
    data = []
    for obj in queryset:
        item = {}
        for field in opt.get_fields():
            if not field.many_to_many and not field.one_to_many:
                value = getattr(obj, field.name)
                if isinstance(value, datetime.datetime):
                    value = value.strftime('%d/%m/%Y')
                item[field.verbose_name] = value
        data.append(item)

    response.write(json.dumps(data, ensure_ascii=False, indent=4))
    return response


def export_to_txt(modeladmin, request, queryset):
    opt = modeladmin.model._meta
    content_disposition = f'attachment; filename={opt.verbose_name}.txt'
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = content_disposition

    # Write data rows in a readable format
    for obj in queryset:
        data_row = []
        for field in opt.get_fields():
            if not field.many_to_many and not field.one_to_many:
                value = getattr(obj, field.name)
                if isinstance(value, datetime.datetime):
                    value = value.strftime('%d/%m/%Y')
                data_row.append(f"{field.verbose_name}: {value}")
        response.write('\n'.join(data_row) + '\n\n')  # Add extra newline for separation

    return response


# Short descriptions for admin actions
export_to_csv.short_description = 'Export to CSV'
export_to_json.short_description = 'Export to JSON'
export_to_txt.short_description = 'Export to TXT'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created',
                    'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv, export_to_json, export_to_txt]
