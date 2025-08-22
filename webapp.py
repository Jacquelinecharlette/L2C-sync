import streamlit as st
import requests
import json
from msal import ConfidentialClientApplication

# Azure AD app details (from your App Registration)
CLIENT_ID = "your-client-id"
TENANT_ID = "your-tenant-id"
CLIENT_SECRET = "your-client-secret"   # Create in Certificates & Secrets
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["User.Read"]   # Basic scope to read user profile

# Initialize MSAL client
app = ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET,
)

# Get token
result = app.acquire_token_for_client(scopes=SCOPE)

if "access_token" in result:
    access_token = result["access_token"]

    # Call Microsoft Graph API (/me)
    graph_endpoint = "https://graph.microsoft.com/v1.0/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(graph_endpoint, headers=headers)

    st.write("Graph API Response:")
    st.json(response.json())

else:
    st.error("Could not acquire token: " + str(result.get("error_description")))

 
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
