#!/usr/bin/env python3
"""Descarga y traduce únicamente las etiquetas de los trucos GOWR PS4 v06.00.
No modifica offsets ni bytes. Ejecutar en PC conectado a Internet.
"""
import argparse
import pathlib
import sys
import urllib.request
import xml.etree.ElementTree as ET

URL = 'https://raw.githubusercontent.com/GoldHEN/GoldHEN_Cheat_Repository/main/shn/CUSA34384_06.00.shn'
FILENAME = 'CUSA34384_06.00.shn'
TRANSLATIONS = {
 'Infinite Health/Rage/Stum/Arrows/Throwables/Weapon Charge (MASTERCODE/MUST BE ON)': '[00] MAESTRO - OBLIGATORIO (ACTIVAR PRIMERO)',
 'Infinite Health': '[01] Kratos - Vida infinita',
 'Infinite Rage': '[02] Kratos - Ira infinita',
 '1 Hit Stum': '[03] Combate - Aturdir de un golpe',
 'Infinite Arrows/Throwables': '[04] Armas - Flechas/objetos infinitos',
 'Infinite Weapon Charge (L1+Triangle)': '[05] Armas - Carga infinita (L1+Triangulo)',
 'No Cooldown': '[06] Combate - Sin espera de habilidades',
 'Max/Infinite HS/Resources/Fleeting Echoes/Mastery Seal/Spirit Seal/Divine Triunph': '[07] Recursos - Maximo/ilimitados',
 'Max XP (Do Not Use In Valhalla)': '[08] XP maxima - NO USAR EN VALHALLA',
 'Crystalline Fragment (100/Use Only For It)': '[09] Recursos - 100 fragmentos cristalinos',
}

def make_custom(data: bytes) -> bytes:
    root = ET.fromstring(data)
    if root.tag != 'Trainer' or root.get('Cusa') != 'CUSA34384' or root.get('Version') != '06.00':
        raise ValueError('El archivo NO coincide con CUSA34384 version 06.00. Se cancela.')
    cheats = root.findall('Cheat')
    actual = [c.get('Text') for c in cheats]
    if len(cheats) != len(TRANSLATIONS) or set(actual) != set(TRANSLATIONS):
        raise ValueError('El repositorio ha cambiado sus trucos. Revisar manualmente antes de instalar.')
    for c in cheats:
        lines = c.findall('Cheatline')
        if not lines or any(ln.findtext('Offset') is None or ln.findtext('ValueOn') is None or ln.findtext('ValueOff') is None for ln in lines):
            raise ValueError('Cheatline incompleta: se cancela')
        c.set('Text', TRANSLATIONS[c.get('Text')])
    # Verificación: estructura y bytes coinciden estrictamente con la fuente original.
    original = ET.fromstring(data)
    for old, new in zip(original.findall('Cheat'), cheats):
        assert ET.tostring(ET.fromstring(ET.tostring(old)).find('Cheatline')) == ET.tostring(ET.fromstring(ET.tostring(new)).find('Cheatline'))
    ET.indent(root, space='  ')
    return b'<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(root, encoding='utf-8') + b'\n'

def main():
    parser = argparse.ArgumentParser(description='GOWR Custom Cheats para GoldHEN, CUSA34384 v06.00')
    parser.add_argument('--origen', type=pathlib.Path, help='Archivo .shn original descargado por el usuario (sin Internet)')
    parser.add_argument('--salida', type=pathlib.Path, default=pathlib.Path('SALIDA'))
    args = parser.parse_args()
    if args.origen:
        data = args.origen.read_bytes()
    else:
        print('Descargando solo desde el repositorio oficial GoldHEN...')
        req = urllib.request.Request(URL, headers={'User-Agent':'GOWR-Cheats-ES/1.0'})
        with urllib.request.urlopen(req, timeout=20) as response:
            data = response.read(500_000)
    output = make_custom(data)
    args.salida.mkdir(parents=True, exist_ok=True)
    target = args.salida / FILENAME
    if target.exists():
        # Nunca sobreescribir: guardar una copia externa manual si hay cambios propios.
        backup = target.with_suffix('.shn.bak')
        if backup.exists():
            raise FileExistsError('Ya existe una copia de seguridad. Mueve SALIDA antes de repetir.')
        target.rename(backup)
    target.write_bytes(output)
    print(f'OK: {target.resolve()}')
    print('Trucos traducidos:', len(TRANSLATIONS))
    print('IMPORTANTE: El atajo L1 + CIRCULO NO esta implementado en GoldHEN.')
    print('El menu real de GoldHEN se abre manteniendo SHARE.')

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('ERROR:', exc, file=sys.stderr)
        sys.exit(1)
