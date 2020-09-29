import googlemaps
import pandas as pd

class Location():
    def __init__(self):
        self._name = "None"
        self._address = "None"
    def SetAddress(self,address):
        self._address = address
    def SetName(self,name):
        self._name = name
    def ShowName(self):
        print(self._name)
    def ShowAddress(self):
        print(self._address)

def ask():
    print("是否輸入正確?正確請按Y,否則請按N")
    ans = input()
    if (ans == 'Y'):
        return 1
    elif (ans == 'N'):
        return 0
    else:
        print("輸入錯誤，請重新輸入")
        return ask()


class ModeOne():
    def __init__(self):
        self._init_location = Location()
        self._arrival_df = None
        self._inputFile = None

    def SetInputFile(self):
        self._inputFile = input()

    def SetSchoolInf(self):
        print("請輸入地方名稱")
        self._init_location.SetName(input())
        print("請輸入地方地址")
        self._init_location.SetAddress(input())
        print("該地方名稱為",self._init_location._name)
        print("該地方地址為",self._init_location._address)
        ans = ask()
        if(ans==0):
            self.SetSchoolInf()

    def ReadArrivalData(self):
        print("請輸入目的地檔案之excel檔案名稱")
        try:
            self.SetInputFile()
            self._arrival_df = pd.read_excel(self._inputFile)
            # print(self._arrival_df)
            return 1
        except:
            print("找不到檔案")
            return 0

    def Calculate(self):
        # print(self._init_location._name)
        # print(self._init_location._address)
        # print(self._arrival_df)
        startSchoolAddress = list()
        startSchoolName = list()
        endSchoolAddress = list()
        endSchoolName = list()
        startSchoolAddress.append(self._init_location._address)
        startSchoolName.append(self._init_location._name)
        #print(self._arrival_df)
        for i in self._arrival_df["地方名稱"]:
            endSchoolName.append(i)
        for i in self._arrival_df["地方地址"]:
            endSchoolAddress.append(i)
        distance = list()
        duration = list()
        end = list()
        for i in range(len(endSchoolAddress)):
            end.append(endSchoolName[i])
            try:
                result = gmaps.distance_matrix(startSchoolAddress[0], endSchoolAddress[i], mode='driving', region="tw")["rows"][0]["elements"][0]
                c_distance = result["distance"]["text"]
                c_duration = result["duration"]["text"]
                print(startSchoolName[0],", ",endSchoolName[i])
                print(c_distance,", ",c_duration)
                print("=====================")
                distance.append(c_distance)
                duration.append(c_duration)
            except:
                print("no result")
                distance.append("None")
                duration.append("None")

        df2 = pd.DataFrame({'起始地方':startSchoolName[0],'目標地方':end,'距離':distance,'時間':duration})
        df2.index = df2.index+1
        filename = str(self._init_location._name) + "_" + str(self._inputFile)
        df2.to_excel(filename,index=True)
        print("輸出完畢")

class ModeTwo():
    def __init__(self):
        self._inputFile = None
        self._input_df = None

    def SetInputFile(self):
        self._inputFile = input()

    def SetOutputFileName(self):
        self._outputFileName = input()

    def ReadData(self):
        print("請輸入檔案之excel檔案名稱")
        try:
            self.SetInputFile()
            self._input_df = pd.read_excel(self._inputFile)
            print(self._input_df)
            return 1
        except:
            print("找不到檔案")
            return 0

    def Calculate(self):
        k = 0
        for i in range(len(self._input_df)):
            for j in range(i):
                k+=1
        print("所需計算的次數為"+ str(k) + "次,是否計算? 是請按Y 否則請按N")
        ans = input()
        if(ans=="Y"):
            startName = list()
            endName = list()
            distance = list()
            duration = list()
            print("開始計算")
            for i in range(len(self._input_df)):
                for j in range(i):
                    print(self._input_df.at[i,"地方名稱"],", ",self._input_df.at[j,"地方名稱"])
                    startName.append(self._input_df.at[i,"地方名稱"])
                    endName.append(self._input_df.at[j,"地方名稱"])
                    result = gmaps.distance_matrix(self._input_df.at[i,"地方地址"], self._input_df.at[j,"地方地址"],
                                                   mode='driving', region="tw")["rows"][0]["elements"][0]
                    c_distance = result["distance"]["text"]
                    c_duration = result["duration"]["text"]
                    print(c_distance,", ",c_duration)
                    print("============================")
                    distance.append(c_distance)
                    duration.append(c_duration)
            df2 = pd.DataFrame({'起始學校': startName, '目標學校': endName, '距離': distance, '時間': duration})
            df2.index = df2.index + 1
            filename = "{組合結果}" + str(self._inputFile)
            df2.to_excel(filename, index=True)
            print("輸出完畢")
            return 0
        else:
            return -1


def start():
    print("請輸入模式:(1.固定一點 or 2.組合兩點)")
    mode = input()
    if mode == '1':
        Model = ModeOne()
        Model.SetSchoolInf()
        if (Model.ReadArrivalData() == 1):
            Model.Calculate()

    elif mode == '2':
        Model = ModeTwo()
        if (Model.ReadData() == 1):
            if(Model.Calculate()==-1):
                start()

if __name__ == '__main__':

    #input your api key
    print("請輸入GoogleApiKey:")
    GOOGLE_API_KEY = input()

    try:
        gmaps = googlemaps.Client(key= GOOGLE_API_KEY)
    except:
        print("錯誤的ApiKey")

    start()