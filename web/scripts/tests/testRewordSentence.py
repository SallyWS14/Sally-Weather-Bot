import unittest
import rewordSentence

class Testing(unittest.TestCase):        
    def testIsNewSentence(self):
        a = "Go walk the dog "
        b = rewordSentence.getRewordSentence(a)
        self.assertNotEqual(a, b)
        
    def testIsSentenceSameLength(self):
        sentence = "Go walk the dog"
        a = len(sentence)
        b = len(rewordSentence.getRewordSentence(sentence))
        self.assertEqual(a, b)
        
    def testEmptySentence(self):
        sentence = ""
        a = rewordSentence.getRewordSentence(sentence)
        self.assertEqual(a, "We can't reword an empty sentence")


unittest.main()
