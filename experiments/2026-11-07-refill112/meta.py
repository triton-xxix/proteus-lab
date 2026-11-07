"""Refill row 112: what DWD's station zip says about the air-temperature sensor at 01262 (Munich airport).
Usage: python3 -I meta.py ZIP"""
import sys
import zipfile

z = zipfile.ZipFile(sys.argv[1])
for n in z.namelist():
    print(n)
for n in z.namelist():
    if "Geraete_Lufttemperatur" in n or "Geographie" in n:
        print("=====", n)
        print(z.read(n).decode("latin-1"))
