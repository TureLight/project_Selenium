# coding=utf-8

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import *
import traceback
import time

from src.config.config import Config
from src.log.log import Log
from src.newselenium.keys import Keys

# 记录日志
logger = Log()


class Element(object):
    """
    说明：
        重写selenium的element
        self.element 为selenium的原生WebElement类对象
    """

    def __init__(self, driver, eleobject):
        self.driver = driver              # 浏览器 <class 'WebDriver'>
        self.element = eleobject          # 元素 <class 'WebElement'>
        self._parent = eleobject._parent  # 浏览器 <class 'WebDriver'> parent赋予重写后的Element
        self._id = eleobject._id          # id赋予重写后的Element
        self._w3c = eleobject._w3c        # w3c赋予重写后的Element
        # 切换为selenium的WebElement
        self.webelement = WebElement(parent=self._parent, id_=self._id, w3c=self._w3c)

    def clear(self):
        """
        说明：
            清空输入框内容
        """
        self.element.clear()

    def click(self):
        """
        说明：
            元素触发点击事件
        """
        try:
            self.element.click()
        except ElementNotVisibleException:
            self.focus()
            self.js_click()
        except Exception:
            # 处理可能出现的元素不在界面显示，无法点击的问题，将使用滚动条切换到可显示指定元素的位置，然后再做一次点击操作
            if "is not clickable at point" in traceback.format_exc():  # 控件被其他控件遮挡
                self.focus()
                self.element.click()
            else:
                raise

    def rightClick(self):
        """
        说明：
            右键点击
        """
        ActionChains(self.driver).context_click(
            on_element=self.element
        ).perform()

    def click_and_hold(self):
        """
        说明：
            左键点击不释放
        """
        ActionChains(self.driver).click_and_hold(
            on_element=self.element
        ).perform()

    def double_click(self):
        """
        说明：
            左键双击
        """
        ActionChains(self.driver).double_click(
            on_element=self.element
        ).perform()

    def drag_and_drop(self, target):
        """
        说明：
            将元素拖动并释放到元素target处
        :param target: 目标元素
        示例：
            element.drag_and_drop(target)
        注意：
            在拖拽元素时，即使匹配source元素的规则的在拖拽过程中发生变化，也可以完成拖拽
        """
        if isinstance(target, Element):
            ActionChains(self.driver).drag_and_drop(
                source=self.changeToWebElement(), target=target.changeToWebElement()
            ).perform()
        else:
            ActionChains(self.driver).drag_and_drop(
                source=self.changeToWebElement(), target=target
            ).perform()

    def drag_and_drop_by_offset(self, xoffset: int, yoffset: int):
        """
        说明：
            将元素拖动到相对自身x, y坐标位置并释放
        :param xoffset: x方向像素值
        :param yoffset: y方向像素值
        示例：
            element.drag_and_drop_by_offset(500, 0)
        注意：
            在拖拽元素时，即使匹配source元素的规则的在拖拽过程中发生变化，也可以完成拖拽
        """
        ActionChains(self.driver).drag_and_drop_by_offset(
            source=self.changeToWebElement(), xoffset=xoffset, yoffset=yoffset
        ).perform()

    def key_down(self, value: Keys):
        """
        说明：
            一般用来模拟键盘按下
        :param value: he modifier key to send. Values are defined in `Keys` class.
        """
        ActionChains(self.driver).key_down(
            value=value, element=self.element
        ).perform()

    def key_up(self, value: Keys):
        """
        说明：
            一般用来模拟键盘释放
        :param value: he modifier key to send. Values are defined in `Keys` class.
        """
        ActionChains(self.driver).key_up(
            value=value, element=self.element
        ).perform()

    def release(self):
        """
        Releasing a held mouse button on an element.
        """
        ActionChains(self.driver).release(on_element=self.element).perform()

    def get_attribute(self, name):
        """
        说明：
            根据属性名获取元素的属性值
        :param name: 属性名 type = <class str>
        :return: 属性值 type = <class str>
        """
        return self.element.get_attribute(name=name)

    def get_property(self, name):
        """
        说明：
            根据属性名获取元素的属性值
        :param name: 属性名 type = <class str>
        :return: 属性值 type = <class str>
                """
        return self.element.get_property(name=name)

    def is_displayed(self):
        """
        Whether the element is visible to a user.
        """
        return self.element.is_displayed()

    def is_enabled(self):
        """
        Returns whether the element is enabled.
        """
        return self.element.is_enabled()

    def is_selected(self):
        """
        Returns whether the element is selected.
        Can be used to check if a checkbox or radio button is selected.
        """
        return self.element.is_selected()

    def screenshot(self):
        """
        Saves a screenshot of the current element to a PNG image file. Returns
        False if there is any IOError, else returns True. Use full paths in your filename.
        Args:	
        filename: The full path you wish to save your screenshot to. This should end with a .png extension.
        Usage:	
        element.screenshot(‘/Screenshots/foo.png’)
        """
        time_now = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        path = Config.projectDir + "\\Log\\" + time_now + ".png"
        return self.element.screenshot(filename=path)

    def send_keys(self, *value, clear=False):
        """
        说明：
            输入文字或文件，参数与原接口一致 WebElement.send_keys(self, *value)
        :param clear:  输入前是否清除控件，默认不清楚 <class bool>
        """
        if clear:
            self.element.clear()
            self.element.send_keys(*value)
        else:
            self.element.send_keys(*value)

    def submit(self):
        """
        Submits a form.
        """
        self.element.submit()

    def value_of_css_property(self, property_name: str):
        """
        The value of a CSS property.
        :param property_name:  属性名 type = <class str>
        """
        self.element.value_of_css_property(property_name=property_name)

    @property
    def id(self):
        return self.element.id

    @property
    def text(self):
        # return self.webelement.text
        return self.element.text

    @property
    def location(self):
        return self.element.location

    @property
    def location_once_scrolled_into_view(self):
        return self.element.location_once_scrolled_into_view

    @property
    def parent(self):
        """ 
        :return: 返回该元素所在的webdriver 
        """
        return self.element.parent

    @property
    def rect(self):
        return self.element.rect

    @property
    def size(self):
        return self.element.size

    @property
    def tag_name(self):
        return self.element.tag_name

    @property
    def location(self):
        """
        说明：
            返回元素坐标
        :return: {'y': 1742, 'x': 571}
        """
        return self.element.location

    def __eq__(self, element):  # 等号右边对象
        return hasattr(element, "id") and self._id == element.id

    def __str__(self):
        return '<{0.__module__}.{0.__name__} (text="{1}", session="{2}", element="{3}")>'.format(
            type(self), self.text, self._parent.session_id, self._id)

    # --------------以下为新命名的方法-----------------

    # 切换为selenium的WebElement
    def changeToWebElement(self):
        """
        说明：
            返回原生webelement
        :return: 
        """
        # return self.webelement
        return self.element

    def keyboard(self, key: Keys):
        """
        说明：
            支持的键盘按键，请查看class Keys。
        :param keys: 键盘操作按键 
        """
        self.element.send_keys(key)

    def select(self, text=""):
        """
        说明：
            根据下拉框的选项文本进行选择
        :param text: 下拉框选项文本
        """
        try:
            Select(self.element).select_by_visible_text(text=text)
        except UnexpectedTagNameException:
            logger.error(
                "给定的元素不是下拉框(select)元素，而是(%s)，请给定select元素对象。\n%s"
                % (self.tag_name, traceback.format_exc())
            )
            raise UnexpectedTagNameException

    def js_send_keys(self, value: str):
        """
        说明：
            设置元素的value值
        注意：
            和WebElement.send_keys不同的是，元素调用该方法时会先清空再键入赋值
        :param value: 需要键入的内容 type=<class str>
        """
        self.driver.execute_script(
            "arguments[0].value='{}';".format(value), self.element
        )

    def js_click(self):
        self.driver.execute_script(
            "arguments[0].click()", self.element
        )

    def focus(self):
        """
        说明：
            滚动滚动条到该元素
        """
        self.driver.execute_script("arguments[0].scrollIntoView();", self.element)

    def copy(self):
        """
        说明：
            复制
        """
        # ActionChains(self.driver).key_down(value=Keys.CONTROL, element=self.element) \
        #                          .send_keys('c') \
        #                          .key_up(value=Keys.CONTROL, element=self.element) \
        #                          .perform()
        self.element.send_keys(Keys.CONTROL, 'c')

    def paste(self):
        """
        说明：
            粘贴
        """
        # ActionChains(self.driver).key_down(value=Keys.CONTROL, element=self.element) \
        #                          .send_keys('v') \
        #                          .key_up(value=Keys.CONTROL, element=self.element) \
        #                          .perform()
        self.element.send_keys(Keys.CONTROL, 'v')

    def cut(self):
        """
        说明：
            剪切
        """
        self.element.send_keys(Keys.CONTROL, 'x')

    def selectAll(self):
        """
        说明：
            全选
        """
        self.element.send_keys(Keys.CONTROL, 'a')

    def move_to_me(self):
        """
        说明：
            鼠标移动到元素中间
        """
        ActionChains(self.driver).move_to_element(
            to_element=self.element
        ).perform()

    def move_to_me_with_offset(self, xoffset: int, yoffset: int):
        """
        Move the mouse by an offset of the specified element.
           Offsets are relative to the top-left corner of the element.

        :Args:
         - xoffset: X offset to move to.
         - yoffset: Y offset to move to.
        """
        ActionChains(self.driver).move_to_element_with_offset(
            to_element=self.element, xoffset=xoffset, yoffset=yoffset
        ).perform()

    def remove_attribute(self, name):
        """
        说明：
            删除元素指定属性
        :param name: 属性名
        :return: None
        """
        self.driver.execute_script(
            "arguments[0].removeAttribute('%s');" % name, self.element
        )