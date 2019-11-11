# coding=utf-8

class ReportHtml(object):
    HTML = \
"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
%(HTML_HEAD_TITLE)s
    <style type="text/css">

        * { margin: 0; padding: 0 }
        html, body { width: 100%%; height: 100%%; font-size: 12px;}
        table {  border-collapse: collapse; table-layout: fixed ;bgcolor:#F0E68C}
        td { vertical-align: baseline; font-size: 12px }

    </style>
  </head>

  <body leftmargin="8" marginwidth="0" topmargin="8" marginheight="4" offset="0">
%(HTML_BODY_TABLE)s
  </body>
</html>\n
"""

    HTML_HEAD_TITLE = \
"""
    <title>第%(BUILD_NUMBER)s次构建日志</title>\n
"""

    HTML_BODY_TABLE = \
"""
    <table width="95%%" cellpadding="0" cellspacing="0" style="font-size: 11pt; font-family: Tahoma, Arial, Helvetica, sans-serif">
      <tr><td><font color="#FF0000">(本邮件是程序自动下发的，请勿回复！)</td></tr>
      <tr><td><h2><font color="#0000FF">构建结果 - %(BUILD_STATUS)s</font></h2></td></tr>
      <tr><td><br /><b><font color="#0B610B">构建信息</font></b><hr size="2" width="100%%" align="center" /></td></tr>
      <tr>
	    <td>
          <ul>
            <li>项目名称：&nbsp;%(PROJECT_NAME)s</li>
            <li>构建编号：&nbsp;第%(BUILD_NUMBER)s次构建</li>
            <li>触发原因：&nbsp;%(CAUSE)s</li>
            <li>构建日志：&nbsp;请查看Log目录</li>    
          </ul>
        </td>
       </tr>
      <tr><td><br /><b><font color="#0B610B">测试计划执行结果统计</font></b><hr size="2" width="100%%" align="center" /></td></tr>
      <tr>
	    <td>
          <br />
        </td>
	  </tr>
        <table align="center" class="details" border="1" cellpadding="5" cellspacing="2" width="95%%" bgcolor="#FAFAD2">
           <tbody>
            <tr valign="top" bgcolor="#87CEFA" name="line">
             <th>测试计划</th>
             <th>案例个数</th>
             <th>成功</th>
             <th>失败</th>
             <th>成功率</th>
             <th>失败率</th>
            </tr>
%(HTML_BODY_TABLE_TBODY_TR)s
            <tr valign="top" bgcolor="#87CEFA">
             <td align="center"><b>总计</b></td>
             <td align="center"><b>%(CASE_COUNT)s</b></td>
             <td align="center"><b>%(SUCCESS_COUNT)s</b></td>
             <td align="center"><b>%(FAILURE_COUNT)s</b></td>
             <td align="center">%(SUCCESS_RATE).2f</td>
             <td align="center">%(FAILURE_RATE).2f</td>
            </tr>
           </tbody>
        </table>
        </td>
	  </tr>
      <tr>
	    <td>
          <br />
        </td>
	  </tr>
      <tr><td ><b><font color="#FF0000">用例执行详细清单及失败原因见附件 %(ATTACHED_FILE)s</font></b></td></tr>
    </table>\n
"""

    HTML_BODY_TABLE_TBODY_TR = \
"""
            <tr valign="top">
             <td align="center">%(TEST_PLAN_NAME)s</td>
             <td align="center">%(TEST_PLAN_CASE_COUNT)s</td>
             <td align="center">%(TEST_PLAN_SUCCESS_COUNT)s</td>
             <td align="center" bgcolor="#F08080">%(TEST_PLAN_FAILURE_COUNT)s</td>
             <td align="center">%(TEST_PLAN_SUCCESS_RATE).2f</td>
             <td align="center" bgcolor="#F08080">%(TEST_PLAN_FAILURE_RATE).2f</td>
            </tr>\n
"""