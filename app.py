import streamlit as st
from supabase import create_client

supabase = create_client("URL", "KEY")

st.title("🚴 Rider App")
st.header("You are ready to drive") # 
st.write("Your account is now activated. Let's bank your first load.") # 

shipments = supabase.table("shipments").select("*").neq("status", "Completed").execute()

for s in shipments.data:
    with st.expander(f"Order {s['shipment_no']}"):
        st.write(f"📍 {s['origin']} ➡ {s['destination']}")
        
        # Coordinate Alignment Logic
        curr_gps = st.text_input("Current GPS (Lat, Long)", key=f"gps_{s['id']}")
        
        col1, col2 = st.columns(2)
        if col1.button("Arrive at Source", key=f"src_{s['id']}"):
            if curr_gps == s['source_coords']: # Logic: coordinates line up 
                supabase.table("shipments").update({"status": "Active"}).eq("id", s['id']).execute()
                st.success("GPS Match. Order Picked Up.")
        
        # Handoff Logic
        if col2.button("Pass Order", key=f"pass_{s['id']}"): # Logic: pass on if not confirmed 
            supabase.table("shipments").update({"current_rider_id": None}).eq("id", s['id']).execute()
            st.warning("Order passed to next rider.")
