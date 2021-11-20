from selenium import webdriver
import time
import requests
import bs4
import csv

moment_links=[]

def get_moment_urls(account):
    driver = webdriver.Chrome()
    driver.get('https://nbatopshot.com/user/@'+account+'/moments')
    
    scroll_pause = 1
    current_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == current_height:
            break
        current_height = new_height
    
    link_grab=driver.find_elements_by_tag_name("a")
    for link in link_grab:
       link = link.get_attribute('href')
       if str(link).startswith('https://nbatopshot.com/moment/'):
           moment_links.append(link[-36:])
           
get_moment_urls(str(input("Enter your account handle: ")))
           
series_dict = {'1':'Series 1', '2':'Series 2', '3':'Summer 2021', '4':'Series 3'}
position_dict = {'C':'Center', 'PF':'Power Forward', 'SF':'Small Forward', 'SG':'Shooting Guard', 'PG':'Point Guard'}

attributes = ('Player', 'League', 'Set', 'Rarity', 'Series', 'Serial', 'Total Serial', 'Play Type', 'Team', 'Jersey', 'Position', 'Badges', 'Challenge Reward?', 'Moment Date', 'Purchased By', 'Cost', 'Acquisition Method', 'Purchase Date', 'Payment Method', 'URL')

write = open('topshot.txt', 'a', newline='', encoding='utf8')
writer = csv.writer(write)
writer.writerow(attributes)

for link in moment_links:
    url = 'https://nbatopshot.com/moment/'+link
    html = requests.get(url)
    moment_info = bs4.BeautifulSoup(html.text,'lxml')
    url_ident = url[-36:]
    moment_ident=url_ident
    
    player_name = str(moment_info.find('meta', property='og:title'))
    player_name = ' '.join(player_name.split()[4:6])
        
    league = str(moment_info.find('script', id='__NEXT_DATA__'))
    league = [word for word in (league.split('league":"'))]
    league = (league[1][0:(league[1].index('"'))])
    
    set_name = str(moment_info.find('script', id='__NEXT_DATA__'))
    set_name = [word for word in (set_name.split('flowName":"'))]
    set_name = (set_name[1][0:(set_name[1].index('"'))])
    
    series_tier = str(moment_info.find('meta', property='og:image'))
    if 'fandom' in series_tier:
        tier = 'Fandom'
    elif 'rare' in series_tier:
        tier = 'Rare'
    elif 'ultimate' in series_tier:
        tier = 'Ultimate'
    elif 'legendary' in series_tier:
        tier = 'Legendary'
    else:
        tier = 'Common'
    
    series = series_tier[54]
    series = (series_dict[series])
    
    serial = str(moment_info.find('script', id='__NEXT_DATA__'))
    serial = [word for word in (serial.split('flowSerialNumber":"'))]
    serial = int(serial[1][0:(serial[1].index('"'))])
    
    total_serial = str(moment_info.find('script', id='__NEXT_DATA__'))
    total_serial = [word for word in (total_serial.split('"circulationCount":'))]
    total_serial = int(total_serial[1][0:(total_serial[1].index(','))])
    
    play_type = str(moment_info.find('script', id='__NEXT_DATA__'))
    play_type = [word for word in (play_type.split('playCategory":"'))]
    play_type = (play_type[1][0:(play_type[1].index('"'))])
    
    team = str(moment_info.find('script', id='__NEXT_DATA__'))
    team = [word for word in (team.split('teamAtMoment":"'))]
    team = (team[1][0:(team[1].index('"'))])
    
    jersey = str(moment_info.find('script', id='__NEXT_DATA__'))
    jersey = [word for word in (jersey.split('jerseyNumber":"'))]
    jersey = (jersey[1][0:(jersey[1].index('"'))])
    
    position = str(moment_info.find('script', id='__NEXT_DATA__'))
    position = [word for word in (position.split('primaryPosition":"'))]
    position = position_dict[(position[1][0:(position[1].index('"'))])]
    
    badges = []
    badge = str(moment_info.find('script', id='__NEXT_DATA__'))
    if '"title":"Rookie Mint"' in badge:
        badges.append('Rookie Mint')
    if '"title":"Rookie Year"' in badge:
        badges.append('Rookie Year')
    if '"title":"Rookie Premiere"' in badge:
        badges.append('Rookie Premiere')
    if '"title":"Top Shot Debut"' in badge:
        badges.append('Top Shot Debut')
    if '"title":"Championship Year"' in badge:
        badges.append('Championship Year')
    if '"title":"Challenge Reward"' in badge:
        badges.append('Challenge Reward')
    if len(badges)==0:
        badges.append('None')
    
    if 'Challenge Reward' in badges:
        challenge_reward = True
    else:
        challenge_reward = False
    
    moment_date = str(moment_info.find('script', id='__NEXT_DATA__'))
    moment_date = [word for word in (moment_date.split('dateOfMoment":"'))]
    moment_date = (moment_date[1][0:(moment_date[1].index('T'))])
 
    new_info = (player_name, league, set_name, tier, series, serial, total_serial, play_type, team, jersey, position, badges, challenge_reward, moment_date, moment_ident)
    writer.writerow(new_info)
write.close()
