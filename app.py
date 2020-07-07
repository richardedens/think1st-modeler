#  
#   ---------------------------------------------------------------------------------------
#     _     _       _           _      _         _   
#    | |_  | |__   (_)  _ __   | | __ / |  ___  | |_ 
#    | __| | '_ \  | | | '_ \  | |/ / | | / __| | __|
#    | |_  | | | | | | | | | | |   <  | | \__ \ | |_ 
#     \__| |_| |_| |_| |_| |_| |_|\_\ |_| |___/  \__|
#                                     my@think1st.app
#
#   ---------------------------------------------------------------------------------------
#   Author:         Gerhard Richard Edens
#   Publisher:      Think1st
#   Date:           07/07/2020 
#   Description: 
#   
#   This is the startup main python script that will run the modeler and the internal webserver.
#   ---------------------------------------------------------------------------------------
#

# External libraries.
from runtime import colorer
from waitress import serve
from t1webserver import t1webserver
from t1modeler import t1modeler

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
    serve(t1webserver)
# Define the base server
def modeler():
    t1modeler()

if __name__ == "__main__":
    logging.warning(get_welcome_header())

    # Start the internal webserver.
    webServer = threading.Thread(target=server)
    webServer.start()

    # Start the main window.
    mainWindow = threading.Thread(target=modeler)
    mainWindow.start()

    # Join threads.
    webServer.join()
    mainWindow.join()