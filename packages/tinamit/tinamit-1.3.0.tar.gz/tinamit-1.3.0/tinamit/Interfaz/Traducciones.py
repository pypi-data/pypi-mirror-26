import io
import json

import pkg_resources


class Diccionario(object):
    def __init__(símismo):
        símismo.direc = pkg_resources.resource_filename('tinamit.Interfaz', 'Trads.json')
        with open(símismo.direc, encoding='utf8') as d:
            símismo.dic = json.load(d)

        símismo.lenguas = símismo.dic['Lenguas']
        símismo.estándar = 'Español'

        símismo.verificar_estados()

        símismo.leng_act = símismo.lenguas[símismo.dic['Actual']]
        símismo.trads_act = símismo.leng_act['Trads']
        símismo.izq_a_derech = símismo.leng_act['IzqaDerech']

    def guardar(símismo):
        with io.open(símismo.direc, 'w', encoding='utf8') as d:
            json.dump(símismo.dic, d, ensure_ascii=False, sort_keys=True, indent=2)

    def verificar_estados(símismo):
        estándar = símismo.lenguas[símismo.estándar]

        for nombre, leng in símismo.lenguas.items():
            llenos = []
            for frase in estándar['Trads']:
                if frase in leng['Trads'].keys() and leng['Trads'][frase] != '':
                    llenos.append(1)
                else:
                    leng['Trads'][frase] = ''
                    llenos.append(0)
            símismo.lenguas[nombre]['Estado'] = sum(llenos)/len(llenos)

        for nombre, leng in símismo.lenguas.items():
            for frase in leng['Trads'].copy():
                if frase not in estándar['Trads'].keys():
                    leng['Trads'].pop(frase)
