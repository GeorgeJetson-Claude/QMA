"""
Skill: content_gen
Generates platform-specific content: YT SEO videos (as in youtube_agent), FB posts (exact per MD), X threads.
Focused on driving traffic to live .com + /for-pros for business plan.
"""
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent.parent
YT_PLAN = BASE / "youtube_videos_plan.md"  # reuse existing if present, else generate
FB_FILE = BASE / "Facebook_Posts_2026-06-05.md"

def run(context: dict = None):
    context = context or {}
    platform = context.get("platform", "all")
    service = context.get("service", "roofing")
    
    results = {}
    
    if platform in ("all", "youtube"):
        # YT titles/scripts focused on Austin/Central TX storm roof leads, Gemini brand video only
        yt = {
            "title": f"Free Roofing Quotes Austin TX Central Texas After Storms - 3 Local Pros Compete (Hail Damage)",
            "desc": f"Central Texas hail & wind storms hitting roofs hard? Austin area homeowners: Get 3 free competing roofing quotes from licensed local pros in 60 seconds. No spam. No pressure. Watch our Gemini brand video \"Free Quotes On Anything!\" on site.\nReal savings on storm damage repairs.\nTry now: https://quotemyanything.com/roofing",
            "script": f"[0-5s] Central TX storms? Hail and wind damage to your roof?\n[5-15s] One roofer quote = overpay or insurance issues.\n[15-40s] QuoteMyAnything: 1 form = 3+ local Austin/Central TX roofers compete for your storm repair job.\n[40-55s] Always free for you. 60 seconds. See our Gemini brand commercial on the site.\n[55-60s] Get free roof quotes now: https://quotemyanything.com/roofing . Save after the storms.",
            "tags": f"austin roof quotes, central texas hail damage roof repair, free roofing estimates austin, storm roof damage quotes texas, compare contractor quotes austin"
        }
        results["youtube"] = yt
    
    if platform in ("all", "facebook"):
        # Value-first storm roof posts for Austin/Central TX, slogan + Gemini brand video only. No jingles.
        fb_posts = [
            f"Austin & Central Texas homeowners: Recent hail/wind storms damage your roof? Get 3 free roofing quotes in 60 seconds from local pros who compete. Always free. No spam. Watch the Gemini brand video on site for \"Free Quotes On Anything!\" — then submit: https://quotemyanything.com/roofing",
            f"Storm season in full swing. One quote for roof repair after hail in Williamson, Bastrop, Austin area? Get 3 competing free quotes fast from licensed local roofers. 60s form. Our Gemini commercial shows exactly how you save. https://quotemyanything.com/roofing",
            f"Central Texas storms = roof damage common (invisible hail hits). Don't wait for one roofer. Free Quotes On Anything! matches you to 3 Austin-area pros in under a minute. Always free for homeowners. See Gemini video + get quotes: https://quotemyanything.com/roofing"
        ]
        results["facebook"] = fb_posts
        # Also append to the FB file for user to post
        with open(FB_FILE, "a") as f:
            f.write(f"\n## content_gen Skill {datetime.now()} - STORM ROOF AUSTIN/CENTRAL TX\n")
            for p in fb_posts:
                f.write(f"- {p}\n")
    
    print(f"[content_gen] Generated for {platform} / {service} (storm focus, Gemini brand only). Ready to post + upload.")
    
    return {
        "status": "ok",
        "platform": platform,
        "service": service,
        "items": len(results),
        "call_to_action": "Post FB/X today. Record YT with phone + CapCut using Gemini video. Add end screen to https://quotemyanything.com/roofing . Target storm keywords in Austin, Round Rock, Georgetown, Bastrop."
    }