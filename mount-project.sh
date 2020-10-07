#! /usr/bin/env bash

sudo fusermount -zu /project

mkdir -p /project

# Here you can find Grane and Snorre
#sudo sshfs -o allow_other stoo@st-linrgsn239.st.statoil.no:/project /project
# Here Oseberg is available
sudo sshfs -o allow_other stoo@be-linrgsn154.be.statoil.no:/project /project
