import streamlit as st
import requests
from PIL import Image, ImageDraw
from io import BytesIO

# =========================================================
# SAFE IMAGE LOADER
# =========================================================
def load_image(url, name):
    try:
        r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=10)
        r.raise_for_status()
        return Image.open(BytesIO(r.content)).convert("RGB")
    except:
        img = Image.new("RGB", (1000,650),(25,25,25))
        d = ImageDraw.Draw(img)
        d.text((20,20),f"{name} image failed",fill="white")
        return img

# =========================================================
# FULL MAPS (ALL INCLUDED)
# =========================================================
MAPS = {
    "Oregon":{"Basement":"https://i.imgur.com/x2JhPvB.png","1F":"https://i.imgur.com/uDsdMea.png","2F":"https://i.imgur.com/dyhPgyF.png"},
    "Bank":{"Basement":"https://i.imgur.com/sPn2mO3.png","1F":"https://i.imgur.com/vJWm7pt.png","2F":"https://i.imgur.com/bAfcKrS.png"},
    "Border":{"1F":"https://i.imgur.com/ZI3KXBt.png","2F":"https://i.imgur.com/JADGjHD.png"},
    "Clubhouse":{"Basement":"https://i.imgur.com/oqBIcR8.png","1F":"https://i.imgur.com/CKgNgHI.png","2F":"https://i.imgur.com/4Q1OoaN.png"},
    "Chalet":{"Basement":"https://i.imgur.com/QVelV0t.png","1F":"https://i.imgur.com/nHu283j.png","2F":"https://i.imgur.com/8dfimU3.png"},
    "Coastline":{"1F":"https://i.imgur.com/Bme8NFL.png","2F":"https://i.imgur.com/97ubPOm.png"},
    "Consulate":{"Basement":"https://i.imgur.com/dnzG09V.png","1F":"https://i.imgur.com/wFZ87oX.png","2F":"https://i.imgur.com/mpFuA7U.png"},
    "Emerald Plains":{"1F":"https://i.imgur.com/hEVnYhs.png","2F":"https://i.imgur.com/oYWbJ7W.png"},
    "Favela":{"1F":"https://i.imgur.com/O592wA4.png","2F":"https://i.imgur.com/LRZz5mN.png","3F":"https://i.imgur.com/3ybx732.png"},
    "Fortress":{"1F":"https://i.imgur.com/NqGBFDu.png","2F":"https://i.imgur.com/1bkO7U9.png","3F":"https://i.imgur.com/9MNtGVU.png"},
    "House":{"Basement":"https://i.imgur.com/5UI0jFr.png","1F":"https://i.imgur.com/H8RwBW7.png","2F":"https://i.imgur.com/ZS2iNrM.png"},
    "Kafe Dostoyevsky":{"1F":"https://i.imgur.com/dBfaQp7.png","2F":"https://i.imgur.com/fhgTAHw.png","3F":"https://i.imgur.com/KJOK4BF.png"},
    "Kanal":{"Basement":"https://i.imgur.com/uxgVjR3.png","1F":"https://i.imgur.com/3r9ZqKl.png","2F":"https://i.imgur.com/neiCbZl.png"},
    "Outback":{"1F":"https://i.imgur.com/OCy7VKL.png","2F":"https://i.imgur.com/DwmDszl.png"}
}

# =========================================================
# OPERATORS (FULL CORE SET)
# =========================================================
ATTACKERS = [
"Thermite","Ace","Hibana","Ash","Iana","Nomad","Thatcher",
"Sledge","Buck","Zofia","Ying","Capitao","Flores","Montagne",
"Dokkaebi","Lion","Finka","Gridlock","Zero","Amaru","Nokk"
]

DEFENDERS = [
"Smoke","Mute","Jager","Bandit","Mira","Valkyrie","Azami",
"Doc","Rook","Echo","Lesion","Ela","Kapkan","Frost",
"Alibi","Maestro","Wamai","Melusi","Aruni","Thorn","Caveira"
]

# =========================================================
# ROLES
# =========================================================
ROLE = {
"Thermite":"HARD_BREACH","Ace":"HARD_BREACH","Hibana":"HARD_BREACH",
"Ash":"ENTRY","Iana":"ENTRY","Zofia":"ENTRY",
"Thatcher":"SUPPORT","Capitao":"SUPPORT","Nomad":"SUPPORT",

"Smoke":"ANCHOR","Mute":"ANCHOR","Mira":"ANCHOR",
"Jager":"UTILITY","Bandit":"UTILITY","Wamai":"UTILITY",
"Valkyrie":"INFO","Echo":"INFO"
}

def role(op):
    return ROLE.get(op,"FLEX")

# =========================================================
# STACK SIZE
# =========================================================
def stack_size(x):
    return {"Solo":1,"Duo":2,"Trio":3,"Flex":3,"5-Stack":5}[x]

# =========================================================
# TEAM BUILDER
# =========================================================
def build_team(side, your_op, size):
    pool = ATTACKERS if side=="Attack" else DEFENDERS
    your_role = role(your_op)

    team = [your_op]

    for op in pool:
        if len(team) >= size:
            break
        if op == your_op:
            continue
        if role(op) != your_role:
            team.append(op)

    for op in pool:
        if len(team) >= size:
            break
        if op not in team:
            team.append(op)

    return team

# =========================================================
# TIPS
# =========================================================
def tip(op):
    return {
        "Thermite":"Open reinforced wall for execute.",
        "Ace":"Safer long-range breach.",
        "Hibana":"Flexible breach control.",
        "Ash":"Fast entry frag.",
        "Iana":"Intel before push.",
        "Nomad":"Flank control.",
        "Thatcher":"Disable gadgets.",
        "Smoke":"Delay plant.",
        "Mute":"Drone denial.",
        "Jager":"Anti-grenade utility.",
        "Bandit":"Electric wall denial.",
        "Mira":"Angle control.",
        "Valkyrie":"Camera intel."
    }.get(op,"Play your role")

# =========================================================
# MAP OVERLAY
# =========================================================
def draw_map(img, side):
    draw = ImageDraw.Draw(img)
    w,h = img.size

    if side=="Attack":
        points=[("BREACH",(30,50)),("ENTRY",(55,60)),("FLANK",(70,40))]
        color="red"
    else:
        points=[("HOLD",(30,50)),("WATCH",(55,60)),("DENY",(70,40))]
        color="blue"

    for text,(x,y) in points:
        px,py=int(w*x/100),int(h*y/100)

        draw.ellipse((px-18,py-18,px+18,py+18),fill="black")
        draw.ellipse((px-12,py-12,px+12,py+12),fill=color)

        draw.rectangle((px+25,py-18,px+260,py+18),fill="black")
        draw.text((px+30,py-12),text,fill="white")

    return img

# =========================================================
# AI (FULL FIXED OLLAMA)
# =========================================================
def ask_ai(prompt):
    try:
        r = requests.post(
            "http://127.0.0.1:11434/api/chat",
            json={
                "model":"phi3:latest",
                "messages":[
                    {"role":"user","content":prompt}
                ],
                "stream":False
            },
            timeout=120
        )

        if r.status_code != 200:
            return f"HTTP ERROR {r.status_code}: {r.text}"

        return r.json()["message"]["content"]

    except Exception as e:
        return f"AI ERROR: {str(e)}"

# =========================================================
# UI
# =========================================================
st.set_page_config(layout="wide")
st.title("🧠 Siege Trainer v52 (STABLE BASE SYSTEM)")

col1,col2 = st.columns([2,1])

with col1:

    map_name = st.selectbox("Map", list(MAPS.keys()))
    site = st.selectbox("Site", list(MAPS[map_name].keys()))

    side = st.radio("Side", ["Attack","Defense"], horizontal=True)

    your_op = st.selectbox(
        "Your Operator",
        ATTACKERS if side=="Attack" else DEFENDERS
    )

    stack = st.selectbox("Stack Size", ["Solo","Duo","Trio","Flex","5-Stack"])
    size = stack_size(stack)

    img = load_image(MAPS[map_name][site], map_name)
    img = draw_map(img, side)

    st.image(img, use_container_width=True)

    st.markdown("## 🎮 You")
    st.success(f"{your_op} → {role(your_op)}")
    st.write("Tip:", tip(your_op))

    st.markdown("## 👥 Team")

    team = build_team(side,your_op,size)
    for t in team:
        st.write(f"• {t} → {tip(t)}")

with col2:

    st.markdown("## 🤖 AI Coach")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    msg = st.text_input("Ask AI")

    if st.button("Send"):
        prompt = f"""
You are a Rainbow Six Siege coach.

Map: {map_name}
Site: {site}
Side: {side}
Operator: {your_op}
Stack: {stack}

Give short, tactical advice.
"""

        res = ask_ai(prompt)

        st.session_state.chat.append(("You",msg))
        st.session_state.chat.append(("Coach",res))

    for s,m in st.session_state.chat[::-1]:
        st.write(f"**{s}:** {m}")
