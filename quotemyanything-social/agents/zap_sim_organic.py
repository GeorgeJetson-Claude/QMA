#!/usr/bin/env python3
"""
Zapier Simulation for Organic Lead Mission (no Zapier account needed, free).
Monitors Reddit RSS/new.json for quote needs per mission, fires 5LUV alerts, logs.
Run daily via schedule or cron.
Uses stdlib + mission keywords.
"""
import json
import urllib.request
import urllib.parse
from datetime import datetime
import subprocess

TRIGGER = "/home/tupacmafia911/5LUVINC/scripts/trigger_qma.py"
LEADS_LOG = "/home/tupacmafia911/quotemyanything-social/agents/leads_log.txt"

REDDIT_RSS = "https://www.reddit.com/r/Austin+HomeImprovement+lawncare+HVAC+Roofing+Plumbing+Moving/new.json?limit=25"
KEYWORDS = ["need a quote", "looking for a roofer", "roof repair Austin", "hail damage", "storm damage roof", "central texas storm", "williamson county hail", "bastrop storm roof", "how much does it cost", "recommend a contractor", "HVAC Austin", "lawn care Austin", "roof repair Austin", "moving company Austin", "pest control Austin", "anyone know a good", "cheapest", "get quotes", "Austin"]

def fetch_reddit():
    try:
        req = urllib.request.Request(REDDIT_RSS, headers={"User-Agent": "QMA-Organic-Lead-Agent/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            posts = data.get("data", {}).get("children", [])
            return posts
    except Exception as e:
        print(f"Reddit fetch error: {e}")
        return []

def check_opportunities(posts):
    opps = []
    for post in posts:
        data = post.get("data", {})
        title = (data.get("title", "") + " " + data.get("selftext", "")).lower()
        if any(kw.lower() in title for kw in KEYWORDS):
            opps.append({
                "title": data.get("title"),
                "url": "https://reddit.com" + data.get("permalink", ""),
                "sub": data.get("subreddit")
            })
    return opps

def alert(opps):
    for opp in opps:
        msg = f"🔥 NEW LEAD OPPORTUNITY — Reddit r/{opp['sub']}\n{opp['title']}\n{opp['url']}\nDraft reply: Check out https://quotemyanything.com — free quotes from local pros in 60 sec, no spam 🙌"
        print(msg)
        try:
            subprocess.call(["python3", TRIGGER, "ORGANIC_LEAD_OPPORTUNITY", opp["sub"], opp["title"][:50]])
        except:
            pass
        with open(LEADS_LOG, "a") as f:
            f.write(f"[{datetime.now()}] ORGANIC: {msg}\n")

def main():
    print(f"=== Organic Lead Zap Sim {datetime.now()} ===")
    posts = fetch_reddit()
    opps = check_opportunities(posts)
    if opps:
        alert(opps)
    else:
        print("No new quote opportunities in feed.")
    print("=== Done. Per ORGANIC_LEAD_AGENT_MISSION ===")

if __name__ == "__main__":
    main()