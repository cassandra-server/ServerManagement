#!/bin/bash
mkdir $HOME/.ServerManagement

wget https://github.com/MiguelSanchezP/ServerManagement/archive/master.zip -P $HOME/.ServerManagement/

unzip $HOME/.ServerManagement/master.zip && mv $HOME/.ServerManagement/ServerManagement-master/* $HOME/.ServerManagement/* && rm -r $HOME/.ServerManagement/ServerManagement-master/
