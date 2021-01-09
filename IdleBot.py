from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import tkinter as tk
import os, sys

browser = None

def login(user, passw, check_browser):
    global browser

    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(__file__)
        return os.path.join(base_path, relative_path)

    chrome_driver = resource_path('./driver/chromedriver.exe')
    if check_browser == 1:
        browser = webdriver.Chrome(chrome_driver)
    elif check_browser == 0:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        browser = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver)

    # Login
    browser.get('https://wfg.xcelsolutions.com')
    username = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="reduxFormInputField1"]')))
    password = browser.find_element_by_xpath('//*[@id="reduxFormInputField3"]')
    username.send_keys(user)
    password.send_keys(passw)
    password.send_keys(Keys.RETURN)

    # Navigate to course directory
    # TODO universal navigation for different courses

    # Check for bad login
    try:
        course_button = WebDriverWait(browser, 10).until\
            (EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[3]/div/div[2]/div/div[2]/div/div/div[2]')))
        course_button.click()
    except:
        raise NameError('Bad Login')

    choose_course = WebDriverWait(browser, 10).until\
        (EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[3]/div/div[2]/div/div[3]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[1]/div/button')))
    choose_course.click()

    # Close dialog box if it exists and open course
    try:
        choose_course_content = WebDriverWait(browser, 10).until\
            (EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[3]/div/div[2]/div/div[4]/div[1]/div[2]/div/div[4]/div[1]/div[2]/div/div/div/div')))
        choose_course_content.click()
    except:
        dialog_box = WebDriverWait(browser, 5).until \
            (EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[2]/button')))
        dialog_box.click()

        choose_course_content = WebDriverWait(browser, 10).until \
            (EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[3]/div/div[2]/div/div[4]/div[1]/div[2]/div/div[4]/div[1]/div[2]/div/div/div/div')))
        choose_course_content.click()

    get_hours()

# Navigates bot to course page, begin idle
def get_hours():
    global after_id
    global after_id2

    # print('Farm start')
    complete_course = WebDriverWait(browser, 10).until\
        (EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[3]/div/div[2]/div/div[4]/div[1]/div[2]/div/div[3]/div[2]/div[2]/div/div[1]/div/div[2]/div/button')))
    complete_course.click()

    # Click past identification check
    frame = WebDriverWait(browser, 10).until \
        (EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/iframe')))
    browser.switch_to.frame(frame)

    identify_button = WebDriverWait(browser, 10).until\
        (EC.element_to_be_clickable((By.XPATH, '//*[@id="identify_student_submit"]')))
    identify_button.click()

    after_id = window.after(596000, save)
    after_id2 = window.after(605000, get_hours)


# Save and exit from course
def save():
    global browser

    save_button = WebDriverWait(browser, 10).until \
        (EC.element_to_be_clickable((By.XPATH, '//*[@id="exitButton"]')))
    save_button.click()
    # print('Farmed 10 minutes')


# Start/Stop web bot after button event
def run():
    global browser
    global btn
    global ent_user
    global ent_pass
    global C2

    global user
    global passw
    global check_browser

    global after_id
    global after_id2

    after_id = None
    after_id2 = None
    user1 = user.get()
    passw1 = passw.get()
    check_browser1 = check_browser.get()

    if btn.get() == 'Run':
        btn.set('Stop')
        ent_user.configure(state='disabled')
        ent_pass.configure(state='disabled')
        C2.configure(state='disabled')

        # Run bot, if login error exit, if arbitrary error reset and rerun bot
        # If bot is not working, GUI will stay unresponsive
        # If wrong login, bot quits and prompts user to try to run again
        try:
            login(user1, passw1, check_browser1)
        except NameError:
            browser.quit()
            btn.set('Run')
            ent_user.configure(state='normal')
            ent_pass.configure(state='normal')
            C2.configure(state='normal')
        except Exception as e:
            browser.quit()
            if after_id is not None:
                window.after_cancel(after_id)
                window.after_cancel(after_id2)
            btn.set('Run')
            run()

    elif btn.get() == 'Stop':
        btn.set('Run')
        ent_user.configure(state='normal')
        ent_pass.configure(state='normal')
        C2.configure(state='normal')
        try:
            save()
            time.sleep(3)
            browser.quit()
            window.after_cancel(after_id)
            window.after_cancel(after_id2)
        except:
            browser.quit()
            if after_id is not None:
                window.after_cancel(after_id)
                window.after_cancel(after_id2)

# Create a new window
window = tk.Tk()
window.title("Web Idler")
window.resizable(False, False)

# Create a new frame for data entries and checkboxes
frm = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
frm.pack()

# Username
user = tk.StringVar()
lbl_user = tk.Label(master=frm, text="Username:")
ent_user = tk.Entry(master=frm, width=50, textvariable=user)
lbl_user.grid(row=0, column=0, sticky="e")
ent_user.grid(row=0, column=1)

# Password
passw = tk.StringVar()
lbl_pass = tk.Label(master=frm, text="Password:")
ent_pass = tk.Entry(master=frm, width=50, textvariable=passw, show="*")
lbl_pass.grid(row=1, column=0, sticky="e")
ent_pass.grid(row=1, column=1)

# Toggle show password
def showPass():
    if check_pass.get() == 1:
        ent_pass.configure(show="")
    elif check_pass.get() == 0:
        ent_pass.configure(show="*")

# Checkboxes
check_pass = tk.IntVar()
check_browser = tk.IntVar()
C1 = tk.Checkbutton(frm, text="Show password", variable=check_pass, onvalue=1, offvalue=0, command=showPass)
C2 = tk.Checkbutton(frm, text="Display browser", variable=check_browser, onvalue=1, offvalue=0)
C1.grid(row=2, column=1, sticky="w")
C2.grid(row=3, column=1, sticky="w")

# Create a new frame for Run/Stop button
frm_buttons = tk.Frame()
frm_buttons.pack(fill=tk.X, ipadx=5, ipady=0)

# Create the 'Run/Stop' button
btn = tk.StringVar()
btn.set('Run')
btn_run = tk.Button(master=frm_buttons, textvariable=btn, command=run)
btn_run.pack(side=tk.TOP, ipadx=10, pady=2.5)

# Start the application
window.mainloop()