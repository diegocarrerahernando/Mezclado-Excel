import re
from unicodedata import normalize

def normalizar(texto):
    # Se hace normalizado NFD y se eliminan diacríticos
    normalizado_nfd = re.sub(
        r"([^cn\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f]))|c(?!\u0327(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1",
        normalize("NFD", str(texto)), 0, re.I
    )

    # Se hace normalizado NFC sobre lo anterior (se recuperan ñ's y ç's)
    normalizado_nfc = normalize('NFC', normalizado_nfd)

    # Se hace split de la cadena para sacar aquellas subcadenas que SÍ contengan elementos alfanuméricos
    elementos_alfanumericos= re.compile(r'\W+', re.UNICODE).split(normalizado_nfc)
    # Se juntan esas subcadenas en una única cadena
    cadena_final = ''
    for elemento in elementos_alfanumericos:
        cadena_final += elemento
    return cadena_final


def comparar(cadena1, cadena2, porcentaje):
    if (len(cadena1) and len(cadena2)) == 0:
        return True
    else:
        longitud = min(len(cadena1), len(cadena2))
        caracteres_iguales = 0
        for i in range(0, longitud):
            if cadena1[i] == cadena2[i]:
                caracteres_iguales += 1
        return round(caracteres_iguales / longitud) * 100 > porcentaje


# string = 'http://www.óldâ\'çççççbÄíl$%&/#<<   @>|!eyónlìné.org/browñsó.jsp?*+-id=t17800628-33&div=t17800628-33'

# print(normalizar(string))
