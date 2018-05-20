import requests
import sys
import os

from tqdm import tqdm
from .constants import URL_API_VACANCIES
from .constants import GETTING_IDS_MSG


def make_request(url_vacancies=URL_API_VACANCIES, params=None, timeout=10):
    """
    Makes a request to the api of the hh.ru service
    and returns a response in json format.
    """
    r = requests.get(url_vacancies, params=params, timeout=timeout)
    # print('request url: {};\n'.format(r.url))
    r.raise_for_status()

    return r.json()


def count_vacancies(url_vacancies=URL_API_VACANCIES, **params):
    """
    Counts the number of vacancies issued by the search query.
    """
    found = -1
    params['per_page'] = '1'

    try:
        found = make_request(url_vacancies, params)['found']
    except requests.exceptions.RequestException as err:
        print(err, file=sys.stderr)

    return found


def count_pages(found, per_page):
    """
    Counts number of pages to "read".
    """
    return found // per_page + (found % per_page > 0)


def get_vacancies_ids(url_vacancies=URL_API_VACANCIES, **params):
    """
    Returns the list of vacancies' IDs issued by the search query.
    """
    id_list = []

    found = count_vacancies(url_vacancies, **params)
    per_page = int(params['per_page'])
    try:
        print(GETTING_IDS_MSG)

        for cur_page_num in tqdm(range(count_pages(found, per_page))):
            params['page'] = cur_page_num

            vacancies = make_request(url_vacancies, params)['items']
            id_list += list(map(lambda x: x['id'], vacancies))
    except requests.exceptions.RequestException as err:
        print(err, file=sys.stderr)

    return id_list


def get_vacancy(vac_id, url_vacancies=URL_API_VACANCIES):
    """
    Downloads the vacancy (json format)
    and returns it as a list of python structures.
    """
    url_vacancies += '/{}'

    return make_request(url_vacancies.format(vac_id))


if __name__ == '__main__':
    print('vacancies module')
