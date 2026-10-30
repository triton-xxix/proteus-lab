import sys
import zipfile
with zipfile.ZipFile(sys.argv[1]) as z:
    for i in z.infolist():
        print(i.filename, "compress_type", i.compress_type, "size", i.file_size, "compressed", i.compress_size)
