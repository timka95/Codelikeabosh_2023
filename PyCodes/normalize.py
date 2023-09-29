import pandas as pd


excel_file = '../DataFiles/DevelopmentData.xlsx'


df = pd.read_excel(excel_file)

# Normalizáció
df['FirstObjectDistance_X'] /= 128
df['FirstObjectDistance_Y'] /= 128
df['SecondObjectDistance_X'] /= 128
df['SecondObjectDistance_Y'] /= 128
df['ThirdObjectDistance_X'] /= 128
df['ThirdObjectDistance_Y'] /= 128
df['FourthObjectDistance_X'] /= 128
df['FourthObjectDistance_Y'] /= 128
df['VehicleSpeed'] /= 256
df['FirstObjectSpeed_X'] /= 256
df['FirstObjectSpeed_Y'] /= 256
df['SecondObjectSpeed_X'] /= 256
df['SecondObjectSpeed_Y'] /= 256
df['ThirdObjectSpeed_X'] /= 256
df['ThirdObjectSpeed_Y'] /= 256
df['FourthObjectSpeed_X'] /= 256
df['FourthObjectSpeed_Y'] /= 256


output_file = '../DataFiles/normalized_data.xlsx'
df.to_excel(output_file, index=False)

print("Normalizált adatok mentve:", output_file)
