from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import tkinter as tk
from tkinter import messagebox

browser = ""

def login(user, passw, display):
    global browser
    if display.get() == 1:
        browser = webdriver.Chrome('chromedriver')
    elif display.get() == 0:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_driver = "chromedriver"
        browser = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver)
    else:
        print('Browser is not supported :('
        '''
        TODO
        write an exception if browser is not chrome or phantom 
        ''')

    # Login
    browser.get('https://wfg.xcelsolutions.com')
    username = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="reduxFormInputField1"]')))
    password = browser.find_element_by_xpath('//*[@id="reduxFormInputField3"]')
    username.send_keys(user.get())
    password.send_keys(passw.get())
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

    # Close dialog box if it exists
    try:
        dialog_box = WebDriverWait(browser, 5).until\
            (EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[2]/button')))
        dialog_box.click()
    except:
        pass

    choose_course_content = WebDriverWait(browser, 10).until\
        (EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[3]/div/div[2]/div/div[4]/div[1]/div[2]/div/div[4]/div[1]/div[2]/div/div/div/div')))
    choose_course_content.click()

    while 1:
        get_hours()


def get_hours():
    print('Farm start')
    complete_course = WebDriverWait(browser, 10).until\
        (EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[3]/div/div[2]/div/div[4]/div[1]/div[2]/div/div[3]/div[2]/div[2]/div/div[1]/div/div[2]/div/button')))
    complete_course.click()

    # Click past identification check
    frame = WebDriverWait(browser, 10).until \
        (EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/iframe')))
    browser.switch_to.frame(frame)

    identify_button = WebDriverWait(browser, 10).until\
        (EC.presence_of_element_located((By.XPATH, '//*[@id="identify_student_submit"]')))
    identify_button.click()

    # Farm 10 minutes
    time.sleep(596)

    save_button = WebDriverWait(browser, 10).until\
        (EC.element_to_be_clickable((By.XPATH, '//*[@id="exitButton"]')))
    save_button.click()
    print('Farmed 10 minutes')

    time.sleep(10)

# Render GUI
def render():
    global browser

    # Create a new window
    window = tk.Tk()
    window.title("Web Idler")
    window.resizable(False, False)

    # Create a new frame for data entries and checkboxes
    frm = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
    # Pack the frame into the window
    frm.pack()

    user = tk.StringVar()
    lbl_user = tk.Label(master=frm, text="Username:")
    ent_user = tk.Entry(master=frm, width=50, textvariable=user)
    lbl_user.grid(row=0, column=0, sticky="e")
    ent_user.grid(row=0, column=1)

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

    check_pass = tk.IntVar()
    check_browser = tk.IntVar()
    C1 = tk.Checkbutton(frm, text="Show password", variable=check_pass, onvalue=1, offvalue=0, command=showPass)
    C2 = tk.Checkbutton(frm, text="Display browser", variable=check_browser, onvalue=1, offvalue=0)
    C1.grid(row=2, column=1, sticky="w")
    C2.grid(row=3, column=1, sticky="w")

    # Recursive helper for run()
    def runloop():
        try:
            login(user, passw, check_browser)
        except NameError:
            browser.quit()
            btnText.set('Run')
            ent_user.configure(state='normal')
            ent_pass.configure(state='normal')
            C2.configure(state='normal')
        except Exception as e:
            browser.quit()
            runloop()

    # Run/Stop program through button
    def run():
        if btnText.get() == 'Run':
            btnText.set('Stop')
            ent_user.configure(state='disabled')
            ent_pass.configure(state='disabled')
            C2.configure(state='disabled')
            runloop()

        elif btnText.get() == 'Stop':
            btnText.set('Run')
            ent_user.configure(state='normal')
            ent_pass.configure(state='normal')
            C2.configure(state='normal')
            try:
                save_button = WebDriverWait(browser, 1).until \
                    (EC.element_to_be_clickable((By.XPATH, '//*[@id="exitButton"]')))
                save_button.click()
                browser.quit()
            except:
                browser.quit()

    # Create a new frame for Run/Stop button
    frm_buttons = tk.Frame()
    frm_buttons.pack(fill=tk.X, ipadx=5, ipady=0)

    # Create the 'Run/Stop' button
    btnText = tk.StringVar()
    btnText.set('Run')
    btn_run = tk.Button(master=frm_buttons, textvariable=btnText, command=run)
    btn_run.pack(side=tk.TOP, ipadx=10, pady=2.5)

    # Start the application
    window.mainloop()


def main():
    render()

main()
