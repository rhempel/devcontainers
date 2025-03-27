@echo off
REM Script to create desktop shortcuts to OpenOCD for each supported MCU
REM
REM NOTE: Tested on Windows 11 only!
REM
REM See https://superuser.com/a/392082 for details on how this
REM shortcut generator script works.
REM
REM Get the latest OpenOCD for Windows as a .tar.gz here:
REM
REM https://github.com/openocd-org/openocd/releases
REM
REM Open the openocd-xxxxxxx-i686-w64-mingw32.tar.gz file and extract
REM the contents to a convenient path. You will need this path for the
REM next step. The easiest thing to do is right click on the folder
REM that you extracted the download to and pick "Copy as path". You can
REM paste the path into the command below.
REM
REM Usage:
REM
REM make_open_ocd_shortcuts path\to\openocd
REM
REM =====================================================================
REM Set up the path to the DESKTOP - put all the shortcuts there so they
REM are easy to find and give the user the freedom to move them anywhere
REM that is convenient
REM
for /f "tokens=*" %%i in ('powershell -command "[Environment]::GetFolderPath(\"Desktop\")"') do set DESKTOP=%%i

REM Set up a temporary location for the VBS script that will be executed
REM to actually create the shortcut
REM
set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"

REM Remove any quotes around the path to openocd and set up a variable
REM that we can use in the script generator. For details on how this
REM works, see https://stackoverflow.com/a/21771437
REM 
setlocal enableDelayedExpansion
for /f "delims=" %%A in ("%1") do endlocal & set "openocd_path=%%~A"

echo executable is "%openocd_path%\bin\openocd.exe"

goto:main

REM This function builds the script for a specific board. First pass
REM at this function accepts the board as a parameter but we may
REM instead choose to make it a more complex string to give us
REM flexibility in how we call openocd.
REM
REM The function builds the script line by line and then executes
REM it to generate the shortcut.
REM
:make_openocd_shortcut
    echo fibblesnork %1

    echo Set oWS = WScript.CreateObject("WScript.Shell") > %SCRIPT%
    echo sLinkFile = "%DESKTOP%\OpenOCD %1.lnk" >> %SCRIPT%
    echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
    echo oLink.Description = "Start OpenOCD for %1" >> %SCRIPT%
    echo oLink.IconLocation = "%SystemRoot%\System32\SHELL32.dll, 12" >> %SCRIPT%
    echo oLink.TargetPath = "%openocd_path%\bin\openocd.exe" >> %SCRIPT%
    echo oLink.Arguments = "-f board/%1.cfg -c ""adapter speed 4000"" -c ""bindto 0.0.0.0""" >> %SCRIPT%
    echo oLink.WorkingDirectory = "%openocd_path%" >> %SCRIPT%
    echo oLink.Save >> %SCRIPT%

    cscript /nologo %SCRIPT%

    exit /B 0

:main
    call:make_openocd_shortcut st_nucleo_h7
    call:make_openocd_shortcut st_nucleo_g0
    call:make_openocd_shortcut st_nucleo_g4
    call:make_openocd_shortcut st_nucleo_f0
    call:make_openocd_shortcut pico-debug
    call:make_openocd_shortcut nordic_nrf52_dk
