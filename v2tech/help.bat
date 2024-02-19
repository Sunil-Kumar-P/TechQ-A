@echo off

REM Set the path to your virtual environment
set VENV_PATH=.\venv

REM Check if the first argument is "activate"
IF "%1%"=="venv" (
    REM Activate the virtual environment
    call %VENV_PATH%\Scripts\activate
) ELSE IF "%1%"=="install" (
    pip install -r requirement.txt 
) ELSE IF "%1%"=="server" (
    python manage.py runserver %2%
) ELSE IF "%1%"=="migrate" (
    python manage.py makemigrations
    python manage.py migrate
) ELSE IF "%1%"=="superuser" (
    python manage.py createsuperuser
) ELSE IF "%1%"=="-venv" (
    deactivate
) ELSE IF "%1%"=="init" (
    virtualenv venv
) ELSE IF "%1%"=="first" (
    pip install virtualenv
    virtualenv venv
    call %VENV_PATH%\Scripts\activate
    pip install -r requirement.txt
    python manage.py runserver
) ELSE IF "%1%"=="run" (
    call %VENV_PATH%\Scripts\activate
    python manage.py runserver
) ELSE IF "%1%"=="shell" (
    python manage.py shell
) ELSE (
    REM Handle unrecognized command
    echo Unrecognized command: %1% 
    echo  instead can use the below commands
    echo  help.bat first
    echo  help.bat run
    echo  help.bat migrate
    echo  help.bat superuser
    echo  help.bat venv 
    echo  help.bat shell 

)
