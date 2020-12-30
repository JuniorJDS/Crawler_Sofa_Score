# -*- coding: utf-8 -*-
import scrapy
import json
import pandas as pd
from datetime import  date
from collections import defaultdict
#from mongo_connection import db


class sofa_scoure(scrapy.Spider):
    name = 'brasileirao2019_serieA'

    #page number
    pag_num_attack = 1
    pag_num_deffence = 1
    pag_num_passing = 1

    estatistic_data_attack = []
    estatistic_data_deffence = []
    estatistic_data_passing = []
    estatistic_data_goalkeeper = []

    def start_requests(self):

        url_attack = 'https://www.sofascore.com/api/v1/unique-tournament/325/season/22931/statistics?fields=goals%2C' \
                     'bigChancesMissed%2CsuccessfulDribbles%2CtotalShots%2CgoalConversionPercentage%2Crating&group=attack&' \
                     'accumulation=total&order=-rating&offset=0&limit=100&_=1573312147'

        url_deffence = 'https://www.sofascore.com/api/v1/unique-tournament/325/season/22931/statistics?fields=tackles%2C' \
                     'interceptions%2Cclearances%2CerrorLeadToGoal%2CblockedShots%2Crating&group=defence&accumulation=total&' \
                     'order=-rating&offset=0&limit=100&_=1573522360'

        url_passing = 'https://www.sofascore.com/api/v1/unique-tournament/325/season/22931/statistics?fields=bigChancesCreated%2C' \
                      'assists%2CaccuratePasses%2CaccuratePassesPercentage%2CkeyPasses%2Crating&group=passing&accumulation=total&' \
                      'order=-rating&offset=0&limit=100&_=1573590527'

        url_goalkeeper = 'https://www.sofascore.com/api/v1/unique-tournament/325/season/22931/statistics?filters=position.in.G&fields=saves%2C' \
                         'cleanSheet%2CpenaltySave%2CsavedShotsFromInsideTheBox%2CrunsOut%2Crating&group=goalkeeper&' \
                         'accumulation=total&order=-rating&offset=0&limit=100&_=1573607570'

        yield scrapy.http.Request(url=url_attack,
                                  method='GET',
                                  callback=self.parse_attack)

        yield scrapy.http.Request(url=url_deffence,
                                  method='GET',
                                  callback=self.parse_deffence)

        yield scrapy.http.Request(url=url_passing,
                                  method='GET',
                                  callback=self.parse_passing)

        yield scrapy.http.Request(url=url_goalkeeper,
                                  method='GET',
                                  callback=self.parse_goalkeeper)

    def parse_attack(self, response):

        for i in range(len(json.loads(response.body_as_unicode())['results'])):
            sofa_scoure.estatistic_data_attack.append({
                "name": json.loads(response.body_as_unicode())['results'][i]['player']['name'],
                "team": json.loads(response.body_as_unicode())['results'][i]['team']['slug'],
                "goals": int(json.loads(response.body_as_unicode())['results'][i]['goals']),
                "big_chances_missed": int(json.loads(response.body_as_unicode())['results'][i]['bigChancesMissed']),
                "success_ful_dribbles": int(json.loads(response.body_as_unicode())['results'][i]['successfulDribbles']),
                "total_shots": int(json.loads(response.body_as_unicode())['results'][i]['totalShots']),
                "goal_conversion_percentage": float(json.loads(response.body_as_unicode())['results'][i]['goalConversionPercentage']),
                "rating": float(json.loads(response.body_as_unicode())['results'][i]['rating']),
                "league": str('A/2019')
            })

        next_page = 'https://www.sofascore.com/api/v1/unique-tournament/325/season/22931/statistics?fields=goals%2C' \
                     'bigChancesMissed%2CsuccessfulDribbles%2CtotalShots%2CgoalConversionPercentage%2Crating&group=attack&' \
                     'accumulation=total&order=-rating&offset=' + str(sofa_scoure.pag_num_attack * 100) + '&limit=100&_=1573312147'

        if sofa_scoure.pag_num_attack < 8:
            sofa_scoure.pag_num_attack += 1
            yield response.follow(next_page, callback=self.parse_attack)

        else:

            data = defaultdict(dict)
            for l in (sofa_scoure.estatistic_data_attack, sofa_scoure.estatistic_data_deffence, sofa_scoure.estatistic_data_passing, sofa_scoure.estatistic_data_goalkeeper):
                for elem in l:
                    data[elem['name'], elem['team'], elem['rating']].update(elem)

            #Save in bd and/or in csv
            #db.sofa_score_data.insert_many(data.values())
            Data = pd.DataFrame(data).T
            Data.to_csv('brasileirao_2019A.csv', index=False)

    def parse_deffence(self, response):

        for i in range(len(json.loads(response.body_as_unicode())['results'])):
            sofa_scoure.estatistic_data_deffence.append({
                "name": json.loads(response.body_as_unicode())['results'][i]['player']['name'],
                "team": json.loads(response.body_as_unicode())['results'][i]['team']['slug'],
                "tackles": int(json.loads(response.body_as_unicode())['results'][i]['tackles']),
                "interceptions": int(json.loads(response.body_as_unicode())['results'][i]['interceptions']),
                "clearances": int(json.loads(response.body_as_unicode())['results'][i]['clearances']),
                "error_lead_to_goal": int(json.loads(response.body_as_unicode())['results'][i]['errorLeadToGoal']),
                "blocked_shots": int(json.loads(response.body_as_unicode())['results'][i]['blockedShots']),
                "rating": float(json.loads(response.body_as_unicode())['results'][i]['rating'])

            })

        next_page_deff = 'https://www.sofascore.com/api/v1/unique-tournament/325/season/22931/statistics?fields=tackles%2C' \
                     'interceptions%2Cclearances%2CerrorLeadToGoal%2CblockedShots%2Crating&group=defence&accumulation=total&' \
                     'order=-rating&offset=' + str(sofa_scoure.pag_num_deffence * 100) + '&limit=100&_=1573522360'

        if sofa_scoure.pag_num_deffence < 8:

            sofa_scoure.pag_num_deffence += 1
            yield response.follow(next_page_deff, callback=self.parse_deffence)

    def parse_passing(self, response):

        for i in range(len(json.loads(response.body_as_unicode())['results'])):
            sofa_scoure.estatistic_data_passing.append({
                "name": json.loads(response.body_as_unicode())['results'][i]['player']['name'],
                "team": json.loads(response.body_as_unicode())['results'][i]['team']['slug'],
                "bigChancesCreated": int(json.loads(response.body_as_unicode())['results'][i]['bigChancesCreated']),
                "assists": int(json.loads(response.body_as_unicode())['results'][i]['assists']),
                "accuratePasses": int(json.loads(response.body_as_unicode())['results'][i]['accuratePasses']),
                "accuratePassesPercentage": int(json.loads(response.body_as_unicode())['results'][i]['accuratePassesPercentage']),
                "keyPasses": int(json.loads(response.body_as_unicode())['results'][i]['keyPasses']),
                "rating": float(json.loads(response.body_as_unicode())['results'][i]['rating'])

            })

        next_page_pass = 'https://www.sofascore.com/api/v1/unique-tournament/325/season/22931/statistics?fields=bigChancesCreated%2C' \
                      'assists%2CaccuratePasses%2CaccuratePassesPercentage%2CkeyPasses%2Crating&group=passing&accumulation=total&' \
                      'order=-rating&offset=' + str(sofa_scoure.pag_num_passing * 100) + '&limit=100&_=1573590527'

        if sofa_scoure.pag_num_passing < 8:

            sofa_scoure.pag_num_passing += 1
            yield response.follow(next_page_pass, callback=self.parse_passing)

    def parse_goalkeeper(self, response):

        for i in range(len(json.loads(response.body_as_unicode())['results'])):
            sofa_scoure.estatistic_data_goalkeeper.append({
                "name": json.loads(response.body_as_unicode())['results'][i]['player']['name'],
                "team": json.loads(response.body_as_unicode())['results'][i]['team']['slug'],
                "saves": int(json.loads(response.body_as_unicode())['results'][i]['saves']),
                "penalty_save": int(json.loads(response.body_as_unicode())['results'][i]['penaltySave']),
                "saved_shots_from_inside_the_box": int(json.loads(response.body_as_unicode())['results'][i]['savedShotsFromInsideTheBox']),
                "runs_out": int(json.loads(response.body_as_unicode())['results'][i]['runsOut']),
                "rating": float(json.loads(response.body_as_unicode())['results'][i]['rating'])

            })
