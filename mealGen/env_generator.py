from cryptography.fernet import Fernet
# from dotenv import load_dotenv, set_key
import os

def generate_key_and_update_env(env_path='.env', key_name='ENCRYPTION_KEY'):
    # Load existing .env file or create it if it doesn't exist
    if not os.path.exists(env_path):
        with open(env_path, 'w'): pass
    load_dotenv(env_path)

    # Generate a new encryption key
    key = Fernet.generate_key()

    # Add or update the encryption key in the .env file
    set_key(env_path, key_name, key.decode())

if __name__ == "__main__":
    generate_key_and_update_env()