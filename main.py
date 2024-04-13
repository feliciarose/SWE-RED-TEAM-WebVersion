# main.py

from incollege import InCollegeApp

def main():
    app = InCollegeApp()
    while True:
        language = app.choose_language()
        if language not in ["Invalid language. Please choose exactly English or Spanish."]:
            break
        print(language)
    print(language)

    app.main_menu()

if __name__ == "__main__":
    main()
