
import asyncio
import getpass

from matrix_connect import *
from dotenv import load_dotenv, dotenv_values

import collections


if __name__ == '__main__':

    if load_dotenv(verbose=True) == False :
        print("[ERR]\t.env file did not load!")
        exit()
    
    # env_vals = collections.OrderedDict()
    env_vals = dotenv_values(verbose=True)
    password : str
    username : str
    
                
   
      # Get user credentials
    if env_vals.get('IS_TEST', False) :
        password = env_vals.get('PW') 
        username = env_vals.get('UNAME1')
    else :
        username = input("Enter username:")
        password = getpass.getpass("Enter your Matrix password:")
    homeserver_url = "https://aria.im" #@nikreedog:aria-net.org input("Enter the Matrix homeserver URL: ")
    # Run the login and sync function
    asyncio.get_event_loop().run_until_complete(login_and_sync(homeserver_url, username, password))
    exit()