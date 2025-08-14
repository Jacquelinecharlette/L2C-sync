import streamlit as st
import json
 
# Page title
st.title("📩 Send a Message to MS Teams")
 
# Sender info
st.header("Sender Information")
sender_name = st.text_input("Your Name")
sender_email = st.text_input("Your Email")
 
# Recipient info
st.header("Recipient Information")
recipient_name = st.text_input("Recipient Name")
recipient_email = st.text_input("Recipient Email")
 
# Message
st.header("Message")
message_text = st.text_area("Type your message here...")
 
# Send button
if st.button("Send"):
    if sender_name and sender_email and recipient_name and recipient_email and message_text:
        
        # Create JSON payload
        payload = {
            "sender": {
                "name": sender_name,
                "email": sender_email
            },
            "recipient": {
                "name": recipient_name,
                "email": recipient_email
            },
            "message": message_text
        }
 
        # Convert to JSON string
        json_payload = json.dumps(payload, indent=4)
 
        st.success("✅ Message ready to send!")
        st.code(json_payload, language="json")  # Show JSON in the app
 
        # Placeholder: send to MS Teams API
        # requests.post(teams_webhook_url, data=json_payload, headers={'Content-Type': 'application/json'})
 
    else:
        st.error("⚠️ Please fill in all fields before sending.")
 
# Preview section
st.markdown("---")
st.subheader("📤 Message Preview")
if sender_name or recipient_name or message_text:
    st.write(f"**From:** {sender_name if sender_name else '—'} ({sender_email if sender_email else '—'})")
    st.write(f"**To:** {recipient_name if recipient_name else '—'} ({recipient_email if recipient_email else '—'})")
    st.write(f"**Message:** {message_text if message_text else '—'}")
else:
    st.write("_No message yet_")
