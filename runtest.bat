@echo off
rem encodig=GB2312

rem 设置控制台颜色
color 07

set version=[V0.99.1]
title 正在执行_版本%version%
echo **********************************************************************
echo *************************【自动化案例构建开始】***********************
echo *************************【版本%version%】****************************
set pypath="%cd%\venv\Scripts\python.exe"
echo %pypath%
if exist %pypath% (
    echo *************************【使用项目环境下Python解释器执行】***********
    %pypath% runtest.py
) else (
    echo *************************【使用系统环境变量下Python解释器执行】*******
    python runtest.py
)
echo *************************【自动化案例构建结束】***********************
title 执行结束_版本%version%
pause