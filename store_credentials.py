import yagmail
import keyring

EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"  # Use App Password, NOT your main Gmail password!

# Store credentials securely
keyring.set_password("yagmail", EMAIL_SENDER, EMAIL_PASSWORD)
print("✅ Credentials stored securely!")
