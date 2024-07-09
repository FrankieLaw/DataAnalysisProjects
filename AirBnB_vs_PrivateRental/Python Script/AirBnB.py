# FILE PATH FOR READING
test = open( "TextSamples/AirBnBDescription.txt", "r", encoding="utf8" )

# DEFINE THE KEYWORDS THAT I AM LOOKING FOR
keywords = [ "HOME", "HOUSE", "APARTMENT", "CONDO", "BASEMENT", "STUDIO", "LOFT", "HOTEL", "BEDROOM", "SUITE", " APT ", "APPARTMENT", "BED & BREAKFAST", "PRIVATE ROOM", "BUNGALOW", "BACHELOR", "DUPLEX", " ROOM", "PRIVATE SUITE", "COTTAGE", "VILLA", "TOWNHOUSE", "SHARED", "SHARED ROOM", "GUEST HOUSE", "GUESTHOUSE", "GUEST SUITE" ]
results  = { }

# RECORD READING INITIALIZER
entryCount = 0

# SEQUENTIALLY SEARCH ALL KEYWORD AGAINST THE DESCRIPTION
# ANY KEYWORD(S) FOUND ARE PLACED INSIDE OF RESULT DICTIONARY
while( True ):
    entryCount += 1
    results[entryCount] = [ ]

    descriptionString = ( test.readline( ) ).upper( )

    if( descriptionString == '' ):
        print( "End of File" )
        break

    for keyword in keywords:
        sFound = descriptionString.find( keyword )

        if( sFound != -1 ):
            results[ entryCount ].append( "YES" )
        else:
            results[ entryCount ].append( "-" )

# CLOSE FILE POINTERS
test.close( )



# FILE PATH FOR WRITING
check = open( "TextSamples/AirBnBDescription-Results.txt", "w" )

#INSERT COLUMN HEADERS
header = ', '.join( keywords )
check.writelines( header + "\n" )

#INSERT RECORDS
for index in results:
    record = ', '.join( results[index] )
    check.writelines( record + "\n" )

check.close( )