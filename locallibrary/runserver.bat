@echo off
color A
echo 1^> runserver
echo 2^> makemigrations ^& migrate
set /p choice=Choice^>

if "%choice%"=="1" GOTO runserver
if "%choice%"=="2" GOTO migrate

:runserver
set /p run=Port^>
python ./manage.py runserver %run%
exit /b

:migrate
python ./manage.py makemigrations
python ./manage.py migrate
exit /b