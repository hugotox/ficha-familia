from main.models import EstadoFamiliaAnio


def custom_context(request):
    periods = list(EstadoFamiliaAnio.objects.all().values_list("anio", flat=True).distinct("anio").order_by("anio"))
    if request.user:
        es_admin = request.user.is_superuser
    else:
        es_admin = False
    return {
        'PERIODS': periods,
        'ES_ADMIN': es_admin
    }
