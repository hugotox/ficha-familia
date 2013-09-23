from models import EstadoFamiliaAnio


def custom_context(request):
    periods = list(EstadoFamiliaAnio.objects.all().values_list("anio", flat=True).distinct("anio").order_by("anio"))
    return {
        'PERIODS': periods
    }
