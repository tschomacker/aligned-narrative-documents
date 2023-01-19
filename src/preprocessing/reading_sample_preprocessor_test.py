import unittest
from reading_sample_preprocessor import ReadingSamplePreprocessor

class TestEBParser(unittest.TestCase):
    preprocessor = ReadingSamplePreprocessor()
    
    eb_test_df = preprocessor(data_path="../../data/eb_data.json", csv_path="../../data/eb.csv", corpus='eb', verbose=False)
    pv_test_df = preprocessor(data_path="../../data/pv_data.json", csv_path="../../data/pv.csv", corpus='pv', verbose=False)
    kv_test_df = preprocessor(data_path="../../data/kv_data.json", csv_path="../../data/kv.csv", corpus='kv', verbose=False)
    
    def test_page_numbers_removed_verwandlung(self):
        text = TestEBParser.eb_test_df[TestEBParser.eb_test_df.id=="eb-verwandlung"].iloc[0].simple
        self.assertIn("100 Mal bestimmt", text)
        
    def test_page_numbers_removed_verwandlung(self):
        text = TestEBParser.eb_test_df[TestEBParser.eb_test_df.id=="eb-verwandlung"].iloc[0].simple
        self.assertNotIn("9", text)
    
    def test_footnotes_removed_sawyer(self):
        text = TestEBParser.eb_test_df[TestEBParser.eb_test_df.id=="eb-sawyer"].iloc[0].simple
        self.assertNotIn("[3]", text)
    
    def test_ending_removed_prinz(self):
        text = TestEBParser.pv_test_df[TestEBParser.pv_test_df.id=="pv-prinz"].iloc[0].simple
        self.assertNotIn("Passanten", text)
        self.assertIn("beginnt zu lesen", text)
    
    def test_ending_removed_wolfsblut(self):
        text = TestEBParser.pv_test_df[TestEBParser.pv_test_df.id=="pv-wolfsblut"].iloc[0].simple
        self.assertIn("Gejammer", text)
    
    def test_ending_removed_schimmelreiter(self):
        text = TestEBParser.pv_test_df[TestEBParser.pv_test_df.id=="pv-schimmelreiter"].iloc[0].simple
        self.assertNotIn("Leseprobe", text)
        self.assertNotIn("Gutenberg", text)
        
    
    
    def test_begging_removed_schimmelreiter(self):
        text = TestEBParser.pv_test_df[TestEBParser.pv_test_df.id=="pv-schimmelreiter"].iloc[0].original
        self.assertNotIn("Leseprobe", text)
        self.assertNotIn("Gutenberg", text)
        
    
    def test_undine(self):
        simple_text = TestEBParser.pv_test_df[TestEBParser.pv_test_df.id=="pv-undine"].iloc[0].simple
        self.assertIn("keine Antwort", simple_text)
        self.assertNotIn("14", simple_text)
        
        original_text = TestEBParser.pv_test_df[TestEBParser.pv_test_df.id=="pv-undine"].iloc[0].original
        self.assertIn("achtlos nun jeglicher", original_text)
        self.assertIn("Wie der Ritter zu dem Fischer kam", original_text)
        self.assertNotIn("Inhalt", original_text)
        
    
    def test_pv_sandmann(self):
        simple_text = TestEBParser.pv_test_df[TestEBParser.pv_test_df.id=="pv-sandmann"].iloc[0].simple
        self.assertIn("Lebe wohl", simple_text)
        self.assertNotIn("14", simple_text)
        
        original_text = TestEBParser.pv_test_df[TestEBParser.pv_test_df.id=="pv-sandmann"].iloc[0].original
        self.assertIn("Gemütsstimmung", original_text)
        self.assertIn("Kurz und gut", original_text)
        self.assertNotIn("Majorat", original_text)
        self.assertNotIn("Clara an Nathanael", original_text)
        self.assertNotIn("Inhalt", original_text)
        self.assertNotIn("Gutenberg", original_text)
        
    
    def test_kv_sandmann(self):
        simple_text = TestEBParser.kv_test_df[TestEBParser.kv_test_df.id=="kv-sandmann"].iloc[0].simple
        self.assertIn("nur ein Traum", simple_text)
        self.assertNotIn("Kindermann", simple_text)
        self.assertNotIn("Hoffmann", simple_text)
        
        original_text = TestEBParser.kv_test_df[TestEBParser.kv_test_df.id=="kv-sandmann"].iloc[0].original
        self.assertIn("Stadt verlassen.", original_text)
        self.assertIn("Gewiß", original_text)
        self.assertNotIn("Majorat", original_text)
        self.assertNotIn("Clara an Nathanael", original_text)
        self.assertNotIn("Inhalt", original_text)
        self.assertNotIn("Gutenberg", original_text)
        self.assertNotIn("Jahr mochte vergangen", original_text)
        
    
    def test_kv_schimmelreiter(self):
        simple_text = TestEBParser.kv_test_df[TestEBParser.kv_test_df.id=="kv-schimmelreiter"].iloc[0].simple
        self.assertIn("kaum je", simple_text)
        self.assertNotIn("6", simple_text)
        self.assertNotIn("Kindermann", simple_text)
        self.assertNotIn("Storm", simple_text)
        
        original_text = TestEBParser.kv_test_df[TestEBParser.kv_test_df.id=="kv-schimmelreiter"].iloc[0].original
        self.assertIn("guten Mutes", original_text)
        self.assertNotIn("langgestreckte ", original_text)
        self.assertNotIn("Storm", simple_text)
        
        
    
        
    
    def test_naechte(self):
        simple_text = TestEBParser.pv_test_df[TestEBParser.pv_test_df.id=="pv-naechte"].iloc[0].simple
        self.assertIn("Ich bin so glücklich", simple_text)
        self.assertNotIn("passanten", simple_text)
        
        original_text = TestEBParser.pv_test_df[TestEBParser.pv_test_df.id=="pv-naechte"].iloc[0].original
        self.assertIn("Die erste Nacht", original_text)
        self.assertNotIn("Inhalt", original_text)
        self.assertNotIn("Dostojewski", original_text)

    
    def test_naechte_explanation_box(self):
        simple_text = TestEBParser.pv_test_df[TestEBParser.pv_test_df.id=="pv-naechte"].iloc[0].simple
        self.assertNotIn("Unterstrichene Wörter", simple_text)
            
        

if __name__ == '__main__':
    unittest.main()