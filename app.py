import streamlit as st
import hashlib, time
import qrcode
import io
import pandas as pd
from PIL import Image
import uuid

# ----- Blockchain Classes ---------------
class Block:
    def __init__(self, ticket_id, event, user, prev_hash=""):
        self.ticket_id = ticket_id
        self.event = event
        self.user = user
        self.timestamp = time.time()
        self.prev_hash = prev_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = str(self.ticket_id) + self.event + self.user + str(self.timestamp) + self.prev_hash
        return hashlib.sha256(data.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block("GENESIS", "Genesis Event", "System", "0")

    def add_block(self, ticket_id, event, user):
        prev_block = self.chain[-1]
        new_block = Block(ticket_id, event, user, prev_block.hash)
        self.chain.append(new_block)

    def verify_ticket(self, ticket_id):
        for block in self.chain[1:]:
            if block.ticket_id == ticket_id:
                return True, block.hash
        return False, None

# ---------- Main categories with background images -----------------
backgrounds = {
    "Entertainment Events": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=1600&q=80",
    "Sports Events": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=1600&q=80",
    "Educational & Professional Events": "https://images.unsplash.com/photo-1503428593586-e225b39bddfe?auto=format&fit=crop&w=1600&q=80",
    "Festivals & Cultural Events": "https://images.unsplash.com/photo-1496024840928-4c417adf211d?auto=format&fit=crop&w=1600&q=80",
    "Exhibition & Expo Events": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1600&q=80",
    "Lifestyle & Fashion Events": "https://images.unsplash.com/photo-1607082350899-7e105aa886ae?auto=format&fit=crop&w=1600&q=80"
}

# ------------ Sub-events per category ------------------
sub_events = {
    "Entertainment Events": ["Concerts", "Stand-up Comedy", "Theatre Plays", "Movie Premieres"],
    "Sports Events": ["Football Match", "Hockey", "Badminton", "Cricket"],
    "Educational & Professional Events": ["Workshop", "Webinar", "Seminar"],
    "Festivals & Cultural Events": ["Holi", "Music Festival", "Food Festival"],
    "Exhibition & Expo Events": ["Trade Expo", "Art Exhibition"],
    "Lifestyle & Fashion Events": ["Shopping Bazaar", "Fashion Show"]
}

# -------------  Sidebar selection ------------------
st.sidebar.title(" Event Categories")
category = st.sidebar.selectbox("Choose Category", list(backgrounds.keys()))
sub_event_choice = st.sidebar.selectbox("Choose Sub Event", sub_events[category])

# ---------------  Top banner -----------------
st.markdown(
    """
    <style>
    .top-banner {
        background: linear-gradient(90deg, #FF4B4B, #FF7B7B);
        padding: 20px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        color: white;
        margin-bottom: 20px;
    }
    .top-banner h1 {
        margin: 0;
        font-size: 28px;
    }
    .top-banner p {
        margin: 0;
        font-size: 16px;
    }
    </style>
    <div class="top-banner">
        <div>
            <h1>Secure Event Ticket Booking</h1>
            <p>Blockchain-based verification system</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --------  Hero banner with category background -------------
selected_bg = backgrounds[category]
st.markdown(
    f"""
    <style>
    .hero {{
        background-image: url("{selected_bg}");
        background-size: cover;
        background-position: center;
        height: 320px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        margin-bottom: 20px;
    }}
    .hero h1 {{
        font-size: 42px;
        text-shadow: 2px 2px 6px #000;
    }}
    </style>
    <div class="hero">
        <h1>{category}</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# --------  Form section below the image  ---------
st.markdown("<div style='background-color: rgba(255,255,255,0.95); padding: 25px; border-radius: 12px;'>", unsafe_allow_html=True)

# Persist blockchain in session_state
if "bc" not in st.session_state:
    st.session_state.bc = Blockchain()

col1, col2 = st.columns(2)

# Auto-generate unique ticket IDs
def generate_ticket_id():
    return f"t{len(st.session_state.bc.chain)}"
    # Alternative: return f"t{uuid.uuid4().hex[:6]}"

with col1:
    st.subheader("Book a Ticket")
    user_name = st.text_input("Enter Your Name")
    if st.button("Book Ticket"):
        if user_name:
            ticket_id = generate_ticket_id()
            st.session_state.bc.add_block(ticket_id, f"{category} - {sub_event_choice}", user_name)
            st.success(f"Ticket {ticket_id} booked for {sub_event_choice}!")

            # Show updated tickets immediately
            data = [
                {"Ticket ID": b.ticket_id, "Event": b.event, "User": b.user, "Hash": b.hash[:10]+"..."}
                for b in st.session_state.bc.chain[1:]
            ]
            st.dataframe(pd.DataFrame(data))
        else:
            st.error("Please enter User Name.")

with col2:
    st.subheader("Verify a Ticket")
    verify_id = st.text_input("Enter Ticket ID to Verify")
    if st.button("Verify Ticket"):
        valid, hash_val = st.session_state.bc.verify_ticket(verify_id)
        if valid:
            st.success(f"Ticket {verify_id} is valid! Hash: {hash_val[:10]}...")
        else:
            st.error("Ticket not found.")

# -------  Show tickets in a table -----------
st.subheader("Show All Tickets")
data = [
    {"Ticket ID": b.ticket_id, "Event": b.event, "User": b.user, "Hash": b.hash[:10]+"..."}
    for b in st.session_state.bc.chain[1:]
]
if data:
    st.dataframe(pd.DataFrame(data))
else:
    st.info("No tickets booked yet.")

# -------  QR Code Generator --------------
def generate_qr(ticket_id, event, user):
    data = f"TicketID:{ticket_id}, Event:{event}, User:{user}"
    qr = qrcode.make(data)
    return qr

if st.button("Generate QR for Last Ticket"):
    if len(st.session_state.bc.chain) > 1:
        last_block = st.session_state.bc.chain[-1]
        qr_img = generate_qr(last_block.ticket_id, last_block.event, last_block.user)
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="Scan this QR to verify ticket", width=300)
    else:
        st.error("No ticket booked yet.")

st.markdown("</div>", unsafe_allow_html=True)
