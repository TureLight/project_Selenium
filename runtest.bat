@echo off
rem encodig=GB2312

rem ���ÿ���̨��ɫ
color 07

set version=[V0.99.1]
title ����ִ��_�汾%version%
echo **********************************************************************
echo *************************���Զ�������������ʼ��***********************
echo *************************���汾%version%��****************************
set pypath="%cd%\venv\Scripts\python.exe"
echo %pypath%
if exist %pypath% (
    echo *************************��ʹ����Ŀ������Python������ִ�С�***********
    %pypath% runtest.py
) else (
    echo *************************��ʹ��ϵͳ����������Python������ִ�С�*******
    python runtest.py
)
echo *************************���Զ�����������������***********************
title ִ�н���_�汾%version%
pause