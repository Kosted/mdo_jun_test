import pickle
from collections import OrderedDict


class Recommendations:

    def __init__(self, delta=1, force_reread_flag=False):
        self.pickle_filename = 'pickle1' + '.pickle'
        self.delta = None if delta == 1 else delta
        self._recommendation_dict = {}
        self.read_recommendation(force_reread_flag)

    def create_sku_recommendation(self, sku):
        self._recommendation_dict[sku] = OrderedDict()

    def append_recommendation(self, sku, rank, recommend_sku):
        if rank not in self._recommendation_dict[sku]:
            self._recommendation_dict[sku][rank] = [recommend_sku, ]
        else:
            self._recommendation_dict[sku][rank].append(recommend_sku)

    def get_recommendations(self, sku):
        if self.delta is not None:
            return {key: self._recommendation_dict[sku][key] for key in self._recommendation_dict[sku].keys() if
                    key >= 1 - self.delta}
        else:
            return {key: value for key, value in self._recommendation_dict[sku].items()}

    def sort_all_recommendations(self):
        for key in self._recommendation_dict:
            self._recommendation_dict[key] = sorted(self._recommendation_dict[key].items())

    def __contains__(self, item):
        return item in self._recommendation_dict

    def write_to_pickle(self):
        with open(self.pickle_filename, 'wb') as handle:
            pickle.dump(self._recommendation_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def read_from_pickle(self):
        with open(self.pickle_filename, 'rb') as handle:
            self._recommendation_dict = pickle.load(handle)

    def read_from_csv(self):
        print("Read from csv file.")
        with open('recommends.csv', 'r') as file:
            for line in file:
                sku, recommend_sku, rank = line.split(',')
                rank = float(rank.replace('\n', ""))
                if sku not in self:
                    self.create_sku_recommendation(sku)

                self.append_recommendation(sku, rank, recommend_sku)

        self.write_to_pickle()

    def read_recommendation(self, force_reread_flag=False):
        print("Start read from file.")
        if force_reread_flag:
            return self.read_from_csv()

        try:
            self.read_from_pickle()
        except FileNotFoundError:
            print("pickle file doesent exist.")
            self.read_from_csv()
        print("End read from file.")

    def set_delta(self, delta):
        self.delta = delta
