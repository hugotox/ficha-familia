# Rut validator
def validate_rut(rut):
    valid = False

    if rut is not None and rut != "":
        rut = rut.replace(".", "").replace("-", "")
        dv = str(rut[-1]).upper()
        rut = rut[0:-1]
        suma = 0
        multi = 2
        for r in rut[::-1]:
            try:
                r = int(r)
            except:
                return False
            suma += int(r) * multi
            multi += 1
            if multi == 8:
                multi = 2
        resto = suma % 11
        diff = 11 - resto
        if diff == 11:
            expected = '0'
        elif diff == 10:
            expected = 'K'
        else:
            expected = str(diff)
        valid = expected == dv
    return valid
