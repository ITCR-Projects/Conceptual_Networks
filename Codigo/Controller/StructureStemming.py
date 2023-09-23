class StructureStemming:
    def __init__(self,):
        self.stem_words = {}

    def add(self, root, word):
        if root not in self.stem_words:
            self.stem_words[root] = [{word: 1}, 1]
        else:
            dic_words = self.stem_words[root][0]
            if word in dic_words.keys():
                self.stem_words[root][0][word] += 1
            else:
                self.stem_words[root][0][word] = 1
            self.stem_words[root][1] += 1

    def merge(self, root1, root2):
        return

    def getStemWords(self):

        return self.stem_words
