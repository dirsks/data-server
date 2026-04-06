@echo off
title DataStore Server Setup

echo Installing dependencies...
npm install express

echo Starting server
node server.js

pause