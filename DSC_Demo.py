import googlemaps
import pandas as pd

class DistanceMatrix():
    def __init__(self):
        self._startPlace = {"Name": None , "Address": None}  # dict
        self._inputDataFrame = None
        self._outputDistance = list()
        self._outputDuration = list()

    def SetStartPlace(self):
        self._startPlace['Name'] = "政治大學"
        self._startPlace['Address'] = "台北市文山區指南路二段64號"

    def SetInputDataFrame(self):
        self._inputDataFrame = pd.read_csv("./dat.in.csv")

    def Calculate(self):
        # for i in range(len(self._inputDataFrame["學校"])):
            # print(self._inputDataFrame["學校"][i])
        for j in range(len(self._inputDataFrame["學校"])):
                                            # original address           # destination address
            result = gmaps.distance_matrix(self._startPlace["Address"], self._inputDataFrame["地址"][j] ,mode='driving',
                                           region='tw')
            # print(result)
            result = result["rows"][0]["elements"][0]
            self._outputDistance.append(result["distance"]["text"])
            self._outputDuration.append(result["duration"]["text"])

    def Output(self):
        output_df = pd.DataFrame({"起始學校":self._startPlace["Name"],"終點學校":self._inputDataFrame["學校"],
                                  "距離":self._outputDistance,"時間":self._outputDuration})
        filename = "dat.out.csv"
        output_df.to_csv(filename,index=True)

    def Start(self):
        self.SetStartPlace()
        self.SetInputDataFrame()
        self.Calculate()
        self.Output()




class PlacesAPI():
    def __init__(self):
        self.cities = ["臺北市","新北市","桃園市","臺中市","臺南市","高雄市","基隆市","新竹市","嘉義市","新竹縣",
        "苗栗縣","彰化縣","南投縣","雲林縣","嘉義縣","屏東縣","宜蘭縣","花蓮縣","臺東縣","澎湖縣"]
        self.results = list()
        self.ids = list()
        self.store_inf = list()

    def Compute(self):
        # 　for city in self.cities:
        result = gmaps.geocode(self.cities[0])
        print(result)
        loc = result[0]['geometry']['location']
        print(loc)  # 回傳經緯度
        query_result = gmaps.places_nearby(keyword="百貨", location=loc, radius=10000)
        # print(query_result)
        self.results.extend(query_result['results'])
        # for i in self.results:
        #  print(i)
        for place in self.results:
            self.ids.append(place['place_id'])
        self.ids = list(set(self.ids))  # 去掉重複的
        for id in self.ids:
            self.store_inf.append(gmaps.place(place_id=id, language='zh-TW')['result'])

    def Output(self):
        output = pd.DataFrame.from_dict(self.store_inf)
        print(output)
        filename = "dat2.out.xlsx"
        output.to_excel(filename, index=True)

    def Start(self):
        self.Compute()
        self.Output()




if __name__ == '__main__':
    GOOGLE_API_KEY = "Your Key"
    gmaps = googlemaps.Client(key= GOOGLE_API_KEY)
    # stage = DistanceMatrix()
    # stage.Start()
    stage2 = PlacesAPI()
    stage2.Start()