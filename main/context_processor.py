from main.models import EvaluacionFactoresProtectores


def custom_context(request):
    periods = list(EvaluacionFactoresProtectores.objects.all().values_list("anio_aplicacion", flat=True).distinct("anio_aplicacion").order_by("anio_aplicacion"))
    if request.user:
        es_admin = request.user.is_superuser
    else:
        es_admin = False
    return {
        'PERIODS': periods,
        'ES_ADMIN': es_admin
    }
