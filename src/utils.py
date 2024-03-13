import pandas as pd
from datetime import datetime
import time

import scrapping


def retrieve_all_bets(driver, betclic_url):
    """

    Process:
    - on clique sur l'affiche - recupere le nom des equipes - checkons si c'est la dernière affiche -
    scroll - clique sur me menu déroulant de la section 'ecarts de buts' - recupere les 2 paris
    pour lesquels les cotes sont les plus faibles (mais pas 1.01) sous forme de dictionnaire -
    ajoute le pari a une liste - on revient sur la page precedente - et reiterons le process
    """
    all_bets = []
    i = 1

    while i != 100:
        try:
            i, paris = scrapping.retrieve_all_bets_per_game(driver, i)
            print("Success to retrieve dates for game {}".format(i))
            print(100 * "-")

            # ajoute des deux paris (dictionnaire) à la liste des paris
            all_bets.append(paris)
            time.sleep(2)

            # on revient a la page precédente
            driver.get(betclic_url)
            time.sleep(3)
            i += 1
            # Creation de la dataframe (concatenation avec la dataframe précédente)
            # ligne: matchs + date: colonnes, pari 1, pari 2, et au fur et mesure des features type (lendemain de ldc, championnat ...)
        except Exception as e:
            print(e)
            i += 1
    return all_bets


def create_dataframe(bets):
    """
    - bets: list of dict
    Example:
    paris = [
    {'affiche': 'Grenoble - Laval', 'Laval ne perd pas ou perd de 2 buts ou -': '1,02', 'Grenoble ne perd pas ou perd de 1 but exactement': '1,05'},
    {'affiche': 'Lazio - Udinese', 'Lazio ne perd pas ou perd de 1 but exactement': '1,03', 'Udinese ne perd pas ou perd de 2 buts ou -': '1,06'},
    {'affiche': 'Chelsea - Newcastle', 'Newcastle ne perd pas ou perd de 3 buts ou -': '1,02', 'Chelsea ne perd pas ou perd de 1 but exactement': '1,07', 'Newcastle ne perd pas ou perd de 2 buts ou -': '1,09'},
    {'affiche': 'Almeria - Séville', 'Almeria ne perd pas ou perd de 2 buts ou -': '1,03', 'Séville ne perd pas ou perd de 1 but exactement': '1,08'},
    {'affiche': 'Gil Vicente - Chaves', 'Gil Vicente ne perd pas ou perd de 1 but exactement': '1,03', 'Chaves ne perd pas ou perd de 2 buts ou -': '1,07'}
]
    """
    today_date = datetime.now().strftime("%d/%m/%y")

    # Trouver le nombre maximum de paris dans un dictionnaire
    max_paris = max(len(bet) - 1 for bet in bets)  # -1 pour exclure la clé 'affiche'

    data = []
    for match in bets:
        affiche_date = f"{match['affiche']} - {today_date}"
        paris = [(key, value) for key, value in match.items() if key != 'affiche']
        paris_str = [f"{pari[0]}: {pari[1]}" for pari in paris]
        data.append([affiche_date] + paris_str + [''] * (max_paris - len(paris)))

    # Créer la DataFrame
    columns = ['Index'] + [f'pari_{i}' for i in range(1, max_paris + 1)]
    df = pd.DataFrame(data, columns=columns)
    df.set_index('Index', inplace=True)

    return df


