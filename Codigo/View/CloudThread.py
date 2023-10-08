# PyQt6 dependencies
from PyQt6.QtCore import QThread, pyqtSignal
from matplotlib import pyplot as plt
from wordcloud import WordCloud

# Class that create a thread to process the files
class CloudThread(QThread):

    finished = pyqtSignal()

    def __init__(self, cloud_parameters, main_controller):
        super().__init__()
        self.cloud_parameters = cloud_parameters
        self.main_controller = main_controller

    def run(self):
        cloud = self.main_controller.get_cloud_words()
        try:
            wordcloud = WordCloud(**self.cloud_parameters).generate_from_frequencies(cloud)
        except Exception as e:
            print(e)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        # Save temporality the cloud in a png then is show it
        plt.savefig("wordcloud.png", bbox_inches='tight', pad_inches=0, transparent=True)
        self.finished.emit()