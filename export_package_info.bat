@echo off
rem encodig=GB2312
echo **********************************************************************
echo ***********************������Python��������Ϣ��***********************
set pypath="%cd%\venv\Scripts\pip.exe"
rem echo %pypath%
if exist %pypath% (
    echo ***********************����⵽��ĿĿ¼��Python��������***************
    echo # ��ĿĿ¼��Python������package��Ϣ > %cd%\package_info.txt
    %pypath% freeze >> %cd%\package_info.txt
) else (
    echo ***********************��δ��⵽��ĿĿ¼��Python��������ʹ�û���������Python��������************
    echo # ϵͳ����������Python������package��Ϣ > %cd%\package_info.txt
    pip freeze >> %cd%\package_info.txt
)
echo ***********************������Python����Ϣ��ɡ�***********************
pause