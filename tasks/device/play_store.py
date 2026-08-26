"""Real uiautomator2 implementations for Play Store interactions."""
from __future__ import annotations
from time import time

from tasks.device.home import open_app


def download_app(device, app_name: str) -> None:
    open_app(device, "Play Store")
    device(text="Search").click()
    device(resourceId="com.android.vending:id/search_box_text_input").set_text(app_name)
    device.press("enter")
    device(text=app_name).click()
    device(text="Install").click()


def sign_in(device) -> None:
    sl = device(text="Sign in")
    sl.click_exists(timeout=10)
    sl = device(text="SKIP")
    sl.click_exists(timeout=10)
    device.click(0.275, 0.341)
    device.send_keys("34156g@gmail.com")
    time.sleep(5)  # Wait for the email input to be processed
    s1 = device(text="Next")
    s1.click_exists(timeout=10)
    device.click(0.275, 0.341)
    device.send_keys("superdoter")
    time.sleep(5)  # Wait for the password input to be processed
    s3 = device(text="Next")
    s3.click_exists(timeout=10)
    s3 = device(text="TRY ANOTHER WAY")
    s3.click_exists(timeout=10)