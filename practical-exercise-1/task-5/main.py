import pandas as pd

htmlFile = pd.read_html('text_5_var_65', encoding='utf-8')
htmlFile[0].to_csv('answer_5_var_65.csv')