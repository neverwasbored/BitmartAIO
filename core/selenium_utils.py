from selenium import webdriver


def close_all_windows(driver: webdriver):
    for handle in driver.window_handles:
        if len(driver.window_handles) == 1:
            return True
        driver.switch_to.window(handle)
        driver.close()
    return False
