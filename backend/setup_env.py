import os
from pathlib import Path

def setup_environment():
    """Set up environment variables for the application."""
    env_file = Path('.env')
    
    if env_file.exists():
        print('Environment file already exists. Do you want to overwrite it? (y/n)')
        if input().lower() != 'y':
            print('Setup cancelled.')
            return
    
    print('\nSetting up environment variables...')
    print('Please enter the following information:')
    
    # Google Calendar API credentials
    print('\nGoogle Calendar API:')
    client_id = input('Enter your Google Client ID: ').strip()
    client_secret = input('Enter your Google Client Secret: ').strip()
    
    # OpenAI API key
    print('\nOpenAI API:')
    openai_key = input('Enter your OpenAI API key: ').strip()
    
    # Google Maps API key
    print('\nGoogle Maps API:')
    maps_key = input('Enter your Google Maps API key: ').strip()
    
    # Write to .env file
    env_content = f'''# Google Calendar API credentials
GOOGLE_CLIENT_ID={client_id}
GOOGLE_CLIENT_SECRET={client_secret}

# OpenAI API key
OPENAI_API_KEY={openai_key}

# Google Maps API key
GOOGLE_MAPS_API_KEY={maps_key}
'''
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print('\nEnvironment variables have been set up successfully!')
    print('Make sure to add .env to your .gitignore file to keep your credentials secure.')

if __name__ == '__main__':
    setup_environment() 