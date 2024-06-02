import requests
import json
import prettytable


if __name__=='__main__':
    #Getting parameters for API URL
    keyFile = open("registrationkey.txt", 'r')
    registrationKey = keyFile.read()


    #url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/?' + registrationKey

    #Code prefix seems to be OE, UM or US?
    #ex. OEUM001058000000029203313 ("Annual median wage for Nuclear Medicine Technologists in All Industries in Albany-Schenectady-Troy, NY")

    #Retrieving data
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": ['CUUR0000SA0','SUUR0000SA0'],"startyear":"2023", "endyear":"2023", "registrationkey": registrationKey})
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)

    #Displaying retrieved data in a table
    for series in json_data['Results']['series']:
        x=prettytable.PrettyTable(["series id","year","period","value","footnotes"])
        seriesId = series['seriesID']
        for item in series['data']:
            year = item['year']
            period = item['period']
            value = item['value']
            footnotes=""
            for footnote in item['footnotes']:
                if footnote:
                    footnotes = footnotes + footnote['text'] + ','
        
            if 'M01' <= period <= 'M12':
                x.add_row([seriesId,year,period,value,footnotes[0:-1]])
        output = open(seriesId + '.txt','w')
        output.write (x.get_string())
        output.close()

