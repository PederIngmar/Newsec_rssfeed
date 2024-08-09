import feedparser
import json
from functools import reduce
from operator import getitem

realestate_rss_feeds = {
    "E24": "https://e24.no/rss2/?seksjon=eksklusiv24_eiendom",
    "DN": "https://services.dn.no/api/feed/rss/?categories=nyheter&topics=eiendom",
    "FA": "https://ws.finansavisen.no/api/articles.rss?category=Bolig",
    "Nordicpropertynews": "https://nordicpropertynews.com/feed",
    "Fastighetssverige": "https://fastighetssverige.se/feed",
    "DI": "https://www.di.se/rss",
}
{
    "Eiendomswatch": "",
    "Estatenyheter": "",
    "Estatevest": "",
}

RSS_path_config = {
    "E24": {
        "title": ["title"],
        "url": ["link"],
        "date": ["published"],
        "image": ["e24_articleimg"]
    },
    "DN": {
        "title": ["title"],
        "url": ["link"],
        "date": ["published"],
        "image": ["media_content", 0, "url"]
    },
    "FA": {
        "title": ["title"],
        "url": ["link"],
        "date": ["published"],
        "image": ["media_content", 0, "url"]
    },
    "Nordicpropertynews": {
        "title": ["title"],
        "url": ["link"],
        "date": ["published"],
        "image": ["media_content", 0, "url"]
    },
    "DI": {
        "title": ["title"],
        "url": ["link"],
        "date": ["published"],
        "image": ["media_content", 0, "url"]
    },
    "Eiendomswatch": {
        "title": ["title"],
        "url": ["link"],
        "date": ["published"],
        "image": ["media_content", 0, "url"]
    },
    "Fastighetssverige": {
        "title": ["title"],
        "url": ["link"],
        "date": ["published"],
        "image": ["media_content", 0, "url"]
    }
}

def safe_get(dct, keys):
    """
    Safely retrieves the value at nested keys in a dictionary.
    Returns None if any key in keys doesn't exist in dct.
    """
    try:
        return reduce(getitem, keys, entry)
    except (KeyError, TypeError):
        return None
    
    
for feed in realestate_rss_feeds:
    print(feed)
    d = feedparser.parse(realestate_rss_feeds[feed])
    all_links = ""
    for i, entry in enumerate(d["entries"]):
        #print(entry)
        if entry != {}:
            json_obj = {
                "url": safe_get(entry, RSS_path_config[feed]["url"]),
                "title": safe_get(entry, RSS_path_config[feed]["title"]),
                "date": safe_get(entry, RSS_path_config[feed]["date"]),
                "image": safe_get(entry, RSS_path_config[feed]["image"])
            }
            # Save json to storage/
            with open(f"storage/{feed}/{i}.json", "w") as file:
                json.dump(json_obj, file)
            all_links += json_obj["url"] + ", "
    print(all_links)