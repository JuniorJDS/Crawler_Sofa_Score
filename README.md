# Sofa Score Crawler Brazilian Football 2019

> The purpose of this crawler is access the site [Sofa Score](https://www.sofascore.com/tournament/football/brazil/brasileiro-serie-a/325) and extract the public  data of the soccer players at brazilian league (Brasileirão Serie A and Brasileirão Serie B).

The data contains:
- **Attack** - Goals, Big chances missed, Successful dribbles, Total shots, Percent of Goal conversion
- **Defence** - Tackles, Interceptions,	Clearances,	Errors lead to goal,	Blocked shots
- **Passing** - Big chances created, Assists,	Accurate passes,	Percent of Accurate passes,	Key passes
- **Goalkeeper** - Saves,	Clean sheets,	Penalties saved,	Saved shots from inside the box,	Runs out,	Rating


![Exemple Of Images](https://github.com/JuniorJDS/Crowler_Sofa_Score/blob/master/sofa_score_Attack.png)

## Project Structure
``` 
├── Crawler_Sofa_Score
    ├── Sofa_Score                   
    │   ├── spiders
    │       ├── __init__.py
    │       ├── sofa_scoure_2019A.py        # spider to brasileirao 2019 serie A
    │       ├── sofa_scoure_2019B.py        # spider to brasileirao 2019 serie B
    │   ├── _init__.py
    │   ├── items.py
    │   ├── middlewares.py
    │   ├── pipelines.py         
    │   └── settings.py
    ├── README.md
    ├── requirements.txt
    ├── scrapy.cfg                   
    └── ...
```
## How to run our spider
Install the virtual environment and requirements:
``` 
    python3 -m venv venv

    source plataforma_venv/bin/activate

    pip3 install --upgrade pip

    pip3 install -r requirements.txt
```
To put our spider to work, go to the project’s top level directory and run:
```
scrapy crawl brasileirao2019_serieA 
scrapy crawl brasileirao2019_serieB
```
