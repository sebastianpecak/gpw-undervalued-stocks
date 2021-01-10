import requests
import re
import xml.etree.ElementTree as ET
import csv

# If debug mode is enabled then we do not fetch data from GPW server.
IS_DEBUG_MODE = True
INDEXES_URL   = "https://www.gpw.pl/ajaxindex.php?start=indicatorsTab&format=html&action=GPWListaSp&gls_isin="

def to_int_or_value(param, value=0):
    try:
        return int(param.replace(" ", ""))
    except:
        return value

def to_float_or_value(param, value=0.0):
    try:
        return float(param.replace(" ", "").replace(",", "."))
    except:
        return value

def take_pbv(entry):
    return entry["price_to_book_value"]

def get_companies_list_from_file():
    listFile = open("all_gpw_companies.list", "r")
    result   = listFile.read()
    listFile.close()
    return result

def get_companies_list_from_server():
    custom_headers = {'Host':'www.gpw.pl','User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0','Accept':'text/html, */*; q=0.01','Accept-Language':'pl,en-US;q=0.7,en;q=0.3','Accept-Encoding':'gzip, deflate, br','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','X-Requested-With':'XMLHttpRequest','Origin':'https://www.gpw.pl','Connection':'keep-alive','Referer':'https://www.gpw.pl/spolki'}
    custom_request = "action=GPWCompanySearch&start=ajaxSearch&page=spolki&format=html&lang=PL&letter=&offset=0&limit=1000&order=&order_type=&searchText=&index%5Bempty%5D=on&index%5BWIG20%5D=on&index%5BmWIG40%5D=on&index%5BsWIG80%5D=on&index%5BWIG30%5D=on&index%5BWIG%5D=on&index%5BWIGdiv%5D=on&index%5BWIG-CEE%5D=on&index%5BWIG-Poland%5D=on&index%5BInvestorMS%5D=on&index%5BTBSP.Index%5D=on&index%5BCEEplus%5D=on&index%5BmWIG40TR%5D=on&index%5BNCIndex%5D=on&index%5BsWIG80TR%5D=on&index%5BWIG-banki%5D=on&index%5BWIG-budownictwo%5D=on&index%5BWIG-chemia%5D=on&index%5BWIG-energia%5D=on&index%5BWIG-ESG%5D=on&index%5BWIG-g%C3%B3rnictwo%5D=on&index%5BWIG-informatyka%5D=on&index%5BWIG-leki%5D=on&index%5BWIG-media%5D=on&index%5BWIG-motoryzacja%5D=on&index%5BWIG-nieruchomo%C5%9Bci%5D=on&index%5BWIG-odzie%C5%BC%5D=on&index%5BWIG-paliwa%5D=on&index%5BWIG-spo%C5%BCywczy%5D=on&index%5BWIG-telekomunikacja%5D=on&index%5BWIG-Ukraine%5D=on&index%5BWIG.GAMES%5D=on&index%5BWIG.MS-BAS%5D=on&index%5BWIG.MS-FIN%5D=on&index%5BWIG.MS-PET%5D=on&index%5BWIG20TR%5D=on&index%5BWIG30TR%5D=on&index%5BWIGtech%5D=on&index%5BWIGtechTR%5D=on&sector%5B510%5D=510&sector%5B110%5D=110&sector%5B750%5D=750&sector%5B410%5D=410&sector%5B310%5D=310&sector%5B360%5D=360&sector%5B740%5D=740&sector%5B180%5D=180&sector%5B220%5D=220&sector%5B650%5D=650&sector%5B350%5D=350&sector%5B320%5D=320&sector%5B610%5D=610&sector%5B690%5D=690&sector%5B660%5D=660&sector%5B330%5D=330&sector%5B820%5D=820&sector%5B399%5D=399&sector%5B150%5D=150&sector%5B640%5D=640&sector%5B540%5D=540&sector%5B140%5D=140&sector%5B830%5D=830&sector%5B790%5D=790&sector%5B520%5D=520&sector%5B210%5D=210&sector%5B170%5D=170&sector%5B730%5D=730&sector%5B420%5D=420&sector%5B185%5D=185&sector%5B370%5D=370&sector%5B630%5D=630&sector%5B130%5D=130&sector%5B620%5D=620&sector%5B720%5D=720&sector%5B710%5D=710&sector%5B810%5D=810&sector%5B430%5D=430&sector%5B120%5D=120&sector%5B450%5D=450&sector%5B160%5D=160&sector%5B530%5D=530&sector%5B440%5D=440&country%5BPOLSKA%5D=on&country%5BAUSTRALIA%5D=on&country%5BAUSTRIA%5D=on&country%5BBelgia%5D=on&country%5BBU%C5%81GARIA%5D=on&country%5BCYPR%5D=on&country%5BCZECHY%5D=on&country%5BDANIA%5D=on&country%5BESTONIA%5D=on&country%5BFRANCJA%5D=on&country%5BGLOBAL%5D=on&country%5BGUERNSEY%5D=on&country%5BHISZPANIA%5D=on&country%5BHOLANDIA%5D=on&country%5BINNY%5D=on&country%5BIRLANDIA%5D=on&country%5BKANADA%5D=on&country%5BLITWA%5D=on&country%5BLUKSEMBURG%5D=on&country%5BNIEMCY%5D=on&country%5BNorwegia%5D=on&country%5BREPUBLIKA+CZESKA%5D=on&country%5BS%C5%81OWACJA%5D=on&country%5BS%C5%82owenia%5D=on&country%5BSTANY+ZJEDNOCZONE%5D=on&country%5BSZWAJCARIA%5D=on&country%5BSZWECJA%5D=on&country%5BUKRAINA%5D=on&country%5BW%C4%98GRY%5D=on&country%5BWIELKA+BRYTANIA%5D=on&country%5BW%C5%81OCHY%5D=on&country%5BJERSEY%5D=on&voivodship%5B11%5D=on&voivodship%5B16%5D=on&voivodship%5B5%5D=on&voivodship%5B13%5D=on&voivodship%5B17%5D=on&voivodship%5B7%5D=on&voivodship%5B2%5D=on&voivodship%5B10%5D=on&voivodship%5B8%5D=on&voivodship%5B4%5D=on&voivodship%5B15%5D=on&voivodship%5B9%5D=on&voivodship%5B6%5D=on&voivodship%5B3%5D=on&voivodship%5B12%5D=on&voivodship%5B14%5D=on"
    response = requests.post("https://www.gpw.pl/ajaxindex.php", data=custom_request, headers=custom_headers)
    return response.text

def get_companies_list_xml():
    if IS_DEBUG_MODE is True:
        companies_list = get_companies_list_from_file()
    else:
        companies_list = get_companies_list_from_server()
    # Remove unwanted parts from response.
    script_pos = companies_list.find("<script>")
    companies_list = companies_list[0:script_pos]
    companies_list = companies_list.replace("&", "").replace("\t", "").replace("\n", "").replace("\r", "").strip()
    companies_list_html = '<html>' + companies_list + '</html>'
    return ET.fromstring(companies_list_html)

def parse_companies_list_xml(xml_tree):
    parsed_companies = []
    for child in xml_tree:
        company_name = child[0][0][0].text.strip()
        link         = child[0][0].attrib["href"]
        isin_pos     = link.find("=") + 1
        isin         = link[isin_pos:]
        parsed_companies.append({"name":company_name, "isin":isin})
    return parsed_companies

def get_company_indexes_from_file(company_isin):
    indexes_file    = open("cache/" + company_isin, "r")
    company_indexes = indexes_file.read()
    indexes_file.close()
    return company_indexes

def get_company_indexes_from_server(company_isin):
    indexes_response = requests.post(INDEXES_URL + company_isin).text
    return indexes_response

def get_company_indexes_xml(company_isin):
    if IS_DEBUG_MODE is True:
        company_indexes = get_company_indexes_from_file(company_isin)
    else:
        company_indexes = get_company_indexes_from_server(company_isin)
    # Remove unwanted parts from response.
    company_indexes = company_indexes.replace("&nbsp;", "").replace("&", "").replace("\t", "").replace("\n", "").replace("\r", "").strip()
    return ET.fromstring(company_indexes)

def get_parsed_company_indexes(indexes_xml):
    parsed_indexes = {}
    for index in indexes_xml[0][0]:
        if index[1].text is None:
            continue
        key   = index[0].text.strip()
        value = index[1].text.strip()
        if "Rynek" in key:
            parsed_indexes["market"] = value
        elif "Sektor" in key:
            parsed_indexes["sector"] = value
        elif "Liczba" in key:
            parsed_indexes["shares_total"] = to_int_or_value(value, -1)
        elif "rynkowa" in key:
            parsed_indexes["market_value_pln"] = to_float_or_value(value)
            # Check unit.
            if 'mln zł' in key:
                parsed_indexes["market_value_pln"] *= 1000000
        elif "księgowa" in key:
            parsed_indexes["book_value_pln"] = to_float_or_value(value)
            # Check unit.
            if 'mln zł' in key:
                parsed_indexes["book_value_pln"] *= 1000000
        elif "C/WK" in key:
            # Calculate P/BV index if needed.
            if 'x' in value and parsed_indexes["book_value_pln"] != 0:
                parsed_indexes["price_to_book_value"] = parsed_indexes["market_value_pln"] / parsed_indexes["book_value_pln"]
            else:
                parsed_indexes["price_to_book_value"] = to_float_or_value(value)
                if parsed_indexes["book_value_pln"] == 0:
                    current_annotation_value = ''
                    if 'annotation' in parsed_indexes:
                        current_annotation_value = parsed_indexes['annotation'] + ' '
                    parsed_indexes['annotation'] = current_annotation_value + key + ': Book value is zero.'
        elif "C/Z" in key:
            parsed_indexes["price_to_profit"] = to_float_or_value(value)
            # Annotate if needed.
            if 'x' in value:
                current_annotation_value = ''
                if 'annotation' in parsed_indexes:
                    current_annotation_value = parsed_indexes['annotation'] + ' '
                parsed_indexes["annotation"] = current_annotation_value + key + ': Unknown special value \'' + value + '\'.'
    return parsed_indexes

def get_all_indexes(companies_list):
    for company in companies_list:
        indexes_xml    = get_company_indexes_xml(company['isin'])
        parsed_indexes = get_parsed_company_indexes(indexes_xml)
        company.update(parsed_indexes)
    return companies_list

def export_sorted_data_to_csv(companies_list, file_name):
    companies_list.sort(key=take_pbv)
    csv_columns = ['name','isin','market','sector','shares_total','market_value_pln','book_value_pln','price_to_book_value', 'price_to_profit', 'annotation']
    try:
        with open(file_name, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in companies_list:
                writer.writerow(data)
    except IOError:
        print("I/O error")

# Main program.
# Get list of all the companies listed on GPW.
# Get all the indexes for all the companies.
# Make a list of companies sorted by P/BV (ascending).
def main():
    all_companies_xml = get_companies_list_xml()
    companies_list    = parse_companies_list_xml(all_companies_xml)
    companies_list    = get_all_indexes(companies_list)
    export_sorted_data_to_csv(companies_list, "exported_data.csv")

if __name__ == "__main__":
    main()
