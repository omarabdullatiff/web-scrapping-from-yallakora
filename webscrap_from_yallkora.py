import csv
import requests
from bs4 import BeautifulSoup


date = input("Enter the date in this format mm/d/yyyy: ")
page = requests.get(f'https://www.yallakora.com/match-center/?date=2/15/2025')

def main(page):
    src = page.content
    soup = BeautifulSoup(src,'lxml')
    match_Details = []

    championShips = soup.find_all('div', {'class': 'matchCard'})

    def getMatchInfo(championShips):
        championShip_title = championShips.contents[1].find('h2').text.strip()

        allMatches = championShips.contents[3].find_all('li')
        
        numOfMatches = len(allMatches)

        for i in range(numOfMatches):
            # Get teams name
            teamA = allMatches[i].find('div', {'class': 'teamA'}).text.strip()
            teamB = allMatches[i].find('div', {'class': 'teamB'}).text.strip()
            
            # Get score of matches
            matchScore = allMatches[i].find('div', {'class': 'MResult'}).find_all('span', {'class': 'score'})
            score = f"{matchScore[0].text.strip()} - {matchScore[1].text.strip()}"

            # Get match time
            matchTime = allMatches[i].find('div', {'class':'MResult'}).find('span', {'class': 'time'}).text.strip()
            
            # Save previous info
            match_Details.append({
                "Championship name": championShip_title,
                "1st team": teamA,
                "2nd team": teamB,
                "Score": score,
                "Time": matchTime
            })

    for i in range(len(championShips)):
         getMatchInfo(championShips[i])
    
    
    key =  match_Details[0].keys()

    with open("/Users/Omar/Desktop/DE/matches_details.csv", 'w') as finalResult:
        dictWriter = csv.DictWriter(finalResult , key)
        dictWriter.writerows(match_Details)

        

main(page)