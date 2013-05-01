from utils.validators import validate_rut


def format_rut(rut):
    formatted = ""
    if validate_rut(rut):
        rut = rut.replace(".", "").replace("-", "")
        tmp = rut[::-1]
        rut = "%s-%s.%s.%s" % (tmp[0], tmp[1:4], tmp[4:7], tmp[7:])
        formatted = rut[::-1]
    return formatted
