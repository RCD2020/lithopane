from zipfile import ZipFile
from tempfile import TemporaryFile

# with ZipFile('zip files/test.zip', 'w') as f:
#     f.writestr('test.txt', 'test1\n')
#     f.writestr('test.txt', 'test2')

#     # will need to use a tempfile
#     # as writing huge strings in memory slows the program
#     # and streaming the data is much more efficient

with TemporaryFile() as tmp:
    for x in range(20):
        tmp.write(f'{x}\n'.encode('ascii'))

    tmp.seek(0)

    with ZipFile('zip files/test2.zip', 'w') as f:
        f.writestr('test.txt', tmp.read())