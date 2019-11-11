# coding=utf-8

from src.newselenium.by import By


class 主页:
    购票 = (By.CSS_SELECTOR, ".k2")


class 购票页:
    出发地 = (By.CSS_SELECTOR, "#fromStationText")
    目的地 = (By.CSS_SELECTOR, "#toStationText")
    出发日 = (By.CSS_SELECTOR, "#train_date")
    返程日 = (By.CSS_SELECTOR, "#back_train_date")
    普通 = (By.CSS_SELECTOR, "#sf1")
    学生 = (By.CSS_SELECTOR, "#sf2")
    查询 = (By.CSS_SELECTOR, "#a_search_ticket")
