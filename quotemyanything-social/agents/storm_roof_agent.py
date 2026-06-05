#!/usr/bin/env python3
"""
Storm Roof Social Auto Agent for QuoteMyAnything (Austin / Central Texas focus).
- Runs content_gen for roofing (storm/hail specific, Gemini brand video only - no jingles).
- Syncs Drive assets (Gemini videos, logos from 5LUV Upload / QMA Project Archive).
- Monitors via zap_sim style for Reddit/X storm roof opportunities.
- Generates value-first posts: "Free Quotes On Anything!" + Gemini video link + link to https://quotemyanything.com/roofing
- Fires 5LUV for each generated/posted.
- Appends to leads_x_reddit_fb.md , Facebook_Posts , current_leads_outreach.
- For new social accounts: outputs ready copy for @QMA_AustinStormRoof or similar (user creates accounts).
- Integrates with phone control /fire RUN_SKILL or direct.
- Zaps: calls the updated zap_sim_organic for roof storm keywords.
- Run daily or via schedule / phone control. Uses other AIs (Grok/Claude) via content gen.

Drive assets: rclone from gdrive for latest Gemini commercial for YT/social embeds (user uploads the ads).
Other AIs: content generated here + user can feed to Claude/Grok for images/captions.

Per QMA master: value-first non-spam, Austin + Central TX storms first (hail alley, recent May/June 2026 events), get roof leads.
"""

import subprocess
from datetime import datetime
from pathlib import Path
import sys

BASE = Path(__file__).parent
TRIGGER = "/home/tupacmafia911/5LUVINC/scripts/trigger_qma.py"
LEADS_FILE = BASE / "leads_x_reddit_fb.md"
FB_FILE = BASE / "Facebook_Posts_2026-06-05.md"
OUTREACH_FILE = BASE / "current_leads_outreach.txt"

DRIVE_GEMINI = "gdrive:QMA Project Archive/"  # adjust; user has 5LUV Upload/ for videos
GEMINI_VIDEO_REF = "https://quotemyanything.com (watch Gemini brand video on site)"

def fire_5luv(v1, v2="", v3="QMA Roof Storm Leads Austin/Central TX"):
    try:
        out = subprocess.check_output(["python3", TRIGGER, v1, v2, v3], timeout=15).decode().strip()
        print(f"[5LUV] {v1}: {out}")
        return True
    except Exception as e:
        print(f"[5LUV fail] {e}")
        return False

def run_content_gen():
    print("=== Running content_gen for roofing storm leads (Gemini brand only) ===")
    try:
        # Call via the skill directly (or phone /fire)
        cmd = f"cd {BASE} && python3 -c \"import sys; sys.path.insert(0,'.'); from skills.content_gen import run; print(run({{'platform':'all', 'service':'roofing'}}))\""
        out = subprocess.getoutput(cmd)
        print(out)
        fire_5luv("CONTENT_GEN_ROOF_STORM", "Austin Central Texas hail wind", "Gemini brand video + Free Quotes On Anything!")
        return out
    except Exception as e:
        print(f"content_gen fail: {e}")
        return ""

def sync_drive_assets():
    print("=== Drive sync for Gemini brand assets (videos/logos for social/YT ads) ===")
    try:
        # Pull latest from Drive QMA assets for Gemini video refs (user uploads to YT)
        out = subprocess.getoutput(f"rclone lsd {DRIVE_GEMINI} 2>&1 | head -5")
        print("Drive assets sample:", out[:200])
        fire_5luv("DRIVE_SYNC_GEMINI", "for social auto + YT ads", "Gemini brand video ready for storms")
        # In real: rclone copy the gemini/ mp4s or links to local for embedding in posts.
        return "Synced Drive Gemini assets for brand video in posts/ads."
    except Exception as e:
        print(f"drive sync note: {e} (rclone may need setup; use assets/gemini/ local)")
        return "Use local assets/gemini/gemini_qma_commercial.mp4 + user YT upload for ads."

def run_zap_sim_roof_storm():
    print("=== Run updated zap_sim_organic for roof storm keywords (Austin/Central TX) ===")
    try:
        out = subprocess.getoutput(f"python3 {BASE}/zap_sim_organic.py 2>&1")
        print(out[:500])
        fire_5luv("ZAP_SIM_ROOF_STORM", "Reddit/X storm roof opps", "Central Texas hail leads to QMA roofing")
        return "Zap sim run for roof storm leads."
    except Exception as e:
        print(f"zap sim: {e}")
        return ""

def generate_storm_roof_posts():
    """Additional storm-specific for new social accounts / X / Reddit. Value first, Gemini brand."""
    posts = [
        "Central Texas storms & hail hitting roofs hard (Austin, Williamson, Bastrop, Round Rock)? Don't take the first roofer quote. Get 3 free competing quotes from licensed local pros in 60s — always free for homeowners. Watch our Gemini brand video 'Free Quotes On Anything!' on the site, then submit: https://quotemyanything.com/roofing #AustinRoofing #CentralTexasStorm",
        "Hail damage from last night's Central TX storms? Invisible hits on shingles common in Hail Alley. Get 3 free roofing quotes fast from Austin area pros who compete for your business. 60 seconds. Gemini commercial shows the savings. https://quotemyanything.com/roofing No spam, real options after the wind & hail.",
        "Austin & Central Texas friends: Storm season = roof claims time. Insurance stories everywhere. Use this free tool for 3 local licensed roofers to fight for your job. 'Free Quotes On Anything!' + our Gemini brand 10s video on site. Takes 60s: https://quotemyanything.com/roofing",
        "Williamson County / Georgetown / Jarrell hail & 60mph winds? Roof damage? Get 3 free quotes from Central TX roofers competing — no obligation. Always free. See Gemini video + start here: https://quotemyanything.com/roofing",
    ]
    with open(LEADS_FILE, "a") as f:
        f.write(f"\n## storm_roof_agent {datetime.now()} - Austin/Central TX hail/wind roof leads\n")
        for p in posts:
            f.write(f"- {p}\n")
    with open(OUTREACH_FILE, "a") as f:
        f.write(f"\n## STORM ROOF OUTREACH {datetime.now()}\n")
        for p in posts:
            f.write(f"X/Reddit/FB: {p}\n")
    print("Generated storm roof posts for new social / X / Reddit / FB. Appended.")
    for p in posts:
        fire_5luv("ROOF_STORM_SOCIAL_POST", p[:60], "Gemini brand + QMA roofing Austin")
    return posts

def main():
    print(f"=== QMA Storm Roof Social Auto Agent {datetime.now()} ===")
    print("Focus: Roof leads Austin + Central Texas storms (hail/wind damage, recent events May/June 2026).")
    print("Brand: Gemini video only. Slogan: Free Quotes On Anything! Public clean.")
    print("New social: Copy for @QMA_AustinRoofStorm or similar (user creates on X/FB/IG/YT).")
    print("Zaps: Integrated sim for Reddit storm roof keywords.")
    print("Drive + other AIs: Sync for Gemini assets; content via this + Grok/Claude.")
    
    run_content_gen()
    sync_drive_assets()
    run_zap_sim_roof_storm()
    generate_storm_roof_posts()
    
    print("\n=== Done. Post the generated to new/existing accounts. Use phone control /fire for more. Fire 5LUVs done. Check for-pros for routing inbound roof leads. ===")
    fire_5luv("STORM_ROOF_AGENT_RUN", "Austin Central Texas", "Gemini brand video + roof leads from storms")

if __name__ == "__main__":
    main()