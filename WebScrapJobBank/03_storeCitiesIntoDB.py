import mysql.connector


# ==========================================
#  MAIN - MySQL Setup
# ==========================================
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="jobscrappydb"
)

mycursor = mydb.cursor( )


# ==========================================
#  MAIN - Execute Query
# ==========================================
print( "\n\n" )
with open( "./sandboxOutput/cities.txt", 'r', encoding='utf-8' ) as myFile:
    while True:
        content = myFile.readline( ).strip( )
        if len( content ) == 0:
            break

        # =========================================================
        #  INSERT Records into database
        #  Exception will automatically prevent duplicate records.
        # =========================================================
        try:
            insertQuery = f"""INSERT INTO jobbank_data_cities_province( searchkey ) VALUES( "{content}" )"""
            mycursor.execute( insertQuery )
            mydb.commit( )

        except Exception as e:
            print( f"Error: {e} | {content} Is affected" )


print( "End of Program\n" )