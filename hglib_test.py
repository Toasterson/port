import hglib

client = hglib.open('~/.ports/tmp/python3')
rev = None
tags = client.tags()
for tag in client.tags():
    if '3.5.1' in tag[0].decode():
        rev = tag[2]
        print(tag[0].decode() + ' ' + tag[2].decode())
        break
client.update(rev)
