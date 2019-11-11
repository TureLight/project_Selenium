# coding=utf-8

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
import traceback
import time
import os

from src.config.config import Config
from src.log.log import Log
from src.newselenium.by import By
from src.newselenium.keys import Keys
from src.newselenium.element import Element
from src.exception.seleniumexecption import SeleniumTypeError, SeleniumTimeoutError
from src.public.regedit import Regedit


# 记录日志
logger = Log()


class Driver(object):
    """
    说明：
        重写selenium的webdriver
        self.driver 为selenium的原生webdriver类对象
    """

    def __init__(self, url=None, browsertype="", browserdriver=None):
        """
        说明：
            实例化出driver对象
        :param url: 访问地址
        :param browsertype: 浏览器类型 firefox \ chrome
        """
        self.__driver = browserdriver  # 浏览器 <class 'WebDriver'>
        self.url = url
        self.browsertype = browsertype
        if not self.__driver:  # 如果未指定浏览器对象，则自动打开浏览器
            self.__initOpenBrowser()
        elif isinstance(self.__driver, (Driver, )):
            raise SeleniumTypeError("参数WebDriver类型不对，不能为newselenium.Driver类")
        elif isinstance(self.__driver, (WebDriver, )):
            logger.info("将selenium.WebDriver类转化为newselenium.Driver类")

    @classmethod
    def webdriverToDriver(cls, webdriver: WebDriver):
        """
        说明：
            类方法
            将webDriver实例转化为Driver实例
        示例：

            from selenium import webdriver
            from src.newselenium.driver import Driver

            driver = webdriver.Chrome()
            driver.get(url=r"https://www.baidu.com/")
            newdriver = Driver.webdriverToDriver(webdriver=driver)
            newdriver.close()

            ...

        :param webdriver: webDriver实例  <class 'selenium.webdriver.remote.webdriver.WebDriver'>
        :return: Driver实例  <class 'Driver'>
        """
        return Driver(url=webdriver.current_url, browsertype="fromWebDriver", browserdriver=webdriver)

    def __getOption(self, browser):
        if Config.headLess:
            if str.lower(browser) == "chrome":
                option = webdriver.ChromeOptions()
                option.set_headless(headless=True)
                return option
            if str.lower(browser) == "firefox":
                option = webdriver.FirefoxOptions()
                option.set_headless(headless=True)
                return option
        else:
            return None

    def __initOpenBrowser(self):
        driverspath = os.path.join(Config.projectDir, "Drivers")
        try:
            browser = str.strip(self.browsertype)
            if not browser:  # 如果没有指定浏览器类型，读取配置中设置的浏览器类型
                browser = str.strip(Config.browserType)
            if str.lower(browser) == "chrome":  # 谷歌浏览器
                driver_remote = os.path.join(driverspath, "chromedriver.exe")
                self.__driver = webdriver.Chrome(
                    executable_path=driver_remote,
                    options=self.__getOption(browser=browser),
                )
                logger.info("当前谷歌浏览器版本为%s" % self.__driver.capabilities["version"])
                # 静态超时时间
                # 2018-6-10 改为根据浏览器类型区分，火狐浏览器对这一方法兼容性较差，可能会导致报错
                self.__driver.implicitly_wait(Config.timeOut)
            elif str.lower(browser) == "firefox":  # 火狐浏览器
                driver_remote = os.path.join(driverspath, "geckodriver.exe")
                self.__driver = webdriver.Firefox(
                    executable_path=driver_remote,
                    options=self.__getOption(browser=browser),
                )
                logger.info(
                    "当前使用的是火狐浏览器，初始化时未指定静态超时时间，可以通过driver.implicitly_wait() 方法设置"
                )
                logger.info("当前火狐浏览器版本为%s" % self.__driver.capabilities["version"])
            elif str.lower(browser) == "phantomjs":  # 无头浏览器
                driver_remote = os.path.join(driverspath, "phantomjs.exe")
                self.__driver = webdriver.PhantomJS(
                    executable_path=driver_remote,
                )
                logger.info(
                    "当前使用的是phantomjs浏览器"
                )
                logger.info("当前phantomjs浏览器版本为%s" % self.__driver.capabilities["version"])
            elif str.lower(browser) == "360":  # 360浏览器
                driver_remote = os.path.join(driverspath, "chromedriver.exe")
                chrome_options = Options()
                browser_path_360 = Config.browserPath360
                if browser_path_360 is None:  # 如果未配置则从注册表中获取
                    browser_path_360 = Regedit.get_value(path=r"HKEY_CLASSES_ROOT\360SeSES\DefaultIcon", name="(默认)").split(",")[0]
                chrome_options.binary_location = browser_path_360
                self.__driver = webdriver.Chrome(chrome_options=chrome_options,
                                                 executable_path=driver_remote)
                logger.info("当前360浏览器Chrome内核版本为%s" % self.__driver.capabilities["version"])
                # 静态超时时间
                self.__driver.implicitly_wait(Config.timeOut)
            else:
                raise SeleniumTypeError("未找到指定的浏览器及其对应的驱动...")
            # 打开网页
            self.__driver.get(url=self.url)
        except Exception as e:
            logger.error("使用驱动打开浏览器错误，可能是驱动版本与浏览器版本不匹配。报错信息:\n" + traceback.format_exc())

    # --------------以下为重写的方法,方法名和源码一致，某些调用更方便,功能更强大-----------------

    def move_to_element(self, to_element: Element):
        """
        说明：
            鼠标移动到指定元素上
        :param to_element: 需要移动到的元素 type = <class Element>
        """
        ActionChains(self.__driver).move_to_element(
            to_element=to_element.changeToWebElement()
        ).perform()

    def move_to_element_with_offset(self, to_element: Element, xoffset: int, yoffset: int):
        """
        Move the mouse by an offset of the specified element.
           Offsets are relative to the top-left corner of the element.

        :Args:
         - to_element: The WebElement to move to.
         - xoffset: X offset to move to.
         - yoffset: Y offset to move to.
        """
        ActionChains(self.__driver).move_to_element_with_offset(
            to_element=to_element.changeToWebElement(),
            xoffset=xoffset,
            yoffset=yoffset
        ).perform()

    def pause(self, seconds):
        """ Pause all inputs for the specified duration in seconds """
        ActionChains(self.__driver).pause(seconds=seconds).perform()

    def release(self, on_element: Element):
        """
        Releasing a held mouse button on an element.

        :Args:
         - on_element: The element to mouse up.
           If None, releases on current mouse position.
        """
        ActionChains(self.__driver).release(
            on_element=on_element.changeToWebElement()
        ).perform()

    def drag_and_drop(self, source: Element, target: Element):
        """
        说明：
            将元素source拖动并释放到元素target处
        :param source: 需要移动的元素
        :param target: 目标元素
        示例：
            driver.drag_and_drop(source, target)
        注意：
            在拖拽元素时，即使匹配source元素的规则的在拖拽过程中发生变化，也可以完成拖拽
        """
        ActionChains(self.__driver).drag_and_drop(
            source=source.changeToWebElement(), target=target.changeToWebElement()
        ).perform()
        # ActionChains(self.__driver).click_and_hold(source).move_to_element(target).release().perform()

    def drag_and_drop_by_offset(self, source: Element, xoffset: int, yoffset: int):
        """
        说明：
            将元素source拖动到相对自身x, y坐标位置并释放
        :param source: 需要移动的元素
        :param xoffset: x方向像素值
        :param yoffset: y方向像素值
        示例：
            driver.drag_and_drop_by_offset(source, 500, 0)
        注意：
            在拖拽元素时，即使匹配source元素的规则的在拖拽过程中发生变化，也可以完成拖拽
        """
        ActionChains(self.__driver).drag_and_drop_by_offset(
            source=source.changeToWebElement(), xoffset=xoffset, yoffset=yoffset
        ).perform()

    def click_and_hold(self, on_element: Element):
        """
        Holds down the left mouse button on an element.

        :Args:
         - on_element: The element to mouse down.
           If None, clicks on current mouse position.
        """
        ActionChains(self.__driver).click_and_hold(
            on_element=on_element.changeToWebElement()
        ).perform()

    def key_down(self, value: Keys, element: Element):
        """
        Sends a key press only, without releasing it.
           Should only be used with modifier keys (Control, Alt and Shift).

        :Args:
         - value: The modifier key to send. Values are defined in `Keys` class.
         - element: The element to send keys.
           If None, sends a key to current focused element.

        Example, pressing ctrl+c::

            ActionChains(driver).key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()

        """
        ActionChains(self.__driver).key_down(
            value=value, element=element.changeToWebElement()
        ).perform()

    def key_up(self, value: Keys, element: Element):
        """
        Releases a modifier key.

        :Args:
         - value: The modifier key to send. Values are defined in Keys class.
         - element: The element to send keys.
           If None, sends a key to current focused element.

        Example, pressing ctrl+c::

            ActionChains(driver).key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()

        """
        ActionChains(self.__driver).key_up(
            value=value, element=element.changeToWebElement()
        ).perform()

    def send_keys(self, *keys_to_send):
        """
        Sends keys to current focused element.

        :Args:
         - keys_to_send: The keys to send.  Modifier keys constants can be found in the
           'Keys' class.
        """
        ActionChains(self.__driver).send_keys(*keys_to_send).perform()

    def send_keys_to_element(self, element: Element, *keys_to_send):
        """
        Sends keys to an element.

        :Args:
         - element: The element to send keys.
         - keys_to_send: The keys to send.  Modifier keys constants can be found in the
           'Keys' class.
        """
        ActionChains(self.__driver).send_keys_to_element(
            element=element.changeToWebElement(),
            *keys_to_send
        ).perform()

    def move_by_offset(self, xoffset: int, yoffset: int):
        """
        Moving the mouse to an offset from current mouse position.

        :Args:
         - xoffset: X offset to move to, as a positive or negative integer.
         - yoffset: Y offset to move to, as a positive or negative integer.
        """
        ActionChains(self.__driver).move_by_offset(
            xoffset=xoffset, yoffset=yoffset
        ).perform()

    def switch_to_frame(self, frame_reference: (int, str, Element)):
        """
        说明：
            切换iframe/frame窗口
            可以根据iframe/frame标签的id、name属性，也可以通过getelement()返回的Element对象切换进去
            如果没有找到则会切换到最上层Top Window
        :param frame_reference: 
        """
        if isinstance(frame_reference, (int, str)):
            self.__driver.switch_to.frame(frame_reference=frame_reference)
        elif isinstance(frame_reference, Element):
            self.__driver.switch_to.frame(
                frame_reference=frame_reference.changeToWebElement()
            )
        else:
            self.__driver.switch_to.default_content()  # 切换到最上层页面

    def switch_to_default_content(self):
        """
        说明：
            切换到最上层页面 Top Window
        """
        self.__driver.switch_to.default_content()

    def switch_to_window(self, window_name: str):
        """
        说明：
            切换窗口句柄(标签页)
        :param window_name: 
            1.可以使用Driver.window_handles 返回的句柄进行切换
        示例:
            1. driver.switch_to_window(driver.window_handles[0])
        """
        self.__driver.switch_to.window(window_name=window_name)

    def switch_to_alert(self):
        """
        说明：
            Switches focus to an alert on the page.
            将焦点切换到页面的提示框上(alert)，可以使用返回的alert对象操作提示框
        :return: 提示框alert对象 type = <class Alert >
        """
        return self.__driver.switch_to.alert

    def execute_script(self, script: str, *args):
        """
        说明：
            执行 js 命令
        :param script: js 脚本 type = <class str>
        :param args: 可以是Element对象
        示例：
            driver.execute_script("arguments[0].scrollIntoView();", Element)
            driver.execute_script("return arguments[0].scrollHeight;", Element)
            driver.execute_script("return arguments[0][arguments[1]]", su, "value")
        """
        # 如果参数里面有Element的实例化对象，需要将其转化为selenium.webdriver.remote.webelement.WebElement对象
        if args:
            args = (arg.element if isinstance(arg, Element) else arg for arg in args)
        return self.__driver.execute_script(script, *args)

    def get(self, url: str):
        """
        说明：
            在当前窗口请求地址url
        """
        self.__driver.get(url=url)

    def back(self):
        """
        说明：
            在浏览器历史中向后退一步
        """
        self.__driver.back()

    def forward(self):
        """
        说明：
            在浏览器历史上前进一步
        """
        self.__driver.forward()

    def close(self):
        """
        说明：
            关闭当前窗口
        """
        self.__driver.close()

    def quit(self):
        """
        说明：
            关闭所有窗口并退出浏览器
        """
        self.__driver.quit()

    def maximize_window(self):
        """
        说明：
            最大化浏览器窗口
        """
        self.__driver.maximize_window()

    def minimize_window(self):
        """
        说明：
            最小化浏览器窗口
        """
        self.__driver.minimize_window()

    def refresh(self):
        """
        说明：
            刷新当前页面
        """
        self.__driver.refresh()

    def get_window_position(self):
        """
        说明：
            返回当前浏览器的 x,y 坐标
        :return: {'y': 10, 'x': 10} type = <class dict>
        """
        return self.__driver.get_window_position()

    def get_window_rect(self):
        """
        说明：
            返回当前浏览器的位置
        :return:
        """
        return self.__driver.get_window_rect()

    def get_window_size(self):
        """
        说明：
            返回当前浏览器的位置
        :return: {'width': 945, 'height': 1030} type = <class dict>
        """
        return self.__driver.get_window_size()

    def set_window_position(self, x: int, y: int, windowHandle="current"):
        """
        说明：
            设置浏览器的位置
        :param x: 
        :param y: 
        :param windowHandle: 
        """
        self.__driver.set_window_position(x=x, y=y, windowHandle=windowHandle)

    def set_window_rect(self, x=None, y=None, width=None, height=None):
        """
        说明：
            设置浏览器的位置与大小
        :param x: 
        :param y: 
        :param width: 
        :param height: 
        """
        self.__driver.set_window_rect(x=x, y=y, width=width, height=height)

    def set_window_size(self, width: int, height: int, windowHandle="current"):
        """
        说明：
            设置浏览器的大小
        :param width: 
        :param height: 
        :param windowHandle: 
        """
        self.__driver.set_window_size(
            width=width, height=height, windowHandle=windowHandle
        )

    def implicitly_wait(self, time_to_wait: int) -> None:
        self.__driver.implicitly_wait(time_to_wait=time_to_wait)

    def get_cookies(self):
        """
        说明：
            获得所有 cookie 信息
        :return: 所有cookie信息
        """
        return self.__driver.get_cookies()

    def get_cookie(self, name: str):
        """
        说明：
            返回有特定 name 值有 cookie 信息
        :param name:
        :return: 指定cookie值
        """
        return self.__driver.get_cookie(name=name)

    def add_cookie(self, cookie_dict: dict):
        """
        说明：
            添加 cookie
        :param cookie_dict: 字典对象, 必填参数 - "name" and "value";
                                     可选参数 - "path", "domain", "secure", "expiry"
        :return: None
        示例：
            driver.add_cookie({'name' : 'foo', 'value' : 'bar'})
            driver.add_cookie({'name' : 'foo', 'value' : 'bar', 'path' : '/'})
            driver.add_cookie({'name' : 'foo', 'value' : 'bar', 'path' : '/', 'secure':True})
        """
        self.__driver.add_cookie(cookie_dict=cookie_dict)

    def delete_cookie(self, name: str):
        """
        说明：
            删除指定 cookie
        :param name:
        :return: None
        """
        self.__driver.delete_cookie(name=name)

    def delete_all_cookies(self):
        """
        说明：
            删除所有 cookie信息
        :return: None
        """
        self.__driver.delete_all_cookies()

    @property
    def window_handles(self):
        """
        说明：
            返回当前浏览器的窗口句柄
        :return: <type list>
        """
        return self.__driver.window_handles

    @property
    def current_window_handle(self):
        """
        说明：
            返回当前窗口句柄
        :return: type = <class str>
        """
        return self.__driver.current_window_handle

    @property
    def current_url(self):
        """
        说明：
            返回当前窗口请求的url地址
        :return: type = <class str>
        """
        return self.__driver.current_url

    @property
    def title(self):
        """
        说明：
            返回当前窗口的标题
        :return: type = <class str>
        """
        return self.__driver.title

    @property
    def name(self):
        return self.__driver.name

    @property
    def page_source(self):
        return self.__driver.page_source

    # --------------以下为新命名的方法-----------------

    def getelement(self, by=By.ID, value=None):
        """
        说明：
            定位并返回元素
        :param by: By.ID By.XPATH By.LINK_TEXT By.PARTIAL_LINK By.NAME By.TAG_NAME By.CLASS_NAME By.CSS_SELECTOR type = <class By>
        :param value: 匹配规则 type = <class str>
        :return: type = <class Element>
        示例：
            element = driver.getelement(By.ID, "id_name")
        """
        # return Element(self.__driver, self.__driver.find_element(by=by, value=value))
        return DriverWait(driver=self.__driver, timeout=Config.timeOut).\
            presence_of_element_located(by=by, value=value)

    def getelements(self, by=By.ID, value=None):
        """
        说明：
            定位并返回元素
        :param by: By.ID By.XPATH By.LINK_TEXT By.PARTIAL_LINK By.NAME By.TAG_NAME By.CLASS_NAME By.CSS_SELECTOR type = <class By>
        :param value: 匹配规则 type = <class str>
        :return: type = <class list>
        示例：
            elements = driver.getelements(By.ID, "id_name")
        """
        # elements = self.__driver.find_elements(by=by, value=value)  # 如果没找到返回空列表
        elements = DriverWait(driver=self.__driver, timeout=Config.timeOut).\
            presence_of_all_elements_located(by=by, value=value)
        return list(map(lambda ele: Element(self.__driver, ele), elements))

    def doubleClick(self, element: Element):
        """
        说明：
            鼠标双击指定的element
        :param element: element type = <class Element>
        """
        ActionChains(self.__driver).double_click(element.changeToWebElement()).perform()

    def leftClick(self, element: Element):
        """
        说明：
            鼠标左击指定的element
        :param element: element type = <class Element>
        """
        ActionChains(self.__driver).click(element.changeToWebElement()).perform()

    def rightClick(self, element: Element):
        """
        说明：
            鼠标右击指定的element
        :param element: element type = <class Element>
        """
        ActionChains(self.__driver).context_click(element.changeToWebElement()).perform()

    def switch_to_window_byTagName(self, tag_name: str):
        """
        说明：
            切换窗口句柄(标签页)
        :param tag_name: 
            1.可以使用窗口的标签页名称进行切换
        示例:
            1. driver.switch_to_window_byTagName("百度一下，你就知道")
        """
        time_out = 10
        clock = 0
        while clock < 10:
            for handle in self.__driver.window_handles:
                self.__driver.switch_to.window(handle)
                if self.__driver.title == tag_name:
                    print(self.__driver.title)
                    return
            time.sleep(1)
            clock += 1
        raise SeleniumTimeoutError("未找到您提供“{}”的标签名".format(tag_name))

    def operateAlert(self, mode="ACCEPT"):
        """
        说明：
            操作当前窗口的alert提示框，也支持confirm、prompt对话框
        :param mode: 
            1. "ACCEPT" 点击提示框确认按钮
            2. "DISMISS" 点击提示框右上角的“x”
            3. "TEXT" 返回提示框的文字信息
        :return: 如果mode="TEXT"将返回提示框的内容
        """
        alert = self.__driver.switch_to.alert
        if mode.upper() == "ACCEPT":
            alert.accept()
        elif mode.upper() == "DISMISS":
            alert.dismiss()
        elif mode.upper() == "TEXT":
            return alert.text

    def open_newindow(self):
        """
        说明：
            打开新窗口(标签页)
        """
        self.execute_script("window.open()")

    def get_screenshot(self, path=None):
        """
        说明：
            截图并保存到指定log目录
        :param path: 如果指定目录则存放在指定目录中
        """
        if not path:
            time_now = time.strftime("%Y%m%d-%H%M%S", time.localtime())
            path = Config.projectDir + "\\Log\\" + time_now + ".png"
            self.__driver.get_screenshot_as_file(filename=path)
        else:
            self.__driver.get_screenshot_as_file(filename=path)

    def scrollToBottom(self):
        """
        说明：
            滚动滚动条到底部
        """
        self.__driver.execute_script("window.scrollTo(0, 999999)")

    def scrollToUp(self):
        """
        说明：
            滚动滚动条到顶部
        """
        self.__driver.execute_script("window.scrollTo(0, 0)")

    def scrollToXY(self, x=0, y=0):
        """
        说明：
            滚动到相对于左上角的(x, y)位置
        """
        self.__driver.execute_script("window.scrollTo({}, {})".format(x, y))

    def focusElement(self, element: Element):
        """
        说明：
            视图定位到指定的element上
        :param element: Element对象 <class 'Element'>
        """
        self.execute_script("arguments[0].scrollIntoView();", element)

    def changeToWebDriver(self):
        """
        说明：
            返回原生webdriver对象
        :return: 
        """
        return self.__driver

    def waitUntil(self, timeout=10):
        """
        说明：
            明确等待
        :param timeout: 超时时间
        :return: type=WebDriverWait
        """
        return DriverWait(driver=self.__driver, timeout=timeout)

    @property
    def driver(self) -> WebDriver:
        return self.__driver


class DriverWait(object):
    """
        self.__driver 为selenium的原生webdriver类对象 <class WebDirver>
    """
    def __init__(self, driver: Driver, timeout: int, poll_frequency=0.5, ignored_exceptions=None):
        self.__driver = driver  # <class WebDirver>
        self.__timeout = timeout
        self.__poll_frequency = poll_frequency
        self.__ignored_exceptions = ignored_exceptions
        self._WebDriverWait = WebDriverWait(driver=self.__driver,
                                            timeout=self.__timeout,
                                            poll_frequency=self.__poll_frequency,
                                            ignored_exceptions=self.__ignored_exceptions)

    def presence_of_element_located(self, by=By.ID, value="") -> Element:
        """
        说明：
            等待直到定位到元素
        :param by: 定位方式 <class By>
        :param value: 值 <class str>
        :return: 返回被定位的元素 <class Element>
        """
        element = self._WebDriverWait.until(
            EC.presence_of_element_located(locator=(by, value))
        )
        return Element(driver=self.__driver, eleobject=element)

    def title_is(self, title: str) -> bool:
        """
        说明：
            等待直到匹配到指定浏览器的title
        :param title: title <class str>
        :return: returns True if the title matches, false otherwise <class bool>
        """
        return self._WebDriverWait.until(
                    EC.title_is(title=title)
                )

    def title_contains(self, title: str) -> bool:
        """
        说明：
            等待直到匹配到指定浏览器的title中包含某些字符串
        :param title: title <class str>
        :return: returns True when the title matches, False otherwise <class bool>
        """
        return self._WebDriverWait.until(
                    EC.title_contains(title=title)
               )

    def visibility_of_element_located(self, by=By.ID, value="") -> (Element, bool):
        """
        说明：
            等待直到定位的元素可见
        :param by: 定位方式 <class By>
        :param value: 值 <class str>
        :return: 如果定位到的元素可见则返回该元素 <class Element> 否则引起TimeoutException
        """
        element = self._WebDriverWait.until(
                    EC.visibility_of_element_located(locator=(by, value))
                  )
        return Element(driver=self.__driver, eleobject=element) if element else False

    def visibility_of(self, element: Element) -> (Element, bool):
        """
        说明：
            等待直到指定的元素可见且元素的长和宽大于0
        :param element: 期望检查的指定元素 <class Element>
        :return: 如果该元素存在则返回该元素 <class Element> 否则引起TimeoutException
        """
        element = element.changeToWebElement()
        ele = self._WebDriverWait.until(
               EC.visibility_of(element=element)
              )
        return Element(driver=self.__driver, eleobject=ele) if ele else False

    def presence_of_all_elements_located(self, by=By.ID, value="") -> list:
        """
        说明：
            等待直到定位到元素
        :param by: 定位方式 <class By>
        :param value: 值 <class str>
        :return: 返回 list of Elements
        """
        elements = self._WebDriverWait.until(
                    EC.presence_of_all_elements_located(locator=(by, value))
                  )
        if elements:
            return list(map(lambda ele: Element(driver=self.__driver, eleobject=ele), elements))
        else:
            return elements

    def text_to_be_present_in_element(self, by=By.ID, value="", text="") -> bool:
        """
        说明：
            等待直到找到指定元素(参数:by value)的text属性包含指定的内容(参数:text)
        :param by: 定位方式 <class By>
        :param value: 值 <class str>
        :param text: text属性包含的内容
        :return: 如果存在返回True 否则引起TimeoutException
        """
        return self._WebDriverWait.until(
                    EC.text_to_be_present_in_element(locator=(by, value), text_=text)
               )

    def text_to_be_present_in_element_value(self, by=By.ID, value="", text="") -> bool:
        """
        说明：
            等待直到找到指定元素(参数:by value)的value属性包含指定的内容(参数:text)
        :param by: 定位方式 <class By>
        :param value: 值 <class str>
        :param text: text属性包含的内容
        :return: 如果存在返回True 否则引起TimeoutException
        """
        return self._WebDriverWait.until(
                    EC.text_to_be_present_in_element_value(locator=(by, value), text_=text)
               )

    def frame_to_be_available_and_switch_to_it(self, locator=(By.ID, "value")) -> bool:
        """
        说明：
            等待直到存在指定的frame可以switch_to,然后会switch_to该frame
        :param locator: 可以根据iframe/frame标签的id、name属性 或者(By.ID, "value")来定位
        :return: 如果存在并switch成功会返回True 否则引起TimeoutException
        """
        return self._WebDriverWait.until(
                    EC.frame_to_be_available_and_switch_to_it(locator=locator)
               )

    def invisibility_of_element_located(self, by=By.ID, value="") -> (bool, Element):
        """
        说明：
            等待直到存在指定的元素在当前DOM上不可见或不存在，如果不存在返回True 如果存在但不可见返回该元素element
        :param by: 定位方式 <class By>
        :param value: 值 <class str>
        :return: 如果不存在返回True <class bool> 如果存在但不可见返回该元素element <class Element>，否则引起TimeoutException
        """
        element = self._WebDriverWait.until(
                   EC.invisibility_of_element_located(locator=(by, value))
                  )
        return True if element is True else Element(driver=self.__driver, eleobject=element)

    def element_to_be_clickable(self, by=By.ID, value="") -> Element:
        """
        说明：
            等待直到指定的元素可见并可点击
        :param by: 定位方式 <class By>
        :param value: 值 <class str>
        :return: 如果存在则返回该元素，否则引起TimeoutException
        """
        element = self._WebDriverWait.until(
                   EC.element_to_be_clickable(locator=(by, value))
                  )
        return Element(driver=self.__driver, eleobject=element)

    def staleness_of(self, element: Element) -> bool:
        """ Wait until an element is no longer attached to the DOM.
        element is the element to wait for.
        returns False if the element is still attached to the DOM, true otherwise.
        """
        element = element.changeToWebElement()
        return self._WebDriverWait.until(
                    EC.staleness_of(element=element)
               )

    def element_to_be_selected(self, element: Element) -> bool:
        """ An expectation for checking the selection is selected.
        element is WebElement object
        """
        element = element.changeToWebElement()
        return self._WebDriverWait.until(
                    EC.element_to_be_selected(element=element)
               )

    def element_located_to_be_selected(self, by=By.ID, value="") -> bool:
        """An expectation for the element to be located is selected.
        locator is a tuple of (by, path)"""
        return self._WebDriverWait.until(
                    EC.element_located_to_be_selected(locator=(by, value))
               )

    def element_selection_state_to_be(self, element: Element, is_selected: bool) -> bool:
        """ An expectation for checking if the given element is selected.
        element is WebElement object
        is_selected is a Boolean."
        """
        element = element.changeToWebElement()
        return self._WebDriverWait.until(
                    EC.element_selection_state_to_be(element=element, is_selected=is_selected)
               )

    def element_located_selection_state_to_be(self, by: By, value: str, is_selected: bool) -> bool:
        """ An expectation to locate an element and check if the selection state
        specified is in that state.
        locator is a tuple of (by, path)
        is_selected is a boolean
        """
        return self._WebDriverWait.until(
                    EC.element_located_selection_state_to_be(locator=(by, value), is_selected=is_selected)
               )

    def alert_is_present(self) -> Alert:
        """ Expect an alert to be present."""
        return self._WebDriverWait.until(
                    EC.alert_is_present()
               )
