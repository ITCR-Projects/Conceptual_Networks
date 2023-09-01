from Codigo.Controller.TextHandlerAdmin import TextHandlerAdmin

class MainController:
    def __init__(self):
        self.textHandlerAdmin = TextHandlerAdmin()

    def addFiles(self, filepath):
        if filepath == "":
            return {
                'response': True,
                'message': "Ruta del archivo inválida",

            }
        return self.textHandlerAdmin.add_file(filepath)

    def textAnalysis(self):
        self.textHandlerAdmin.lexical_analysis()

    def cleanText(self):
        self.textHandlerAdmin.setTextBlank()









