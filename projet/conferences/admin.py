from django.contrib import admin
from .models import Conferences
from users.models import *
from django.db.models import Count
# Register your models here.
class ReservationInline(admin.TabularInline):
    model=Reservation
    extra=1
    readonly_fields=('reservation_date',)
    can_delete=True
"""class ReservationInline(admin.StackedInline):
    model=Reservation
    extra=1
    readonly_fields=('reservation_date',)
    can_delete=True
"""
class ConferenceDateFilter(admin.SimpleListFilter):
    title='date conf filter'
    parameter_name='conference date'
    def lookups(self,request,model_admin):
        return (
            ('Past',('Past Conferences')),
            ('Upcoming',('Upcoming Conferences')),
            ('Today',('Today Conferences'))
        )
    def queryset(self, request, queryset):
        #bch nchouf l conference ili mafihomch participant
        if self.value()=='Past' :
            return queryset.filter(end_date__lt=timezone.now().date())
        if self.value()=='Upcoming':   
            return queryset.filter(start_date__gt=timezone.now().date())
        if self.value()=='Today':   
            return queryset.filter(start_date=timezone.now().date())
        return queryset
    
class ParticipantFilter(admin.SimpleListFilter):
    title="participant filter"
    parameter_name="participants"
    def lookups(self,request,model_admin ):
        return (
            ('0',('no participants')),
            ('more',('More participants'))
        )
    """
    def queryset(self, request, queryset):
        #bch nchouf l conference ili mafihomch participants
        if self.value()=='0' :
            return queryset.annotate(participant_count=Count('Reservation')).filter(participant_count=0)
        if self.value()=='more':   
            return queryset.annotate(participant_count=Count('Reservation')).filter(participant_count__gt=0)
        return queryset
    """
    def queryset(self, request, queryset):
        #bch nchouf l conference ili mafihomch participants
        if self.value()=='0' :
            return queryset.filter(Reservation__isnull=True)
        if self.value()=='more':   
            return queryset.filter(Reservation__isnull=False)
        return queryset
     
class ConferenceAdmin(admin.ModelAdmin):
    list_display=('title' ,'location','start_date','end_date','price')
    search_fields=('title',)
    list_per_page=2
    #pour un ordre inverse on fait  ordering=('-start_date') 
    ordering=('start_date','title')
    fieldsets= (
        ('description',{
            'fields':('title','description','category','location')
        }),
        ('horaire',{
            'fields':('start_date','end_date','created_at','updated_at')
        }),
        ('Documents',{
            'fields':('program',)
        })
    )
    readonly_fields=('created_at','updated_at')
    inlines=[ReservationInline]
    autocomplete_fields=('category',)#voir admin categorie
    list_filter=('title',ParticipantFilter,ConferenceDateFilter)
admin.site.register(Conferences,ConferenceAdmin)
