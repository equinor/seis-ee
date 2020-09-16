#! /usr/bin/env bash

fusermount -zu /project/grane-passive
fusermount -zu /project/snorre-passive

mkdir -p /project/grane-passive
mkdir -p /project/snorre-passive

sudo sshfs -o allow_other stoo@st-linrgsn239.st.statoil.no:/project/grane-passive /project/grane-passive
sudo sshfs -o allow_other stoo@st-linrgsn239.st.statoil.no:/project/snorre-passive /project/snorre-passive
