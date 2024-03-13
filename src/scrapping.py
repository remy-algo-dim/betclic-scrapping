from selenium.webdriver.common.by import By
import time
from collections import OrderedDict


def accept_user_conditions(driver):
    """

    :param driver:
    :return: Click on the button which accepts user conditions
    """
    accept_conditions = "/html/body/div[1]/div/div[2]/button[2]"
    elements = driver.find_elements(By.XPATH, accept_conditions)
    if elements:
        elements[0].click()
    return


def retrieve_current_game(driver):
    """
    Once we clicked on the game we want to retrieve the names of the teams
    :param driver:
    :return: home team name and visitor team name
    """
    current_game = "/html/body/app-desktop/div[1]/div/bcdk-content-scroller/div/" \
                   "sports-match-page/sports-match-header/div/sports-events-event/div/scoreboards-scoreboard"
    elements = driver.find_elements(By.XPATH, current_game)
    current_home_team, current_out_team = elements[0].text.split('\n')[0], elements[0].text.split('\n')[2]
    return current_home_team, current_out_team


def retrieve_rates(driver):
    """

    :param driver:
    :return: dictionary with bet in key, rate in value
    """
    # Trouver le div basé sur le titre qui précède directement le conteneur de votre cible
    # Explication: //h2[contains(text(), 'Première équipe à marquer')] trouve le <h2> contenant le texte spécifique.
    # Remplacez <h2> par l'élément approprié si le titre n'est pas dans un
    # <h2>./following::div[contains(@class, 'marketBox_body')][1] sélectionne le premier div
    # qui suit le titre trouvé et qui contient la classe marketBox_body. following:: permet de
    # sélectionner tous les éléments qui suivent dans le document, pas seulement les enfants directs,
    # et [1] limite la sélection au premier élément correspondant.
    paris = {}
    element_cible = driver.find_element(By.XPATH,
                                        "//h2[contains(text(), 'Écart de buts')]/"
                                        "following::div[contains(@class, 'marketBox_body')][1]")
    print("Success to retrieve rates")
    markets_grid = element_cible.text.split('\n')
    for i in range(0, len(markets_grid), 2):
        pari = markets_grid[i]
        cote = markets_grid[i + 1]
        paris[pari] = cote

    # Trier le dict en fonction des cotes, et on ne garde que les paris entre 1.02 et 1.1
    paris = {k: v for k, v in sorted(paris.items(), key=lambda item: item[1])
             if 1.01 < float(v.replace(',', '.')) < 1.11}

    paris = dict(list(paris.items()))
    return paris


def retrieve_current_scrapped_game_date(driver):
    """
    Retrieve the date of the game we are about to scrap
    if the returned list contains one element (the hour), it means the game is today, otherwise
    it's not today (day, hour)
    :param driver:
    :return: date in list
    """
    day = '/html/body/app-desktop/div[1]/div/bcdk-content-scroller/div' \
          '/sports-match-page/sports-match-header/div/sports-events-event/' \
          'div/scoreboards-scoreboard/scoreboards-scoreboard-global/div/div[2]'
    elements = driver.find_elements(By.XPATH, day)
    return elements[0].text.split('\n')


def retrieve_all_bets_per_game(driver, index_):
    """

    :param driver:
    :param index_: game index
    :return:
    """
    match_i = "/html/body/app-desktop/div[1]/div/bcdk-content-scroller/div/" \
              "sports-pinned-competition-page/sports-events-list/bcdk-vertical-scroller/" \
              "div/div[2]/div/div/div[1]/div[2]/sports-events-event[{}]/a/div/" \
              "scoreboards-scoreboard/scoreboards-scoreboard-global/div/div[2]/div[1]".format(index_)
    # click on the gmae
    elements = driver.find_elements(By.XPATH, match_i)
    print("Click on the game")
    if elements:
        elements[0].click()
        time.sleep(3)
        # on recupere l'affiche du match pour voir s'il s'agit du dernier de la liste de today
        current_home_team, current_out_team = retrieve_current_game(driver)
        print("Current game: {} - {}".format(current_home_team, current_out_team))
        current_game_date = retrieve_current_scrapped_game_date(driver)
        if len(current_game_date) > 1:
            print("The game is not today, lets stop")
            index_ = 99  # on fixe i à 99 car l'incrémentation plus bas le place à 100 et donc stoppera la boucle

        # scroll 52% to see th arrow down of 'ecarts de buts' section
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.56);")
        time.sleep(1)

        # section ecarts de buts, on déroule (appuie sur la flèche deroulante)
        # il y a plusieurs arrow down avec les memes elements javascript donc je clique sur la troisieme (celle
        # des ecarts de buts)

        # Trouver la section contenant la flèche "vers le bas"
        section_ecarts_de_buts = driver.find_element(By.XPATH,
                                                     "//h2[contains(text(), 'Écart de buts')]"
                                                     "/ancestor::sports-markets-single-market")

        # Trouver la flèche "vers le bas" dans cette section
        icone_fleche_bas = section_ecarts_de_buts.find_element(By.XPATH, ".//span[@class='icons icon_down']")

        # Cliquer sur la flèche "vers le bas"
        icone_fleche_bas.click()

        # récupération de toutes les côtes (same xpath) + ajout de l'affiche au debut du dict
        paris = retrieve_rates(driver)
        updated_dict = OrderedDict([('affiche', "{} - {}".format(current_home_team, current_out_team))])
        # Ajouter les éléments du dictionnaire existant après la clé 'affiche'
        updated_dict.update(paris)
        updated_dict = dict(updated_dict)  # change type
        return index_, updated_dict

