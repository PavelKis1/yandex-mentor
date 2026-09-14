@echo off
cd /d C:\Users\Pavel\Desktop\yandex_review
call npx -y playwright@1.57.0 install chromium > logs\pw_install.log 2>&1
echo DONE >> logs\pw_install.log