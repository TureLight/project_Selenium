Dim $a, $b
; 光标定位
$a = ControlFocus("打开", "", "[ID:1148]")
;MsgBox(4096, "测试", $a , 10)
;C:\Sql\Procedure\arcs_arcsm_risktemplatemgr_or.sql
$b = ControlSetText("打开", "", "[CLASS:Edit]", "C:\Users\zhangzheng17239\Desktop\test_1.au3")
;MsgBox(4096, "测试", $b , 10)
ControlClick("打开", "打开(&O)", "[CLASS:Button]", "left")