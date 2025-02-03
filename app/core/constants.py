# user.py
JWT_LEFITIME_SECONDS = 3600
PASSWORD_MIN_LENGTH = 3
PASSWORD_LENGTH_ERROR = 'Password should be at least 3 characters'
PASSWORD_EMAIL_ERROR = 'Password should not contain e-mail'
TOKEN_URL = 'auth/jwt/login'
USER_HAS_REGISTERED = 'Пользователь {} зарегистрирован.'

# google_client.py
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
