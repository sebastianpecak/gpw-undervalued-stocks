import requests
import re
import xml.etree.ElementTree as ET
import csv

def to_int_or_value(param, value=0):
    try:
        return int(param.strip().replace(" ", ""))
    except:
        return value

def to_float_or_value(param, value=0.0):
    try:
        return float(param.strip().replace(" ", "").replace(",", "."))
    except:
        return value

def take_pbv(entry):
    return entry["price_to_book_value"]

my_headers={'Host':'www.gpw.pl','User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0','Accept':'text/html, */*; q=0.01','Accept-Language':'pl,en-US;q=0.7,en;q=0.3','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','X-Requested-With':'XMLHttpRequest','Origin':'https://www.gpw.pl','Connection':'keep-alive','Referer':'https://www.gpw.pl/spolki'}
my_request="action=GPWCompanySearch&start=ajaxSearch&page=spolki&format=html&lang=PL&letter=&offset=0&limit=1000&order=&order_type=&searchText=&index%5Bempty%5D=on&index%5BWIG20%5D=on&index%5BmWIG40%5D=on&index%5BsWIG80%5D=on&index%5BWIG30%5D=on&index%5BWIG%5D=on&index%5BWIGdiv%5D=on&index%5BWIG-CEE%5D=on&index%5BWIG-Poland%5D=on&index%5BInvestorMS%5D=on&index%5BTBSP.Index%5D=on&index%5BCEEplus%5D=on&index%5BmWIG40TR%5D=on&index%5BNCIndex%5D=on&index%5BsWIG80TR%5D=on&index%5BWIG-banki%5D=on&index%5BWIG-budownictwo%5D=on&index%5BWIG-chemia%5D=on&index%5BWIG-energia%5D=on&index%5BWIG-ESG%5D=on&index%5BWIG-g%C3%B3rnictwo%5D=on&index%5BWIG-informatyka%5D=on&index%5BWIG-leki%5D=on&index%5BWIG-media%5D=on&index%5BWIG-motoryzacja%5D=on&index%5BWIG-nieruchomo%C5%9Bci%5D=on&index%5BWIG-odzie%C5%BC%5D=on&index%5BWIG-paliwa%5D=on&index%5BWIG-spo%C5%BCywczy%5D=on&index%5BWIG-telekomunikacja%5D=on&index%5BWIG-Ukraine%5D=on&index%5BWIG.GAMES%5D=on&index%5BWIG.MS-BAS%5D=on&index%5BWIG.MS-FIN%5D=on&index%5BWIG.MS-PET%5D=on&index%5BWIG20TR%5D=on&index%5BWIG30TR%5D=on&index%5BWIGtech%5D=on&index%5BWIGtechTR%5D=on&sector%5B510%5D=510&sector%5B110%5D=110&sector%5B750%5D=750&sector%5B410%5D=410&sector%5B310%5D=310&sector%5B360%5D=360&sector%5B740%5D=740&sector%5B180%5D=180&sector%5B220%5D=220&sector%5B650%5D=650&sector%5B350%5D=350&sector%5B320%5D=320&sector%5B610%5D=610&sector%5B690%5D=690&sector%5B660%5D=660&sector%5B330%5D=330&sector%5B820%5D=820&sector%5B399%5D=399&sector%5B150%5D=150&sector%5B640%5D=640&sector%5B540%5D=540&sector%5B140%5D=140&sector%5B830%5D=830&sector%5B790%5D=790&sector%5B520%5D=520&sector%5B210%5D=210&sector%5B170%5D=170&sector%5B730%5D=730&sector%5B420%5D=420&sector%5B185%5D=185&sector%5B370%5D=370&sector%5B630%5D=630&sector%5B130%5D=130&sector%5B620%5D=620&sector%5B720%5D=720&sector%5B710%5D=710&sector%5B810%5D=810&sector%5B430%5D=430&sector%5B120%5D=120&sector%5B450%5D=450&sector%5B160%5D=160&sector%5B530%5D=530&sector%5B440%5D=440&country%5BPOLSKA%5D=on&country%5BAUSTRALIA%5D=on&country%5BAUSTRIA%5D=on&country%5BBelgia%5D=on&country%5BBU%C5%81GARIA%5D=on&country%5BCYPR%5D=on&country%5BCZECHY%5D=on&country%5BDANIA%5D=on&country%5BESTONIA%5D=on&country%5BFRANCJA%5D=on&country%5BGLOBAL%5D=on&country%5BGUERNSEY%5D=on&country%5BHISZPANIA%5D=on&country%5BHOLANDIA%5D=on&country%5BINNY%5D=on&country%5BIRLANDIA%5D=on&country%5BKANADA%5D=on&country%5BLITWA%5D=on&country%5BLUKSEMBURG%5D=on&country%5BNIEMCY%5D=on&country%5BNorwegia%5D=on&country%5BREPUBLIKA+CZESKA%5D=on&country%5BS%C5%81OWACJA%5D=on&country%5BS%C5%82owenia%5D=on&country%5BSTANY+ZJEDNOCZONE%5D=on&country%5BSZWAJCARIA%5D=on&country%5BSZWECJA%5D=on&country%5BUKRAINA%5D=on&country%5BW%C4%98GRY%5D=on&country%5BWIELKA+BRYTANIA%5D=on&country%5BW%C5%81OCHY%5D=on&country%5BJERSEY%5D=on&voivodship%5B11%5D=on&voivodship%5B16%5D=on&voivodship%5B5%5D=on&voivodship%5B13%5D=on&voivodship%5B17%5D=on&voivodship%5B7%5D=on&voivodship%5B2%5D=on&voivodship%5B10%5D=on&voivodship%5B8%5D=on&voivodship%5B4%5D=on&voivodship%5B15%5D=on&voivodship%5B9%5D=on&voivodship%5B6%5D=on&voivodship%5B3%5D=on&voivodship%5B12%5D=on&voivodship%5B14%5D=on"
#r = requests.post("https://www.gpw.pl/ajaxindex.php", data=my_request, headers=my_headers)

f = open("response", "r")
aaaaa = f.read()
f.close()

asciidata=aaaaa#r.text#.encode("ascii","ignore")
pos = asciidata.find("<script>")
striped = asciidata[0:pos]
striped = striped.replace("&", " ")
myHtml = '<html>' + striped + '</html>'
root = ET.fromstring(myHtml)

spolki=[]
ind_url="https://www.gpw.pl/ajaxindex.php?start=indicatorsTab&format=html&action=GPWListaSp&gls_isin="

for child in root:
    nazwa = child[0][0][0].text.strip()
    link = child[0][0].attrib["href"]
    isin_pos = link.find("=")
    isin = link[isin_pos+1:]
    spolki.append({"name":nazwa, "isin":isin})

for s in spolki:
    indexes_response = requests.post(ind_url + s["isin"]).text
    indexes_ascii = indexes_response#.encode("ascii","ignore")
    indexes_final = indexes_ascii.replace("&nbsp;", " ")
    indexes_xml = ET.fromstring(indexes_final)
    for index in indexes_xml[0][0]:
        if index[1].text is None:
            continue
        if "Rynek" in index[0].text:
            s["market"] = index[1].text.strip()
        elif "Sektor" in index[0].text:
            s["sector"] = index[1].text.strip()
        elif "Liczba" in index[0].text:
            s["shares_total"] = to_int_or_value(index[1].text, -1)
        elif "rynkowa" in index[0].text:
            s["market_value"] = to_float_or_value(index[1].text)
        elif "ksigowa" in index[0].text:
            s["book_value"] = to_float_or_value(index[1].text)
        elif "C/WK" in index[0].text:
            s["price_to_book_value"] = to_float_or_value(index[1].text)
        elif "C/Z" in index[0].text:
            s["price_to_profit"] = to_float_or_value(index[1].text)

spolki.sort(key=take_pbv)

csv_columns = ['name','isin','market','sector','shares_total','market_value','book_value','price_to_book_value', 'price_to_profit']

try:
    with open("exported_data.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in spolki:
            writer.writerow(data)
except IOError:
    print("I/O error")

print(spolki)
