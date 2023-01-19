import unittest
from mils_preprocessor import MILSPreprocessor

class TestMilsPreprocessor(unittest.TestCase):
    mils_preprocessor = MILSPreprocessor()
    test_df = mils_preprocessor()
    
    def test_all_texts_scraped(self):
        no_documents = len(TestMilsPreprocessor.test_df.id.unique())
        self.assertEqual(12, no_documents)
    
    def test_strong_words_rumpelstilzchen(self):
        text = TestMilsPreprocessor.test_df[TestMilsPreprocessor.test_df.id=="mils-rumpelstilzchen"].iloc[0].simple
        self.assertIn("Ein Müller hat eine Mühle", text)
    
    def test_strong_word_schneewittchen(self):
        text = TestMilsPreprocessor.test_df[TestMilsPreprocessor.test_df.id=="mils-schneewittchen"].iloc[0].simple
        self.assertIn("nichts", text)
    
    def test_strong_words_rapunzel(self):
        text = TestMilsPreprocessor.test_df[TestMilsPreprocessor.test_df.id=="mils-rapunzel"].iloc[0].simple
        self.assertIn("schwangere Frau", text)

    def test_syllable_separation_rotkaeppchen(self):
        text = TestMilsPreprocessor.test_df[TestMilsPreprocessor.test_df.id=="mils-rotkaeppchen"].iloc[0].simple
        self.assertIn("Rotkäppchen", text)

    def test_syllable_separation_stadtmusikanten(self):
        text = TestMilsPreprocessor.test_df[TestMilsPreprocessor.test_df.id=="mils-stadtmusikanten"].iloc[0].simple
        self.assertIn("Stadtmusikanten", text)

    def test_syllable_separation_dornroeschen(self):
        text = TestMilsPreprocessor.test_df[TestMilsPreprocessor.test_df.id=="mils-dornroeschen"].iloc[0].simple
        self.assertIn("Dornröschen", text)

    def test_introduction_removed(self):
        for identifier in TestMilsPreprocessor.test_df.id.unique():
            text = TestMilsPreprocessor.test_df[TestMilsPreprocessor.test_df.id==identifier].iloc[0].simple
            self.assertTrue("Das Märchen geht so" not in text)

    def test_outro_removed(self):
        for identifier in TestMilsPreprocessor.test_df.id.unique():
            text = TestMilsPreprocessor.test_df[TestMilsPreprocessor.test_df.id==identifier].iloc[0].simple
            self.assertTrue("Das war das Märchen" not in text)

if __name__ == '__main__':
    unittest.main()