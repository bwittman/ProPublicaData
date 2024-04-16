import json
import httplib2
import time

BASE_URI = 'https://projects.propublica.org/nonprofits/api/v2/'

states = {'AL' : 'Alabama', 'AK' : 'Alaska', 'AZ' : 'Arizona', 'AR' : 'Arkansas', 'AS' : 'American Samoa', 'CA' : 'California', 'CO' : 'Colorado', 'CT' : 'Connecticut', 'DE' : 'Delaware', 'DC' : 'District of Columbia', 'FL' : 'Florida', 'GA' : 'Georgia', 'GU' : 'Guam', 'HI' : 'Hawaii', 'ID' : 'Idaho', 'IL' : 'Illinois', 'IN' : 'Indiana', 'IA' : 'Iowa', 'KS' : 'Kansas', 'KY' : 'Kentucky', 'LA' : 'Louisiana', 'ME' : 'Maine', 'MD' : 'Maryland', 'MA' : 'Massachusetts', 'MI' : 'Michigan', 'MN' : 'Minnesota', 'MS' : 'Mississippi', 'MO' : 'Missouri', 'MT' : 'Montana', 'NE' : 'Nebraska', 'NV' : 'Nevada', 'NH' : 'New Hampshire', 'NJ' : 'New Jersey', 'NM' : 'New Mexico', 'NY' : 'New York', 'NC' : 'North Carolina', 'ND' : 'North Dakota', 'MP' : 'Northern Mariana Islands', 'OH' : 'Ohio', 'OK' : 'Oklahoma', 'OR' : 'Oregon', 'PA' : 'Pennsylvania', 'PR' : 'Puerto Rico', 'RI' : 'Rhode Island', 'SC' : 'South Carolina', 'SD' : 'South Dakota', 'TN' : 'Tennessee', 'TX' : 'Texas', 'TT' : 'Trust Territories', 'UT' : 'Utah', 'VT' : 'Vermont', 'VA' : 'Virginia', 'VI' : 'Virgin Islands', 'WA' : 'Washington', 'WV' : 'West Virginia', 'WI' : 'Wisconsin', 'WY' : 'Wyoming'}
schoolTypes = {'university', 'college', 'institute', 'academy'}


http = httplib2.Http('.cache')

for abbreviation in states:    
    fileName = '-'.join(states[abbreviation].lower().split()) + '.json'
    with open(fileName, 'w') as output:
        first = True
        results = 0
        output.write('{ "organizations": [\n')
        for type in schoolTypes:
            url = f'{BASE_URI}search.json?q={type}&state%5Bid%5D={abbreviation}'
            print(url)
            resp, content = http.request(url)
            if not resp.get('status') == '200':
                print('Error getting ' + url)
            else:
                data = json.loads(content) # turns JSON string into Python
                pages = data['num_pages']
                results += data['total_results']                
                
                for page in range(pages):
                    time.sleep(1) # sleep a second between calls to give the server breathing room
                    url = f'{BASE_URI}search.json?q={type}&state%5Bid%5D={abbreviation}&page={page}'
                    resp, content = http.request(url)                    
                    data = json.loads(content) # turns JSON string into Python
                    for organization in data['organizations']:
                        if first:
                            first = False
                        else:
                            output.write(',\n')
                        output.write('{')
                        output.write(f'"ein": {organization["ein"]}, ')
                        output.write(f'"name": "{organization["name"]}", ')
                        output.write(f'"city": "{organization["city"]}"')
                        output.write('}')                
        output.write('\n],\n"total_results": ' + str(results) + '}\n')