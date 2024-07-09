# =====================================================================
#  THIS IS PART OF THE PROJECT
#  THE SOURCE FILE IS 250MB LARGE, SO IT CANNOT BE INCLUDED IN GITHUB
# =====================================================================

# OPEN THE FILE
print( "Program Begin Processing..." )
file = open( "TextSamples/2022-Airbnb_calendar_AllBooking.csv", "r" )

# ======================================
# EXTRACT FIRST RECORD (HEADER)
# ======================================
header = ( file.readline( ) ).split( "," )

# ======================================
# CLEAN UP HEADER FOR ESCAPE SEQUENCE
# ======================================
colNum = 0

for col in header:
    header[colNum] = header[colNum].replace( "\n", "" )
    colNum += 1


# ======================================
# SEPARATE ALL THE RECORDS BY THEIR
# LISTING_ID
# ======================================
uniqueIDs = {}
curRecord = 0

while( True ):
    record = ( file.readline( ) ).split( "," )

    if( record[0] == '' ):
        print( "\n-- End of Reading --" )
        print( str( len( uniqueIDs ) ) + " records processed")
        print( "\n")
        break

    if( record[0] in uniqueIDs ):
        uniqueIDs[ record[0] ].append( record )
    else:
        uniqueIDs[ record[0] ] = []
        uniqueIDs[ record[0] ].append( record )

    curRecord += 1

file.close( )




# ======================================
# INSERT LISTING RECORDS INTO ANOTHER
# FILE. 2000 LISTINGS PER FILE
# 2000 * 365 RECORDS
# ======================================
fileNum = 1
bookFile = open( "TextSamples/2022-Airbnb-Reservation-Book" + str( fileNum ) + ".csv", "w" )

# WRITE THE HEADERS INTO THE FILE
bookFile.writelines( ", ".join( header ) + "\n" )

# WRITE THE RECORDS INTO THE FILE
listingCount = 1

for id in uniqueIDs:
    # THIS WILL WRITE ALL OF THE RECORD INTO THE NEXT FILE
    if( bookFile.writable ):
        for record in uniqueIDs[ id ]:
            bookFile.writelines( ", ".join( record ) )

        listingCount += 1

        # WHEN 2000 LISTING IS COMPLETE, CLOSE THIS FILE
        if( listingCount == 2000 ):
            # ===================================
            # CLOSE CURRENT FILE
            # ===================================
            print( "end of first 2000 record")
            bookFile.close( ) 

            # =====================
            # CREATE A NEW CSV
            # =====================
            fileNum += 1
            bookFile = open( "TextSamples/2022-Airbnb-Reservation-Book" + str( fileNum ) + ".csv", "w" )
            
            # ===================================
            # WRITE THE HEADERS INTO THE FILE
            # ===================================
            bookFile.writelines( ", ".join( header ) + "\n" )

            # ===================================
            # RESET THE COUNT
            # ===================================
            listingCount = 1


#WRITE 200O LISTING RECORDS INTO THE FILE
#FOR EACH LISTING, WRITE ALL OF THE RECORDS INTO THE FILE
print( "End of Processing" )
bookFile.close( )