#! /usr/bin/env bash

#fusermount -zu /project/grane-passive
#fusermount -zu /project/snorre-passive
fusermount -zu /project
#fusermount -zu /project/snorre-passive

#mkdir -p /project/grane-passive
#mkdir -p /project/snorre-passive
mkdir -p /project

#sudo sshfs -o allow_other stoo@st-linrgsn239.st.statoil.no:/project/grane-passive /project/grane-passive
#sudo sshfs -o allow_other stoo@st-linrgsn239.st.statoil.no:/project/snorre-passive /project/snorre-passive
sudo sshfs -o allow_other stoo@be-linrgsn154.be.statoil.no:/project /project
