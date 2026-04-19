# Blockchain Ticket Booking System

A simple blockchain-based event ticket booking system built with **Python** and **Streamlit**.  
This project demonstrates core blockchain concepts (blocks, hashing, chaining, verification) applied to ticketing, with QR code generation and a clean UI.

## Features
- Book Tickets: Users can book tickets for different event categories and sub-events.
- Blockchain Ledger: Each ticket booking is stored as a block with a unique SHA-256 hash.
- Verification: Tickets can be verified against the blockchain chain.
- QR Code Generation: Each ticket generates a QR code for easy verification.
- Interactive UI: Built with Streamlit, featuring hero banners, forms, and tables.

## Project Structure
BLOCKCHAIN/
├── app.py              # Main Streamlit application (blockchain ticket booking logic + UI)
├── index.html          # Static HTML file 
├── script.js           # JavaScript file
├── style.css           # CSS file for styling beyond Streamlit
├── requirements.txt    # Python dependencies (streamlit, qrcode, pandas, pillow)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Trishika295/Secure-Event-Ticket-Booking.git
   cd blockchain
2. Install dependencies:
   pip install -r requirements.txt
3. Run the app:
   streamlit run app.py


