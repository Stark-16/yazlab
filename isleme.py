import jpype
import jpype.imports
import pandas as pd
from jpype.types import *
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download("punkt")
nltk.download("stopwords")

zemberek_jar_path = "C:\\Users\\AlperenGormez\\Desktop\\nnnnnnnnnnnnn\\Zemberek-Python-Examples\\bin\\zemberek-full.jar"

if not jpype.isJVMStarted():
    jpype.startJVM(classpath=[zemberek_jar_path])

TurkishMorphology = jpype.JClass("zemberek.morphology.TurkishMorphology")
morphology = TurkishMorphology.createWithDefaults()

file_path = 'articles.csv'
#temizlenmek istenen dosyalar buraya yazılır.
try:
    data = pd.read_csv(file_path, delimiter=',', encoding='utf-8')
    if 'Comment' not in data.columns:
        data.columns = ['Rating', 'Comment'] 
except Exception as e:
    print(f"Bir hata oluştu: {e}")

stop_words = set(stopwords.words("turkish"))

simplified_output = []

for index, row in data.iterrows():
    comment_line = row['Comment']  
    if pd.notnull(comment_line):
        tokens = word_tokenize(comment_line)
        tokens = [word for word in tokens if word.lower() not in stop_words]
        cleaned_comment = " ".join(tokens)

        analysis = morphology.analyzeSentence(cleaned_comment)
        processed_line = []

        for result in analysis:
            for single_analysis in result.getAnalysisResults():
                root = single_analysis.getDictionaryItem().lemma 
                pos = single_analysis.getDictionaryItem().primaryPos.name() 
                processed_line.append({"input": result.getInput(), "root": root, "type": pos})

        simplified_output.append({"original_comment": comment_line, "processed": processed_line})

output_df = pd.DataFrame(simplified_output)
output_df.to_csv('simplified_comments.csv', index=False, encoding='utf-8-sig')

jpype.shutdownJVM()