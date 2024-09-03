from django.shortcuts import render, redirect
from ManagerRilievoMatricole.forms import TemplateForm, RilievoForm, CronologiaForm
from ManagerRilievoMatricole.functions.functions import (handle_template_file, handle_rilievo_file,
                                                         handle_cronologia_file)
import pandas as pd
from datetime import datetime
from styleframe import StyleFrame
import shutil
from django.http import FileResponse


# Create your views here.
def download_cheatsheet(request):

    response = FileResponse(open('currMap.xlsx', 'rb'), as_attachment=True, filename="currMap.xlsx")
    return response


def carica_cronologia(file_name):

    FileXLSX = pd.read_excel("ManagerRilievoMatricole/static/cronologia/"+file_name+".xlsx", dtype=str, header=None,
                             keep_default_na=False)

    writer = StyleFrame.ExcelWriter('currMap.xlsx', mode='a')
    FileXLSX.to_excel(writer, index=False, header=False, sheet_name='new sheet')

    FileXLSX.to_excel('currMap.xlsx', index=False, header=False)

    FileXLSX.to_excel("currMap.xlsx", index=False, header=False)

    src_dir = "ManagerRilievoMatricole/static/cronologia/"+file_name+".html"
    dst_dir = "currMap.html"
    shutil.copy(src_dir, dst_dir)

    return redirect('index')


def highlight_Refuso2(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    bg_color = None
    # bg_color = 'blue' if (len(val)>0 and val[0:4] != "FILA" and val[0]!="M") else bg_color
    # bg_color = 'red' if val =="Refuso" else bg_color

    color = 'red' if val == "Refuso" else 'black'
    # color = 'white' if (len(val)>0 and val[0]!="M") else color

    out_string = f'background-color: {bg_color}; color: {color}'

    return out_string


def carica_matricole(file_name):

    matricole_da_aggiungere = pd.read_excel("ManagerRilievoMatricole/static/rilievi/"+file_name, dtype=str)

    map = pd.read_excel("currMap.xlsx", dtype=str, header=None, keep_default_na=False)

    for i in range(len(matricole_da_aggiungere.iloc[:, 0])):
        map[map == matricole_da_aggiungere.iloc[i, 0]] = matricole_da_aggiungere.iloc[i, 1]

    # map.style.apply(highlight_Refuso)

    # map.to_html('maps/table.html', index=False, header=False, border=0)
    map = map.style.applymap(highlight_Refuso2)

    Now = datetime.now()
    NowStr = Now.strftime("%Y%m%d_%H%Md%S")

    writer = StyleFrame.ExcelWriter('currMap.xlsx', mode='a')
    map.to_excel(writer, index=False, header=False, sheet_name='new sheet')

    map.to_excel('currMap.xlsx', index=False, header=False)
    map.to_excel('ManagerRilievoMatricole/static/cronologia/table_'+NowStr+'.xlsx', index=False, header=False)

    map.to_html("ManagerRilievoMatricole/templates/ManagerRilievoMatricole/currMap.html", border=0, index=False,
                header=False)
    map.to_html("ManagerRilievoMatricole/static/cronologia/table_"+NowStr+".html", border=0, index=False, header=False)
    history = pd.read_csv("ManagerRilievoMatricole/static/cronologia/history.csv")

    new_df = pd.DataFrame({"timestamp": Now, "filename": "ManagerRilievoMatricole/static/cronologia/table_" +
                                                         NowStr+".html", "name": Now.strftime("%d_%m_%Y %H:%M")},
                          index=[0])
    new_history = pd.concat([history, new_df])
    new_history.to_csv("ManagerRilievoMatricole/static/cronologia/history.csv", index=False)

    return redirect('index')


def carica_template(file_name):

    File = pd.read_excel("ManagerRilievoMatricole/static/planimetrie/"+file_name, dtype=str, header=None,
                         keep_default_na=False)
    File.to_html("ManagerRilievoMatricole/templates/ManagerRilievoMatricole/currMap.html", index=False, header=False,
                 border=0)
    File.to_excel("currMap.xlsx", index=False, header=False)

    return redirect('index')


def index2(request):

    # print(request.POST['pitcher'])
    history = pd.read_csv("ManagerRilievoMatricole/static/cronologia/history.csv")

    filename = history["filename"][history["name"] == request.POST['pitcher']].iloc[0]
    print(filename)
    print(type(filename))

    end_file = "ManagerRilievoMatricole/templates/ManagerRilievoMatricole/currMap.html"
    shutil.copy(filename, end_file)

    return redirect('index')


def index(request):

    print('sono in index')
    template_path = "ManagerRilievoMatricole/templates/ManagerRilievoMatricole/currMap.html"

    # if request.POST["template"] == "template":
    #     template_path = "ManagerRilievoMatricole/templates/ManagerRilievoMatricole/currMap.html"
    history = pd.read_csv("ManagerRilievoMatricole/static/cronologia/history.csv")
    # print("history: " +history["name"])

    if request.method == 'POST':
        Template = TemplateForm(request.POST, request.FILES)
        Rilievo = RilievoForm(request.POST, request.FILES)
        Cronologia = CronologiaForm(request.POST, request.FILES)

        if "TempSub" in request.POST:
            if Template.is_valid():
                StoredFile = handle_template_file(request.FILES['file'])
                carica_template(StoredFile)
        elif "MatrSub" in request.POST:
            if Rilievo.is_valid():
                StoredFile = handle_rilievo_file(request.FILES['file'])
                carica_matricole(StoredFile)

        else:
            if Cronologia.is_valid():
                StoredFile = handle_cronologia_file(request.FILES['file'])
                carica_cronologia(StoredFile)

    else:
        Template = TemplateForm()
        Rilievo = RilievoForm()
        # Cronologia = CronologiaForm()

    with open(template_path, 'r') as f:
        map_html = f.read()

    return render(request, "ManagerRilievoMatricole/index.html", {
        'Tempform': Template, "map": map_html, 'RilForm': Rilievo, "history": history["name"]
    })
