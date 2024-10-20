from django.contrib import admin

# Register your models here.
from .models import Participant,Reservation
class HasConfirmedReservationFilter(admin.SimpleListFilter):
    title = 'Réservation confirmée'
    parameter_name = 'has_confirmed_reservation'

    def lookups(self, request, model_admin):
        return [
            ('Yes', 'Avec réservation confirmée'),
            ('No', 'Sans réservation confirmée'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            # Retourne les participants avec au moins une réservation confirmée
            return queryset.filter(reservation__confirmed=True).distinct()
        elif self.value() == 'No':
            # Exclut les participants avec des réservations confirmées
            return queryset.exclude(reservation__confirmed=True).distinct()
        return queryset
    

class ParticipantAdmin(admin.ModelAdmin):
    #fields=('email','cin','first_name','last_name','participant_category')
    list_display=('cin','email','first_name','last_name','participant_category','created_at','updated_at')
    search_fields=('first_name','last_name','email')
    list_per_page=2
    ordering=('created_at','first_name')
    fieldsets=(
        ('information sur le participant',
         {
            'fields':('cin','email','first_name','last_name','username')
         }),
        ('categorie du participant',
         {'fields':('participant_category',)
         })
    )
    readonly_fields=('created_at','updated_at')
    list_filter=('participant_category',HasConfirmedReservationFilter)
    #list_editable=('first_name','last_name')
    list_display_links=('email',)
    date_hierarchy='created_at'
    #HasConfirmedReservationFilter
    list_max_show_all = 4 # list_max_show_all limite le nombre d'objets affichés lorsqu'un utilisateur choisit l'option "Afficher tout" dans l'interface d'administration.

admin.site.register(Participant,ParticipantAdmin)

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('conference', 'participant', 'reservation_date', 'confirmed')
    search_fields = ('conference', 'participant')
    list_filter = ('confirmed', 'reservation_date')
    actions=['confirmed','unconfirmed']
    def confirmed(self,request,queryset):
        queryset.update(confirmed=True)
        self.message_user(request,"les reservations sont mis comme confirme")
    confirmed.short_description="Reservation a confirmer"

    def unconfirmed(self,request,queryset):
        queryset.update(confirmed=False)
        self.message_user(request,"les reservations sont mis comme non confirme")
    unconfirmed.short_description="Reservation a annuler"

admin.site.register(Reservation, ReservationAdmin)

