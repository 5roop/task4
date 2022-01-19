#%%

import time
import logging

logging.basicConfig(format='%(asctime)s - %(message)s',
                    level=logging.INFO)
import feedparser
import pandas as pd
from trafilatura import fetch_url, extract

# %%
urls_hr = [
"https://www.index.hr/rss/info",
"https://www.jutarnji.hr/feed",
"https://www.24sata.hr/flatpages/rss",
"https://www.vecernji.hr/feed",
"https://net.hr/feed",
"https://dnevnik.hr/rss",
"https://www.tportal.hr/rss",
"https://www.rtl.hr/feed/",
"https://slobodnadalmacija.hr/feed/",
"https://narod.hr/feed",
"https://www.lika-online.com/feed/",
"https://www.telegram.hr/feed",
"https://www.dnevno.hr/feed",
"http://www.100posto.hr/rss",
"https://www.novilist.hr/feed/",
"https://o-nama.hrt.hr/rss-i-mobilne-aplikacije/rss-328191",
"https://express.24sata.hr/rss/",
"https://hr.n1info.com/feed",
"https://direktno.hr/rss/",
"https://www.monitor.hr/feed/rss/",
"https://klik.hr/rss",
"http://www.glas-slavonije.hr/Rss",
"https://dalmatinskiportal.hr/sadrzaj/rss/vijesti.xml",
"http://www.057info.hr/rss/info.xml",
"https://www.dalmacijanews.hr/rss",
"https://www.zagreb.info/feed/"]
urls_me = [
    "https://rss.portalanalitika.me",
"https://www.vijesti.me/rss",
"https://www.cdm.me/feed/",
"http://barinfo.me/feed/",
"https://crna.gora.me/feed/",
]
urls_bs = [
    "https://avaz.ba/rss",
"https://www.nezavisne.com/rss",
"https://www.oslobodjenje.ba/rss",
"https://www.bljesak.info/rss",
"https://vijesti.ba/rss/svevijesti",
"https://www.slobodna-bosna.ba/rss/",
"https://www.haber.ba/feed",
"https://www.doznajemo.com?format=rss",
"https://www.poskok.info/feed/",
"https://www.vecernji.ba/rss",
"https://magazin.ba/feed",
"https://www.zenicablog.com/feed/",
"http://tip.ba/feed/",
"https://www.krajina.ba/feed/",
"https://zurnal.info/rss",
"https://www.bh-index.info/feed/",
"https://dnevni.ba/feed/",
"https://pogled.ba/rss/naslovna",
"https://fena.ba/rss",
"http://mojusk.ba/feed/",
"https://krupljani.ba/feed",
"https://www.livno-online.com/?format=feed&type=rss",
]
urls_sr = [
"https://www.blic.rs/rss",
"https://www.kurir.rs/rss",
"https://www.rts.rs/page/rss/ci.html",
"https://www.telegraf.rs/rss",
"https://www.novosti.rs/rss",
"https://informer.rs/rss",
"http://www.politika.rs/rss/",
"https://naslovi.net/rss/",
"https://www.vesti-online.com/feed/",
"https://www.danas.rs/feed/",
"http://tanjug.rs/Rsslat.aspx",
"https://www.njuz.net/rss",
"https://feeds.feedburner.com/juznevesti",
"http://www.nspm.rs/component/option,com_bca-rss-syndicator/feed_id,1/",
"https://pescanik.net/feed",
"https://www.vesti.rs/rss.php",
"https://www.vreme.com/rss/novosti-rss.xml",
"https://www.dnevnik.rs/rss.xml",
"https://24online.rs/feed/",
"https://time.rs/rss/rsspage",
"https://www.standard.rs/feed/",
"https://www.istinomer.rs/feed/",
"https://beta.rs/betarss",
]

top_level_dict = {
    "hr": urls_hr,
    "bs": urls_bs,
    "sr": urls_sr,
    "me": urls_me,
}

from typing import List
def get_links_from_rss(url:str) -> List[str]:
    feed = feedparser.parse(url)
    if not feed.entries:
        logging.warning(f"We have no entries at this url: {url:s}")
        return None
    return [entry.get("link") for entry in feed.entries]

def get_text_from_link(url:str) -> str:
    downloaded = fetch_url(url)
    text = extract(downloaded)
    return text

current_items = list()
for lang, urls in top_level_dict.items():
    for url in urls:
        links = get_links_from_rss(url)
        if not links:
            continue
        for link in links:
            text = get_text_from_link(link)
            curtime  = time.strftime("%Y-%m-%dT%T%z")

            itemdict = {
                "language":lang,
                "text": text,
                "source": link,
                "rss_link": url,
                "crawl_time": curtime,
                "text_hash": hash(text)
                }
            current_items.append(itemdict)

# %%
import os
crawl_dir = "/home/peterr/macocu/taskB/task4/"
crawl_file = "22_webcrawl.csv"

current_df = pd.DataFrame(data=current_items)

if crawl_file not in os.listdir(crawl_dir):
    current_df.to_csv(
        os.path.join(
            crawl_dir, crawl_file
        ),
        index=False
    )
else:
    old_df = pd.read_csv(
        os.path.join(
            crawl_dir, crawl_file
        )
    )
    # This is the place to implement some filtering.
    # Later, after existing part is tested.

    
    merged = pd.concat([old_df, current_df], ignore_index=True)
    merged.to_csv(
        os.path.join(
            crawl_dir, crawl_file
            ),
        index=False

    )
# %%
