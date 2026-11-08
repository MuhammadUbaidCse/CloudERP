@echo off
title MTECH ERP Local Server (Google Sync Ready)
cd /d "c:\Users\Muham\Desktop\Mangment Sys"
start "" http://localhost:8000/Mangment%%202.html
echo ========================================================
echo MTECH ERP Server Active on http://localhost:8000
echo Google OAuth & Cloud Sync is ready!
echo Keep this window open while using Google Cloud Sync.
echo ========================================================
py -3 -m http.server 8000
pause
