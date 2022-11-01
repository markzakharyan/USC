import ROOT
from ROOT import TH1F

def createHistoObject(title: str = "") -> TH1F:
    histogram1 = TH1F(title, "", 100, 0, 70)
    histogram1.GetXaxis().SetTitle(title)
    histogram1.GetYaxis().SetTitle("Frequency")
    return histogram1

histo = createHistoObject("num words")

with open("/Users/space/Desktop/College/secret_sauce/wordfreq2.txt", "r") as file:
    while True:
        if not file.readline():
            break
        try:
            x = int(file.readline().split(" ")[1])
            print(x)
            histo.Fill(x)
        except IndexError:
            break

histo.SaveAs("/Users/space/Desktop/College/secret_sauce/histo.root")