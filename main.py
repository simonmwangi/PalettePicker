import app_windows

if __name__ == "__main__":
    # This is where the application will start
    my_app = app_windows.WelcomeWindow()
    my_app.iconbitmap('logo.ico')
    my_app.mainloop()
