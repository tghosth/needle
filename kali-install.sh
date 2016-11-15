#!/bin/bash

# Install Git
sudo apt-get install git

# clone the needle repository and choose the relevant branch 
git clone https://github.com/tghosth/needle.git
cd needle
git checkout bleeding-edge


# Unix packages
sudo apt-get install python2.7 python2.7-dev pip sshpass sqlite3 lib32ncurses5-dev

# Python packages
sudo pip install readline
sudo pip install paramiko
sudo pip install sshtunnel
sudo pip install frida
sudo pip install mitmproxy	
