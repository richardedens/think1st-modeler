###############################################################
#     _     _       _           _      _         _   
#    | |_  | |__   (_)  _ __   | | __ / |  ___  | |_ 
#    | __| | '_ \  | | | '_ \  | |/ / | | / __| | __|
#    | |_  | | | | | | | | | | |   <  | | \__ \ | |_ 
#     \__| |_| |_| |_| |_| |_| |_|\_\ |_| |___/  \__|
#                                       my@think1st.app
#
##############################################################

# External libraries.
from runtime import baseserver, colorer
from waitress import serve
from app import app
from gui import main

# Installed packages.
import time
import threading
import logging
import sys

# Setup loging
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format='%(message)s',
)

# Create a welcome header.
def get_welcome_header():
    welcome_ascii_header = '''
     _     _       _           _      _         _   
    | |_  | |__   (_)  _ __   | | __ / |  ___  | |_ 
    | __| | '_ \  | | | '_ \  | |/ / | | / __| | __|
    | |_  | | | | | | | | | | |   <  | | \__ \ | |_ 
     \__| |_| |_| |_| |_| |_| |_|\_\ |_| |___/  \__|
                                     my@think1st.app
    '''
    return welcome_ascii_header

# Define the base server
def server():
    serve(app)

if __name__ == "__main__":
    logging.warning(get_welcome_header())

    # Start the internal webserver.
    webServer = threading.Thread(target=server)
    webServer.start()

    # Start the main window.
    mainWindow = threading.Thread(target=main)
    mainWindow.start()

    # Join threads.
    webServer.join()
    mainWindow.join()