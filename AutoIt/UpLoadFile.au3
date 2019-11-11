WinActivate("文件上传");
WinWaitActive("文件上传");
;ControlSetText("文件上传", "", "[CLASS:Edit; INSTANCE:1]", "C:\Users\zhangzheng17239\Desktop\作业.png")
ControlSetText("文件上传", "", "[CLASS:Edit; INSTANCE:1]", $CmdLine[1])  ; $CmdLine[1] 上传文件路径
ControlClick("文件上传", "", "[CLASS:Button; INSTANCE:1]", "left")