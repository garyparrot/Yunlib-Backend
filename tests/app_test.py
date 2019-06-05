import app
import Yunlib.resource as res

cloader = res.ConfigLoader('./resource.ini')
print("Testing", cloader.library_id)

craw,result = app.start_crawler(cloader.library_id, cloader.library_pwd)


if result:
    print(app.create_booklist(cloader.library_id,craw))
else:
    print("Failed", craw)

craw = []

if result:
    print(app.create_booklist(cloader.library_id,craw))
else:
    print("Failed", craw)