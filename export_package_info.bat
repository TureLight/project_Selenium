@echo off
rem encodig=GB2312
echo **********************************************************************
echo ***********************【导出Python环境包信息】***********************
set pypath="%cd%\venv\Scripts\pip.exe"
rem echo %pypath%
if exist %pypath% (
    echo ***********************【检测到项目目录下Python解释器】***************
    echo # 项目目录下Python第三方package信息 > %cd%\package_info.txt
    %pypath% freeze >> %cd%\package_info.txt
) else (
    echo ***********************【未检测到项目目录下Python解释器，使用环境变量下Python解释器】************
    echo # 系统环境变量中Python第三方package信息 > %cd%\package_info.txt
    pip freeze >> %cd%\package_info.txt
)
echo ***********************【导出Python包信息完成】***********************
pause