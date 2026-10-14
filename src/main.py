from src.ui.ConsoleUi import ConsoleUI
#from src.ui.GUI import GUI

if __name__ == "__main__":
    try:
        ui = ConsoleUI()
        ui.start()
    except KeyboardInterrupt:
        pass