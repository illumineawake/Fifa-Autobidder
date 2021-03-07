import os.path
import threading
from os import path

import autobidder
import autobuyer
import helpers
from autobidder import Autobidder
from autobuyer import Autobuyer
from helpers import *


# Each button starts a new thread
class RunThread(threading.Thread):
    def __init__(self, queue, driver, action, auxiliary, futbinurl):
        threading.Thread.__init__(self)
        self.action = action
        self.queue = queue

        # auxiliary = parent autobidder object
        self.auxiliary = auxiliary
        self.driver = driver
        self.futbinurl = futbinurl

        # maybe create Helper object in GUI class 
        # if object throws exception does it lose its class variables?
        # if not, helper obj created on init 


    def run(self):
        if self.action == "test":
            self.queue.put("Running test function")

            autobidder.manageWatchlist()

        if self.action == "autobidder":
            self.queue.put("Starting autobidder")
            # log_event("Test function")
            # testhelper = Helper(self.driver)
            # testhelper.start()
            # autobidder = Autobidder(self.driver, self.queue)
            self.auxiliary.initializeBot()

        if self.action == "autobidder_devmode":
            self.queue.put("Starting autobidder - dev mode")
            # log_event("Test function")
            # testhelper = Helper(self.driver)
            # testhelper.start()
            autobidder = Autobidder(self.driver, self.queue)
            autobidder.initializeBot()

        if self.action == "watchlist":
            self.queue.put("Managing watchlist")
            # log_event("Test function")
            # testhelper = Helper(self.driver)
            # testhelper.start()
            self.auxiliary.manageWatchlist()

        if self.action == "autobuyer":
            self.queue.put("Starting autobuyer")
            # autobuyer = Autobuyer(self.driver, self.queue)
            # autobuyer.start()

        if self.action == "login":
            self.queue.put("Logging in")
            # log_event("AutoLogin...")
            
            txt = open("./data/logins.txt", "r")
            counter = 0
            credentials = []
            for aline in txt:
                counter += 1
                line = aline.strip("\n")
                credentials.append(str(line))
            txt.close()

            USER = {
                "email": credentials[0],
                "password": credentials[1],
            }

            EMAIL_CREDENTIALS = {
                "email": credentials[2],
                "password": credentials[3],
            }

            login(self.driver, USER, EMAIL_CREDENTIALS)
            # Set user's starting coins
            self.auxiliary.helper.setStartingCoins()

        if self.action == "getFutbinDataFromURL":
            self.queue.put("Fetching player info")
            log_event("Fetching player info...")

            helper = Helper(self.driver)
            helper.getFutbinDataAndPopulateTable(self.futbinurl)