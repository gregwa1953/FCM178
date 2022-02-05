# ===================================================
#                 TMDB wrapper
# ---------------------------------------------------
#                   wrapper.py
# ---------------------------------------------------
# Author: G.D. Walters
# Copyright (c) 2022 by G.D. Walters
# Project creation date: 24 January, 2022
# Release date:
# Version: 0.0.4
# ---------------------------------------------------
# NOTE: Version 0.0.4 only supports the API version 3
#       API version 4 will hopefully be supported in a later release
# ===================================================
"""
    **********************************************************
    This is a simple wrapper to The Movie DataBase API.
    ----------------------------------------------------------
    You MUST have a TMDB API key, which is currently free.  You can sign up for one
    at https://www.themoviedb.org/documentation/api
    **********************************************************
    Currently supported functions:
      *** Search functions ***
      *** Search functions will return a number of results depending on query ***
      search_movie
      search_tvshow
      search_multi

      *** Get detail functions (REQUIRE ID FROM SEARCH FUNCTIONS) ***
      get_movie_by_id
      get_movie_credits
      get_person
      get_tvshow_by_id
      get_tv_season_detail
      get_tv_episode_detail
      get_tv_show_season_credits
      get_movie_watch_providers
      get_tv_on_air (VERY EXPERMENTAL)

      These are the minimum functions that I consider to be needed for most use
      More functions supporting the API will be added as time/health allows
      
      See the API documentation at https://developers.themoviedb.org/3/getting-started/introduction
      for more information.
      """

# ================================
# Imports
# ================================
import requests
import json
import pprint
import locale

# ====================================================================================
# TMDB requires an authorization key.  You can sign up for a free key at the website
# Place your keys here.
# ====================================================================================
mykey3 = <Your API Key Here>

loc = locale.getlocale()[0]
# print(loc)


def addinto(l1, l2):
    for c in l2:
        l1.append(c)
    return l1


def search_movie(
    key, query, page=1, language="en-US", include_adult=False
):  # region,year,primary_release_year):
    """
    Function search_movie
    inputs:  key           - TMDB API key.
            query         - String containing the movie name to search for.
            page          - Which page to retreive - defaults to 1 - Not needed any more.
            language      - send in variable loc which is set at startup.  Defaults to 'en-US'.
            include_adult - Defaults to False - set to True if you want to search for Adult movies.
    returns: status_code   - HTTP Status code.  200 is success - anything else should be considered an error.
            tresults      - Total number of results that were returned.
            tpages        - The number of pages that the search generated.  TMDB ONLY sends 1 page at a time.  A
                            second (or more) request must be made to get all results.  This function takes care of that and returns
                            all found results.
            endresults    - A list of dictionaries with the data from the search (not a JSON data structure).
    """
    curpage = 1
    url = f"https://api.themoviedb.org/3/search/movie?api_key={key}&language={language}&query={query}&page={page}&include_adult={include_adult}"
    resp = requests.get(url)
    # print(f'StatusCode: {resp.status_code}')
    if resp.status_code == 200:
        jdata = resp.json()
        results1 = jdata["results"]
        rcnt = len(results1)
        tpages = jdata["total_pages"]
        if tpages > 1:
            for pag in range(2, tpages + 1):
                url = f"https://api.themoviedb.org/3/search/movie?api_key={key}&language={language}&query={query}&page={pag}&include_adult={include_adult}"
                resp = requests.get(url)
                if resp.status_code == 200:
                    jdatatmp = resp.json()
                    res = jdatatmp["results"]
                    endresults = addinto(results1, res)
            # pprint.pprint(endresults)
            # print(f'Total: {len(endresults)}')
            tresults = jdata["total_results"]
        else:
            endresults = jdata["results"]
            tresults = jdata["total_results"]
    else:
        jdata = None
        tresults = 0
    return resp.status_code, tresults, tpages, endresults


def search_tvshow(key, query, language="en-US", include_adult=False):
    """
    Function search_tvshow (similar to search_movie but for tv series)
    inputs:  key           - TMDB API key.
            query         - String containing the movie name to search for.
            page          - Which page to retreive - defaults to 1 - Not needed any more.
            language      - send in variable loc which is set at startup.  Defaults to 'en-US'.
            include_adult - Defaults to False - set to True if you want to search for Adult movies.
    returns: status_code   - HTTP Status code.  200 is success - anything else should be considered an error.
            tresults      - Total number of results that were returned.
            tpages        - The number of pages that the search generated.  TMDB ONLY sends 1 page at a time.  A
                            second (or more) request must be made to get all results.  This function takes care of that and returns
                            all found results.
            endresults    - A list of dictionaries with the data from the search (not a JSON data structure).
    """
    url = f"https://api.themoviedb.org/3/search/tv?api_key={key}&query={query}&language={language}&page=1&include_adult={include_adult}"
    resp = requests.get(url)
    # print(f'StatusCode: {resp.status_code}')
    if resp.status_code == 200:
        jdata = resp.json()
        results1 = jdata["results"]
        rcnt = len(results1)
        tpages = jdata["total_pages"]
        if tpages > 1:
            for pag in range(2, tpages + 1):
                url = f"https://api.themoviedb.org/3/search/tv?api_key={key}&language={language}&query={query}&page={pag}&include_adult={include_adult}"
                resp = requests.get(url)
                if resp.status_code == 200:
                    jdatatmp = resp.json()
                    res = jdatatmp["results"]
                    endresults = addinto(results1, res)
            tresults = jdata["total_results"]
        else:
            endresults = jdata["results"]
            tresults = jdata["total_results"]
    else:
        jdata = None
        tresults = 0
    return resp.status_code, tresults, tpages, endresults


def search_multi(key, query, language="en-US", include_adult=False):
    """
    Function search_multi - similar to search_movie but supports movies, tv shows and people in a single request
    inputs:  key          - TMDB API key.
            query         - String containing the movie name to search for.
            page          - Which page to retreive - defaults to 1 - Not needed any more.
            language      - send in variable loc which is set at startup.  Defaults to 'en-US'.
            include_adult - Defaults to False - set to True if you want to search for Adult movies.
    returns: status_code   - HTTP Status code.  200 is success - anything else should be considered an error.
            tresults      - Total number of results that were returned.
            tpages        - The number of pages that the search generated.  TMDB ONLY sends 1 page at a time.  A
                            second (or more) request must be made to get all results.  This function takes care of that and returns
                            all found results.
            endresults    - A list of dictionaries with the data from the search (not a JSON data structure).

    NOTE: Using this function will probably return a very large number of responses.
    """
    """Search multiple models in a single request. Multi search currently supports searching for 
       movies, tv shows and people in a single request."""

    url = f"https://api.themoviedb.org/3/search/multi?api_key={key}&language={language}&query={query}&page=1&include_adult=false"
    resp = requests.get(url)
    # print(f'StatusCode: {resp.status_code}')
    if resp.status_code == 200:
        jdata = resp.json()
        results1 = jdata["results"]
        rcnt = len(results1)
        tpages = jdata["total_pages"]
        if tpages > 1:
            for pag in range(2, tpages + 1):
                url = f"https://api.themoviedb.org/3/search/multi?api_key={key}&language={language}&query={query}&page={pag}&include_adult={include_adult}"
                resp = requests.get(url)
                if resp.status_code == 200:
                    jdatatmp = resp.json()
                    res = jdatatmp["results"]
                    endresults = addinto(results1, res)
            tresults = jdata["total_results"]
        else:
            endresults = jdata["results"]
            tresults = jdata["total_results"]
    else:
        jdata = None
        tresults = 0
    return resp.status_code, tresults, tpages, endresults


def get_movie_by_id(key, id, language="en-US"):
    """
    function get_movie_by_id
    This function will return information about a specific movie based on the TMDB-ID.  Use search_movie to get the id.
    inputs:  key         - TMDB API key.
             id          - id of the movie
             language    - send in variable 'loc' which is set at runtime - defaults to 'en-US'
    returns: status_code - HTTP - Status code - 200 is success anything else is considered an error
             jdata       - A JSON data structure containing information on the movie.
    """
    url = f"https://api.themoviedb.org/3/movie/{id}?api_key={key}&language={language}"
    resp = requests.get(url)
    print(f"StatusCode: {resp.status_code}")
    if resp.status_code == 200:
        jdata = resp.json()
    else:
        jdata = None
    return resp.status_code, jdata


def get_movie_credits(key, id, language="en-US"):
    url = f"https://api.themoviedb.org/3/movie/{id}/credits?api_key={key}&language={language}"
    resp = requests.get(url)
    print(f"StatusCode: {resp.status_code}")
    if resp.status_code == 200:
        jdata = resp.json()
    else:
        jdata = None
    return resp.status_code, jdata


def get_tvshow_by_id(key, id, language="en-US"):
    """
    function get_tvshow_by_id
    This function will return information about a specific tv series based on the TMDB-ID.  Use search_tvshow to get the id.
    inputs:  key         - TMDB API key.
             id          - id of the movie
             language    - send in variable 'loc' which is set at runtime - defaults to 'en-US'
    returns: status_code - HTTP - Status code - 200 is success anything else is considered an error
             jdata       - A JSON data structure containing information on the tv series.
    """
    url = f"https://api.themoviedb.org/3/tv/{id}?api_key={key}&language={language}"
    resp = requests.get(url)
    print(f"StatusCode: {resp.status_code}")
    if resp.status_code == 200:
        jdata = resp.json()
    else:
        jdata = None
    return resp.status_code, jdata


def get_tv_episode_detail(key, id, season, episode, language="en-US"):
    """
    function get_tv_episode_detail
    Get the TV episode details by id.
    inputs:  key         - TMDB API key.
             id          - id of the movie
             season      - Season of the tv series (INT)
             episode     - Episode number of the series (INT)
             language    - send in variable 'loc' which is set at runtime - defaults to 'en-US'
    returns: status_code - HTTP - Status code - 200 is success anything else is considered an error
             jdata       - A JSON data structure containing information on the tv series.
    """
    url = f"https://api.themoviedb.org/3/tv/{id}/season/{season}/episode/{episode}?api_key={key}&language={language}"
    resp = requests.get(url)
    print(f"StatusCode: {resp.status_code}")
    if resp.status_code == 200:
        jdata = resp.json()
    else:
        jdata = None
    return resp.status_code, jdata


def get_tv_show_season_credits(key, id, season, language="en_US"):
    url = f"https://api.themoviedb.org/3/tv/{id}/season/{season}/credits?api_key={key}&language={loc}"
    print(url)
    resp = requests.get(url)
    print(f"Status code: {resp.status_code}")
    if resp.status_code == 200:
        jdata = resp.json()
    else:
        jdata = None
    return resp.status_code, jdata


def get_tv_season_detail(key, id, season, language="en-US"):
    """
    function get_tv_season_detail
    This function will get the TV season details by id.
    inputs:  key         - TMDB API key.
             id          - id of the movie
             season      - Season number of the tv series (INT)
             language    - send in variable 'loc' which is set at runtime - defaults to 'en-US'
    returns: status_code - HTTP - Status code - 200 is success anything else is considered an error
             jdata       - A JSON data structure containing information on the tv series.
    """
    url = f"https://api.themoviedb.org/3/tv/{id}/season/{season}?api_key={key}&language={language}"
    resp = requests.get(url)
    print(f"StatusCode: {resp.status_code}")
    if resp.status_code == 200:
        jdata = resp.json()
    else:
        jdata = None
    return resp.status_code, jdata


def get_movie_watch_providers(key, id, region, language="en-US"):
    # Returns a list of the watch provider (OTT/streaming) data that TMDB have available for movies.
    # You can specify a watch_region param if you want to further filter the list by country.
    # =========================================================
    # Please note: In order to use this data you must attribute the source of the
    # data as JustWatch. If TMDB finds any usage not complying with these terms they will revoke access to the API.
    # =========================================================
    url = f"https://api.themoviedb.org/3/movie/{id}/watch/providers?api_key={key}&language={language}&watch_region={region}"
    resp = requests.get(url)
    print(f"StatusCode: {resp.status_code}")
    if resp.status_code == 200:
        jdata = resp.json()
    else:
        jdata = None
    return resp.status_code, jdata


def get_tv_on_air(key, language="en-US"):
    """
    Get a list of shows that are currently on the air.

    This query looks for any TV show that has an episode with an air date in the next 7 days.

    Currently only returns the first page (about 20 results)
    ****************************************************
    *********** Experimental - NOT FINISHED ************
    ****************************************************
    """
    url = f"https://api.themoviedb.org/3/tv/on_the_air?api_key={key}&language={language}&page=1"
    resp = requests.get(url)
    print(f"StatusCode: {resp.status_code}")
    if resp.status_code == 200:
        jdata = resp.json()
    else:
        jdata = None
    return resp.status_code, jdata


def get_person(key, id, language="en-US"):
    url = f"https://api.themoviedb.org/3/person/{id}?api_key={key}&language={loc}"
    resp = requests.get(url)
    if resp.status_code == 200:
        jdata = resp.json()
    else:
        jdata = None
    return resp.status_code, jdata


def testit():
    # Get Locale for language
    loc = locale.getlocale()[0]
    print(loc)

    print("Search Movie by name")
    status, tresults, tpages, endresults = search_movie(
        mykey3,
        "The Mitchells vs. the machines",
        page=1,
        language={loc},
        include_adult=False,
    )

    print(f"Search Movie response: {status} - Total Results: {tresults}")
    pprint.pprint(endresults)
    movie_id = endresults[0]["id"]
    print(f"Movie_Id: {movie_id}")
    inp = input("Press Return")

    print("Search TV show by name")
    status, tresults, tpages, endresults = search_tvshow(
        mykey3, "Father Brown", language={loc}
    )
    print(f"Search TV response: {status} - Total Results: {tresults}")
    pprint.pprint(endresults)
    print("")
    inp = input("Press Return")

    print("Search Multi-Search")
    status, tresults, tpages, endresults = search_multi(
        mykey3, "Harry Potter", language={loc}
    )
    # status, total_results, jdata = search_multi(mykey3,
    #                                             'Harry Potter',
    #                                             language={loc})
    if status == 200:
        print(f"Number of results: {tresults}")
        pprint.pprint(endresults)
        print("")
    inp = input("Press Return")

    print("Get Movie by ID")
    status, jdata = get_movie_by_id(mykey3, 501929, language={loc})
    if status == 200:
        pprint.pprint(jdata)
    inp = input("Press Return")

    print(
        "Get TV Show by ID - Currently only returns the first page (about 20 results)"
    )
    status, jdata = get_tvshow_by_id(mykey3, 61511, language={loc})
    if status == 200:
        pprint.pprint(jdata)
    inp = input("Press Return")

    print("Get Season Detail")
    status, jdata = get_tv_season_detail(mykey3, 61511, 9, language={loc})
    if status == 200:
        pprint.pprint(jdata)
    inp = input("Press Return")
    print("Get TV Episode Detail (by season and episode)")
    status, jdata = get_tv_episode_detail(mykey3, 61511, 9, 10, language={loc})
    if status == 200:
        pprint.pprint(jdata)
    inp = input("Press Return")

    print("Season credits")
    status, jdata = get_tv_show_season_credits(mykey3, 61511, 1, language=loc)
    if status == 200:
        pprint.pprint(jdata)

    inp = input("Press Return -> ")

    print("JustWatch Providers:")
    status, jdata = get_movie_watch_providers(mykey3, 501929, region=loc, language=loc)
    if status == 200:
        pprint.pprint(jdata)

    inp = input("Press Return")

    print("TV On the Air:")
    status, jdata = get_tv_on_air(mykey3, loc)
    if status == 200:
        pprint.pprint(jdata)


if __name__ == "__main__":
    testit()
