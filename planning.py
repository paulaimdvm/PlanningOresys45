import streamlit as st
from supabase import create_client

# ==============================
# 🔑 CONFIG SUPABASE
# ==============================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Mon planning", layout="centered")

st.title("📅 Mon activité")

# ==============================
# 📝 INPUT UTILISATEUR
# ==============================
trigramme = st.text_input("Entre ton trigramme (ex: ABC)").upper().strip()

# ==============================
# 🎯 PLANNING (à adapter librement)
# ==============================
planning = {
    "Visite immersive": "📍  [A compléter]",
    "Excursion à vélo": "📍 [A compléter]",
    "Initiation surf": "📍 [A compléter]" ,
    "Paddle & Kayak": "📍 [A compléter]" ,
}

# ==============================
# 🔍 RECHERCHE
# ==============================
if st.button("Voir mon planning"):

    if trigramme == "":
        st.warning("⚠️ Merci d'entrer un trigramme")
    else:
        try:
            # ✅ chercher l'inscription
            res = supabase.table("inscriptions") \
                .select("*") \
                .ilike("trigramme", trigramme) \
                .execute()

            # 🔍 RESULTAT
            if res.data:
                activite = res.data[0]["activite"]

                st.success(f"✅ Tu es inscrit à : {activite}")

                # ✅ afficher planning
                if activite in planning:
                    st.info(f"📅 {planning[activite]}")
                else:
                    st.warning("⚠️ Planning non défini pour cette activité")

            else:
                st.error("❌ Aucune inscription trouvée pour ce trigramme")

        except Exception as e:
            st.error(f"🔥 Erreur : {e}")
