from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import gspread


page0 = requests.get('https://runtrack.run/running-in/united-states/california')
soup0 = BeautifulSoup(page0.content, 'html.parser')

city_records = []
track_name_records = []
open_to_the_public_records = []
free_entry_records = []
number_of_lanes_records = []
approx_lengths_records = []
location_records = []
url_records = []
working_hours = []
free_of_charge = []
indo = []
info = []
# state = []

area_links = ["https://runtrack.run"+link['href'] for link in soup0.find_all('div', {'class':'right-menu-section'})[10].find_all('a')][:1]

time.sleep(1)

for track_links in area_links:
    page = requests.get(track_links)
    soup = BeautifulSoup(page.content, 'html.parser')
    running_links = []
    # running_links = [running_link['href'] for running_link in soup.find('h3', {'class':'track-color'}).next_sibling.next_sibling.find_all('a')]
    if soup.find('h3', {'class':'track-color'}):
        for running_link in soup.find('h3', {'class':'track-color'}).next_sibling.next_sibling.find_all('a'):
            running_links.append(str(running_link['href']))
    else:
        for running_link in soup.find_all('h3', {'class':'spot-color'})[0].find_next_siblings()[0].find_all('a'):
            running_links.append(str(running_link['href']))

    time.sleep(1)

    for running_link in running_links:

        track_links = ["https://runtrack.run"+running_link for running_link in running_links]
        time.sleep(1)




        for track_link in track_links:

            ''' Sending URL to this function will return with the data'''
            page2 = requests.get(track_link)
            soup2 = BeautifulSoup(page2.content, 'html.parser')


            # The Area.
            city = soup2.select("dt:-soup-contains('Area') + dd")
            if not city or len(city) <= 0:
                city_records.append("N/A")
            else:
                city_records.append(city[0].string)

            # The Track Name.
            if soup2.find('h1'):
                track_name_records.append(soup2.find('h1').string)
            else:
                track_name_records.append(soup2.find('span', class_='sub-headline').string)

            # Open To The Public.
            open_to_the_public = soup2.select("dt:-soup-contains('Open to the public') + dd")
            if open_to_the_public:
                open_to_the_public_records.append(open_to_the_public[0].string)
            elif soup2.select("dt:-soup-contains('Open to the public?') + dd"):
                open_to_the_public_records.append(open_to_the_public[0].string)
            elif len(open_to_the_public) <= 0:
                open_to_the_public_records.append("N/A")

            # Free Entry.
            free_entry = soup2.select("dt:-soup-contains('Free entry') + dd")
            if free_entry:
                free_entry_records.append(free_entry[0].string)
            elif soup2.select("dt:-soup-contains('Free entry?') + dd"):
                free_entry_records.append(free_entry[0].string)
            elif len(free_entry) <= 0:
                free_entry_records.append("N/A")
                

            # Number Of Lanes.
            number_of_lanes = soup2.select("dt:-soup-contains('Number of lanes') + dd")
            if not number_of_lanes or len(number_of_lanes) <= 0:
                number_of_lanes_records.append("N/A")
            elif len(number_of_lanes) >= 1:
                number_of_lanes_records.append(number_of_lanes[0].string)
                

            # Approximate lengths of straights/curves.
            approx_lengths = soup2.select("dt:-soup-contains('Approximate lengths of straights/curves') + dd")
            if not approx_lengths or len(approx_lengths) <= 0:
                if soup2.select("dt:-soup-contains('Length') + dd"):
                    approx_lengths_records.append(soup2.select("dt:-soup-contains('Length') + dd")[0].text)
                approx_lengths_records.append("N/A")
            elif soup2.select("dt:-soup-contains('Length') + dd"):
                approx_lengths_records.append(soup2.select("dt:-soup-contains('Length') + dd")[0].string)
            elif len(approx_lengths) >= 1:
                approx_lengths_records.append(approx_lengths[0].string)


            # Location.
            location = soup2.select("dt:-soup-contains('Location') + dd")
            if not location or len(location) <= 0:
                location_records.append("N/A")
            else:
                location_records.append(location[0].string)

            url_records.append(track_link)

            time.sleep(1)

            # Working hours.
            # working_hours = ''
            if not soup2.select("div:-soup-contains('Reported public hours')"):
                working_hours.append("N/A")
            else:
                target = ' '.join(soup2.select("div:-soup-contains('Reported public hours')")[-1].text.strip().split()[3:])[:-4]
                for char in target:
                    if char.isupper() and target.index(char) != 0:
                        working_hours.append('\n' + f' {char}')
                    else:
                        working_hours.append(char)

            # Free of charge.
            if not soup2.select("dt:-soup-contains('Free of charge') + dd"):
                free_of_charge.append("N/A")
            else:
                free_of_charge.append(soup2.select("dt:-soup-contains('Free of charge') + dd")[0].string.strip())


            # Indoors.
            if not soup2.select("dt:-soup-contains('Indoors') + dd"):
                indo.append("N/A")
            else:
                indo.append(soup2.select("dt:-soup-contains('Indoors') + dd")[0].string.strip())


            # Information.
            if not soup2.select("dt:-soup-contains('Information') + dd"):
                info.append("N/A")
            else:
                start = ''
                end = ''
                lst_info = str(list(soup2.select("dt:-soup-contains('Information') + dd"))[0])
                for indx, char in enumerate(lst_info):
                    if char == ">":
                        start += str(indx+1)
                        continue
                    elif char == "<" and indx != 0:
                        end += str(indx-1)
                        break
                info.append(lst_info[int(start):int(end)+1])


            time.sleep(1)


l1 = city_records
l2 = track_name_records
l3 = approx_lengths_records
l4 = open_to_the_public_records
l5 = free_entry_records
l6 = number_of_lanes_records
l7 = location_records
l8 = url_records
l9 = working_hours
l10 = free_of_charge
l11 = indo
l12 = info
# l13 = state

s1 = pd.Series(l1, name='City')
s2 = pd.Series(l2, name='Track Name')
s3 = pd.Series(l3, name='Approx Length')
s4 = pd.Series(l4, name='Open To The Public')
s5 = pd.Series(l5, name='Free Entry')
s6 = pd.Series(l6, name='Number Of Lanes')
s7 = pd.Series(l7, name='Location')
s8 = pd.Series(l8, name='URL')
s9 = pd.Series(l9, name='Working Hours')
s10 = pd.Series(l10, name='Free Of Charge')
s11 = pd.Series(l11, name='indo')
s12 = pd.Series(l12, name='info')
# s13 = pd.Series(l13, name='State')


df = pd.concat([s1, s2, s3, s5, s6, s7, s8, s9, s10, s11, s12], axis=1)
df.to_csv('example_02.csv', index=False)





print("Data printed successfully.")