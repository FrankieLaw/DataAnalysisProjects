# ===================================================================================
#  This program is used to extract rawData and strip it of all the cities/provinces
#  Afterwards, the result will get inserted into SQLite DB
#
#  1 -> All of the files will be process first and store into a Dictionary.
#  2 -> For every key in Dictionary, it will query SQLite DB for duplicate key.
#       -> If it doesn't exist, INSERT INTO TABLE
# ===================================================================================
import glob



# ==============================================
#  MAIN - Variable Setup
# ==============================================
allRawFiles           = glob.glob( "./rawData/*.txt" )
cityProvinceDict:dict = {}


# ==============================================
#  MAIN - Program Begin Execution
# ==============================================
for txtFile in allRawFiles:
    with open( txtFile, 'r', encoding='utf-8' ) as contentFile:
        while True:
            data = contentFile.readline( ).split( "|" )

            if len( data ) == 8 :
                key = f"{data[6]}, {data[5]}"
            else:
                break   #EOF Marker
            
            if key not in cityProvinceDict.keys( ):
                cityProvinceDict[key] = 0


# ==============================================
#  MAIN - Saving Results to a File
# ==============================================
with open( "./sandboxOutput/cities.txt", "w", encoding='utf-8' ) as myFile:
    for key, value in cityProvinceDict.items( ):
        myFile.write( key + "\n" )
