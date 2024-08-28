from datetime import datetime


def handle_template_file(f):

    Now = datetime.now()
    NowString = Now.strftime("%Y%m%d%H%M%S")

    StoredFile = f.name[0:-5]+"_"+NowString+".xlsx"

    with open('ManagerRilievoMatricole/static/planimetrie/'+StoredFile, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return StoredFile


def handle_rilievo_file(f):

    Now = datetime.now()
    NowString = Now.strftime("%Y%m%d%H%M%S")
    StoredFile = f.name[0:-5]+"_"+NowString+".xlsx"

    with open('ManagerRilievoMatricole/static/rilievi/'+StoredFile, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return StoredFile


def handle_cronologia_file(f):

    Now = datetime.now()
    NowString = Now.strftime("%Y%m%d%H%M%S")
    StoredFile = f.name[0:-5]+"_"+NowString+".html"

    with open('ManagerRilievoMatricole/static/cronologia/'+StoredFile, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return f.name[0:-5]
