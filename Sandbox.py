
from main import NFTDataProcessor

processor = NFTDataProcessor('NFT_RawData_Offset100')
df_sand = processor.get_data()

print(df_sand.head())
print(df_sand.tail())


