from Codigo.Controller.TextHandlerAdmin import TextHandlerAdmin
#HOLA MUNDO PRUEBA
#HOLAMUNDO PRUEBA 2

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
        return self.textHandlerAdmin.lexical_analysis()

    def cleanText(self):
        self.textHandlerAdmin.setTextBlank()

    def setIgnoreWords(self,iwords):
        self.textHandlerAdmin.setIgnoreWords(iwords)

    def addwordstoignore(self, iwords):
        self.textHandlerAdmin.addwordstoignore(iwords)

    def getStatistics(self):
        return  self.textHandlerAdmin.statistics()









