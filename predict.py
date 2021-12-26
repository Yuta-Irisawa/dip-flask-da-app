import pandas as pd
import codecs
import pickle

class Predict:
    test_df = ""
    output_path = ""
    model = ""
    column = []

    def __init__(self, test_path, output_path):
        output_path = "./output/" + output_path
        self.output_path = output_path
        test_path = "./test_csv/" + test_path
        test_df = self.read_data(test_path)
        self.test_df = test_df.fillna(0)
        self.load_model()

    def read_data(self, path):
        with codecs.open(path, "r", "utf-8", "ignore") as f:
            df = pd.read_csv(f)
        return df

    def load_model(self):
        with open('./model/model.pickle', 'rb') as f:
            res = pickle.load(f)

        self.model = res["MODEL"]
        self.column = res["COLUMNS"]

    def predict_x(self):
        test_x = self.test_df[self.column]
        test_index = self.test_df['お仕事No.']

        test_y_pred = self.model.predict(test_x)

        submit_df = pd.DataFrame({
            'お仕事No.': test_index,
            '応募数 合計': test_y_pred
        })

        submit_df.to_csv(self.output_path, index=None)
