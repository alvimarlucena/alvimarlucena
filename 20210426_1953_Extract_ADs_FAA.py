import pypyodbc # para conectar a um Access DB
import requests # para baixar um arquivo usando python
import zipfile # para trabalhar com zipfiles
from zipfile import ZipFile
import pandas as pd

url = 'https://rgl.faa.gov/Regulatory_and_Guidance_Library/rgad.nsf/1f3d470805e57a0786257bce004f3976/d7876e8a7bb0e2aa86257beb0051e285/$FILE/AD.zip'
r = requests.get(url, allow_redirects=True)
# carrega o arquivo que se deseja baixar
open('ADES.zip', 'wb').write(r.content) #salva com o nome que eu quero. Leva uns 20 segundos e cospe o tamanho do arquivo em bytes

#"""Extract example .zip file into this directory"""
archive = zipfile.ZipFile('ADES.zip', 'r')
archive.extractall(path=None, members=None, pwd=None)

pypyodbc.lowercase = False

conn = pypyodbc.connect(
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
    r"Dbq=e:\OneDrive\Documentos\LCN Consultoria\Tests on BD\AD.accdb;") # aqui tive que colocar o caminho absoluto do arquivo
# o connect não admitiu só o nome do accdb no Working Folder

cur = conn.cursor()

query = 'SELECT * FROM ADs_by_Model'
dataf = pd.read_sql(query, conn)

select_model = 'A320-111'
dataf[dataf.Model==select_model]

query2 = 'SELECT mk.Make, m.Model, a.ADNumber, a.SupersededBy FROM ((ADs AS a INNER JOIN Models_to_ADs AS mta ON a.AD_ID = mta.AD_ID) INNER JOIN Models AS m ON mta.Model_ID = m.Model_ID) INNER JOIN Makes AS mk ON m.Make_ID = mk.Make_ID'
dataf2 = pd.read_sql(query2, conn)
dataf2[dataf2.Model=='DC-8-41'] #aqui, consigo verificar todas as ADS do DC-8 e checar quais são válidas ainda
