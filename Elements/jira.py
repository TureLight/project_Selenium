# coding=utf-8

from src.newselenium.by import By


class JIRA:
    div_mainLogin_loc = (By.CSS_SELECTOR, "#main_login")
    登录框 = (By.CSS_SELECTOR, "#main_login")
    input_username_loc = (By.CSS_SELECTOR, "#username")
    登录用户名输入框 = (By.CSS_SELECTOR, "#username")
    input_password_loc = (By.CSS_SELECTOR, "#password")
    登录密码输入框 = (By.CSS_SELECTOR, "#password")
    input_btnSubmit_loc = (By.CSS_SELECTOR, ".btn-submit")
    登录确定按钮 = (By.CSS_SELECTOR, ".btn-submit")
    # a_zhangzheng_loc = (By.CSS_SELECTOR, "#user_nav_bar_zhangzheng172399")
    a_XinJian_loc = (By.CSS_SELECTOR, "#create_link")  # 新建按钮
    新建按钮 = (By.CSS_SELECTOR, "#create_link")  # 新建按钮
    input_GaiYao_loc = (By.CSS_SELECTOR, "#summary")  # 概要输入框
    概要输入框 = (By.CSS_SELECTOR, "#summary")  # 概要输入框
    input_YouXianJi_loc = (By.CSS_SELECTOR, "#priority-field")  # 优先级输入框
    优先级输入框 = (By.CSS_SELECTOR, "#priority-field")  # 优先级输入框
    select_QueXianLiaYuan_loc = (By.CSS_SELECTOR, "#customfield_10072")  # 缺陷来源下拉框
    缺陷来源下拉框 = (By.CSS_SELECTOR, "#customfield_10072")  # 缺陷来源下拉框
    select_QueXianLiaYuan2_loc = (
        By.CSS_SELECTOR,
        "#customfield_10072\:1",
    )  # 缺陷来源第二个下拉框
    缺陷来源第二个下拉框 = (By.CSS_SELECTOR, "#customfield_10072\:1")  # 缺陷来源第二个下拉框
    textarea_MoKuai_loc = (By.CSS_SELECTOR, "#components-textarea")  # 模块多行输入框
    模块多行输入框 = (By.CSS_SELECTOR, "#components-textarea")  # 模块多行输入框
    select_DanYuanCeShi_loc = (By.CSS_SELECTOR, "#customfield_10160")  # 单元测试发现
    单元测试发现 = (By.CSS_SELECTOR, "#customfield_10160")  # 单元测试发现
    input_JingBanRen_loc = (By.CSS_SELECTOR, "#assignee-field")  # 经办人输入框
    经办人输入框 = (By.CSS_SELECTOR, "#assignee-field")  # 经办人输入框
    textare_HuanJing_loc = (By.CSS_SELECTOR, "#environment")  # 环境多行输入框
    环境多行输入框 = (By.CSS_SELECTOR, "#environment")  # 环境多行输入框
    textarea_MiaoShu_loc = (By.CSS_SELECTOR, "#description")  # 描述多行输入框
    描述多行输入框 = (By.CSS_SELECTOR, "#description")  # 描述多行输入框
    input_WenJian_loc = (
        By.CSS_SELECTOR,
        "#create-issue-dialog .issue-drop-zone__file",
    )  # 上传文件
    上传文件 = (By.CSS_SELECTOR, "#create-issue-dialog .issue-drop-zone__file")  # 上传文件
    input_BaoGaoRen_loc = (By.CSS_SELECTOR, "#reporter-field")  # 报告人输入框
    报告人输入框 = (By.CSS_SELECTOR, "#reporter-field")  # 报告人输入框
    input_BaoGaoRiQi_loc = (By.CSS_SELECTOR, "#customfield_10001")  # 报告日期输入框
    报告日期输入框 = (By.CSS_SELECTOR, "#customfield_10001")  # 报告日期输入框
    input_XiuGaiDanHao_loc = (By.CSS_SELECTOR, "#customfield_10110")  # 修改单号输入框
    修改单号输入框 = (By.CSS_SELECTOR, "#customfield_10110")  # 修改单号输入框
    select_QueXianFaXianJieDuan_loc = (
        By.CSS_SELECTOR,
        "#customfield_10290",
    )  # 缺陷发现阶段选择框
    缺陷发现阶段选择框 = (By.CSS_SELECTOR, "#customfield_10290")  # 缺陷发现阶段选择框
    select_LeiBie_loc = (By.CSS_SELECTOR, "#customfield_10000")  # 类别选择框
    类别选择框 = (By.CSS_SELECTOR, "#customfield_10000")  # 类别选择框
    input_DaHuiCiShu_loc = (By.CSS_SELECTOR, "#customfield_10002")  # 打回次数输入框
    打回次数输入框 = (By.CSS_SELECTOR, "#customfield_10002")  # 打回次数输入框
    select_CeShiFangFa_loc = (By.CSS_SELECTOR, "#customfield_10510")  # 测试方法选择框
    测试方法选择框 = (By.CSS_SELECTOR, "#customfield_10510")  # 测试方法选择框

    # https://se.hundsun.com/dm/secure/Dashboard.jspa;jsessionid=B4409BCDECF07144A2DAF48EB6813067
    a_zhangzheng_loc = (By.CSS_SELECTOR, ".aui-page-header-main>h1111")
