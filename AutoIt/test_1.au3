Dim $a, $b
; ��궨λ
$a = ControlFocus("��", "", "[ID:1148]")
;MsgBox(4096, "����", $a , 10)
;C:\Sql\Procedure\arcs_arcsm_risktemplatemgr_or.sql
$b = ControlSetText("��", "", "[CLASS:Edit]", "C:\Users\zhangzheng17239\Desktop\test_1.au3")
;MsgBox(4096, "����", $b , 10)
ControlClick("��", "��(&O)", "[CLASS:Button]", "left")