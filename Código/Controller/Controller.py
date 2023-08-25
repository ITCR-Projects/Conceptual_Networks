from Código.Controller.TextHandlerAdmin import TextHandlerAdmin


class MainController:
    def __init__(self):
        self.textHandlerAdmin = TextHandlerAdmin()

    def addFiles(self, files):
        if len(files) < 0:
            return
        return self.textHandlerAdmin.add_files(files)

