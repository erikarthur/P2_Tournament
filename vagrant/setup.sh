#!/bin/bash
dropdb tournament
createdb tournament
psql -d tournament -f tournament.sql
