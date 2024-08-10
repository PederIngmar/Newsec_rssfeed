import feedparser
import json
from functools import reduce
from operator import getitem
from json2html import *
import os as os
from threading import Event
from datetime import datetime

exit = Event()


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

def safe_get(entry, keys):
    """
    Safely retrieves the value at nested keys in a dictionary.
    Returns None if any key in keys doesn't exist in dct.
    """
    try:
        return reduce(getitem, keys, entry)
    except (KeyError, TypeError):
        return None
    

def get_rss_data(rss = realestate_rss_feeds):
    parsedict = {}

    # Get the data and put it into json files
    for feed in rss:
        # print(feed)
        d = parsedict[feed] = feedparser.parse(realestate_rss_feeds[feed])
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
                output_dir = f"storage/{feed}"
                os.makedirs(output_dir, exist_ok=True) # First run needs creating the Output folder
                json_fn = os.path.join(output_dir, f"{i}.json")                
                with open(json_fn, "w") as file:
                    json.dump(json_obj, file)
                all_links += json_obj["url"] + ", "
        #print(all_links)



    # getting the timestamp
    dt = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

    # Make html file of feed in Output    
    output_dir = "Output"
    os.makedirs(output_dir, exist_ok=True) # First run needs creating the Output folder    
    html_fn = os.path.join(output_dir, "storage.html")    
    with open(html_fn, "w") as html_file :
        html_file.write(f"<title>NewSec media parser!</title>\n")        
        html_file.write(f"<h1>NewSec media parser, updated {dt}</h1>\n")        
        for feed in realestate_rss_feeds:
            d = parsedict[feed]
            html_file.write(f"<h2>Media: {feed}</h2>\n")        
            for i, entry in enumerate(d["entries"]):
                if entry != {}:
                    for f in ["date"]:
                        data = str(safe_get(entry, RSS_path_config[feed][f]))
                        html_file.write(f'<p>{f}: {data}, ')
                    for f in ["title"]:
                        data = str(safe_get(entry, RSS_path_config[feed][f]))
                        url  = str(safe_get(entry, RSS_path_config[feed]["url"]))
                        html_file.write(f'<a href="{url}">{data}</a>, ')
                    for f in ["image"]:
                        data = "Illustration, image"
                        url  = str(safe_get(entry, RSS_path_config[feed]["image"]))
                        html_file.write(f'{f}: <a href="{url}">{data}</a></p>\n')



    print(f"NewSec media parser Updated rss data to {html_fn} at {dt}")


def main():
    while not exit.is_set():
      get_rss_data()
      exit.wait(20)

    print("All done!")
    # perform any cleanup here

def quit(signo, _frame):
    print("Interrupted by %d, shutting down" % signo)
    exit.set()

if __name__ == '__main__':
    import signal
    for sig in ('TERM', 'HUP', 'INT'):
        signal.signal(getattr(signal, 'SIG'+sig), quit);

    main()


    
