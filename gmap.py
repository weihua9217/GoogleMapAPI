import googlemaps
import pandas as pd

class School():
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
        self._init_school = School()
        self._arrival_df = None
        self._inputFile = None

    def SetInputFile(self):
        self._inputFile = input()

    def SetSchoolInf(self):
        print("請輸入學校名稱")
        self._init_school.SetName(input())
        print("請輸入學校地址")
        self._init_school.SetAddress(input())
        print("學校名稱為",self._init_school._name)
        print("該學校地址為",self._init_school._address)
        ans = ask()
        if(ans==0):
            self.SetSchoolInf()


    def ReadArrivalData(self):
        print("取輸入目的地檔案之excel檔案名稱")
        try:
            self.SetInputFile()
            self._arrival_df = pd.read_excel(self._inputFile)
            return 1
        except:
            print("找不到檔案")
            return 0

    def Calculate(self):
        print(self._init_school._name)
        print(self._init_school._address)
        print(self._arrival_df)
        startSchoolAddress = list()
        startSchoolName = list()
        endSchoolAddress = list()
        endSchoolName = list()

        startSchoolAddress.append(self._init_school._address)
        startSchoolName.append(self._init_school._name)
        for i in self._arrival_df["學校名稱"]:
            endSchoolName.append(i)
        for i in self._arrival_df["學校地址"]:
            endSchoolAddress.append(i)
        distance = list()
        duration = list()
        end = list()
        for i in range(5):
            end.append(endSchoolName[i])
            try:
                result = gmaps.distance_matrix(startSchoolAddress[0], endSchoolAddress[i], mode='driving', region="tw")["rows"][0]["elements"][0]
                c_distance = result["distance"]["text"]
                print(c_distance)
                c_duration = result["duration"]["text"]
                print(c_duration)
                distance.append(c_distance)
                duration.append(c_duration)
            except:
                print("no result")
                distance.append("None")
                duration.append("None")

        df2 = pd.DataFrame({'起始學校':startSchoolName[0],'目標學校':end,'距離':distance,'時間':duration})
        df2.index = df2.index+1
        filename = str(self._init_school._name) + "_" + str(self._inputFile)
        df2.to_excel(filename,index=True)

# class ModeTwo():
#     def __init__(self):

if __name__ == '__main__':

    #input your api key
    GOOGLE_API_KEY = input()
    gmaps = googlemaps.Client(key= GOOGLE_API_KEY)
    #Two mode
    #1:fix one point
    #2:C n 取 2
    #=====[Mode 1]=============
    print("請輸入模式:(1.固定一點 or 2.組合兩點)")
    mode = input()
    if mode=='1':
        Model = ModeOne()
        Model.SetSchoolInf()
        if(Model.ReadArrivalData()==1):
            Model.Calculate()

    elif mode == '2':
        pass
        # Model = ModeTwo()