# ==============================================================
#  00_main.py
#  This program will scrap the entire Job Bank for job postings
#  and stores them into a [html] file to be process afterwards.
# ==============================================================

'''
	[ ] Start Scrapping at Provinical Level
	[ ] 	If there are less than 10,000 jobs at provincial level.  Scrap it.
	[ ]			NB-07-16-2024
	[ ]     Else it needs to be broken down into city size.
	[ ] 		Figure out which Province it is.
	[ ]			Query the province and store all of its city into a list
	[ ]			And then loop through each city and scrap it.
	[ ]				ON-Mississauga-07-16-2024
	[ ]				ON-Milton-07-16-2024
'''

import pyautogui
import time
import webbrowser
import math
import win32clipboard
import requests
import mysql.connector
from bs4 import BeautifulSoup
from datetime import datetime, date


# ==============================================
#  FUNCTION
# ==============================================
def saveHTMLtoFile( fileName:str ) -> None:
    # Click on the browser
    # Open Developers Tool
    waitTime:float = 1
    outputFolder:str = "./test/"

    if Scrappy["debugMode"]:
        outputFolder = "./test/"
    else:
        outputFolder = "./unparsedHTML/"


    pyautogui.moveTo( 178, 369, 0.25 )  
    time.sleep( waitTime )
    pyautogui.click( )
    time.sleep( waitTime )
    pyautogui.press( 'f12' )
    time.sleep( waitTime + 10 )


    # Start looking for HTML
    pyautogui.moveTo( 1167, 175, 0.25 ) 
    time.sleep( waitTime ) 
    pyautogui.click( )
    time.sleep( waitTime ) 
    pyautogui.hotkey('ctrl', 'c')
    time.sleep( waitTime ) 


    # Search for Results Job Div
    win32clipboard.OpenClipboard()

    with open( outputFolder + fileName, 'w', encoding='utf-8' ) as myFile:
        myFile.write( win32clipboard.GetClipboardData( ) )

    win32clipboard.CloseClipboard()

    pyautogui.press( 'f12' )
    print( f"End of Copying HTML to {outputFolder + fileName}....\n" )

def isScrapOutdated( myDate ) -> bool:
    if myDate == None:
        return True
    
    m, d, y = myDate.split( "-" )
    
    # Days since last update
    date1 = date( int(y), int(m), int(d) )
    date2 = date.today( )    
    delta = date2 - date1

    if delta.days >= 7:
        return True
    else:
        return False



# ==============================================
#  CONSTANTS - MODULES
# ==============================================
from modules.ScrappySettings import Scrappy
from modules.CADGeo import *


# ==============================================
#  VARIABLES
# ==============================================
postCountByProvince:dict = {'YT': 338, 'SK': 3989, 'PE': 384, 'NU': 103, 'NS': 2817, 'NL': 1773, 'BC': 34619, 'AB': 30819, 'MB': 3508, 'NB': 2097, 'QC': 15253, 'ON': 44742, 'NT': 211}


# Program Starts
print( "\n\n" )
print( "Program Started..." )


# # Initialization Block
# print( "Initializing Variables..." )
# for abbrCode in PROVINCE.keys( ):
#     if abbrCode not in postCountByProvince.items( ):
#         postCountByProvince[ abbrCode ] = 0


# # Get Post Counts by Province
# print( "Grab Post Counts by Provinces..." )
# for abbrCode in postCountByProvince.keys( ):
#     searchLink:str = 'https://www.jobbank.gc.ca/jobsearch/jobsearch?sort=M&fprov=' + abbrCode

#     content = requests.get( searchLink ).text
#     soup    = BeautifulSoup( content, 'lxml' )
#     postTag = soup.find( 'span', class_="found", role="status" )

#     postCountByProvince[ abbrCode ] = int( postTag.text.replace( ",", "" ) )
#     print( f"{abbrCode} Complete..." )
#     time.sleep( 2 ) # Don't spam the website


# Start Scrapping Job Postings
print( "\nStart Scrapping Process..." )
for abbrCode, postCount in postCountByProvince.items( ):
    searchLink:str = 'https://www.jobbank.gc.ca/jobsearch/jobsearch?sort=M&fprov=' + abbrCode

    clickMore:int  = math.ceil( ( postCount ) / 25 ) - 2
    
    print( f"Extracting {abbrCode} with {postCount} job postings" )
    if postCount < 10000:
        continue
        # print( f"Processing: {searchLink}" )
        # outputFile:str = abbrCode + "-jobPostings.html"

        # webbrowser.open( searchLink )
        # time.sleep( 20 )

        # pyautogui.keyDown('end')
        # pyautogui.keyUp('end')
        
        # while True:    
        #     pyautogui.moveTo( 1100, 600, 0.25 )
        #     pyautogui.click( )

        #     time.sleep( 5 )
        #     pyautogui.keyDown('end')
        #     pyautogui.keyUp('end')

        #     if( clickMore == 0 ):
        #         print( f"{abbrCode} is done Processing..." )
        #         break
            
        #     clickMore -= 1
        #     print( f"Paginate: {clickMore}", end=" | " )

        #     if clickMore % 20 == 0:
        #         time.sleep( 10 )        # Take a break

        # saveHTMLtoFile( outputFile )
        # time.sleep( 3 )

        # pyautogui.moveTo( 380, 20, 0.25 )
        # pyautogui.click( button='middle' )

    else:
        print( f"Processing {abbrCode} with {postCount}..." )

        # Retrieve Full Province String
        provinceStr:str = getProvinceFullString( abbrCode )
        cityQuery:str = f"""
        SELECT * 
        FROM jobbank_data_cities_province 
        WHERE searchkey LIKE '%{provinceStr}%'
        ORDER BY searchkeyID
        """

        # Establish Database Connection
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="jobscrappydb"
        )
        mycursor = mydb.cursor( )
        

        # Retrieve Full List of City Names
        cityList:list  = []
        try:
            mycursor.execute( cityQuery )
            citiesList = mycursor.fetchall( )
            print( f"Total Cities: {len(citiesList)}")

        except Exception as e:
            print( f"Error: {e} | something Is affected" )


        # WebScrap each City
        for record in citiesList:

            # Check to see if it is updated
            # Scrap the Cities that is not updated
            print( f"Scrapping {record[1]}..." )
            if isScrapOutdated( record[2] ) or record[2] == None:

                # Setup Query String
                city           = record[1].split( ", " )
                city           = ' '.join( city[0:len(city)-1] )
                cityQ:str      = city.replace( " ", "+" )
                provQ:str      = provinceStr.replace( " ", "+" )

                domain:str     = f"https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=&locationstring="
                cityQuery:str  = f"{cityQ}%2C{provQ}&d=5"

                searchLink:str = f"{domain}{cityQuery}"


                # Retrieving Post Counts
                content = requests.get( searchLink ).text
                soup    = BeautifulSoup( content, 'lxml' )
                postTag = soup.find( 'span', class_="found", role="status" )

                postCnt = int( postTag.text.replace( ",", "" ) )
                time.sleep( 5 )


                # Calculate Pagination
                clickMore:int = math.ceil( ( postCnt - 25 ) / 25 )


                # Open Browser and Expand all Jobs
                webbrowser.open( searchLink )
                time.sleep( 20 )


                # Debugging Notes
                print( "\n" )
                print( f"{city} | Post: {postCnt} | Click: {clickMore}" )


                # Expand all postings
                while True:    
                    pyautogui.moveTo( 1100, 600, 0.25 )
                    pyautogui.click( )

                    time.sleep( 5 )
                    pyautogui.keyDown('end')
                    pyautogui.keyUp('end')

                    if( clickMore == 0 ):
                        print( f"{city} city is done Processing..." )
                        break
                    
                    clickMore -= 1
                    print( f"Paginate: {clickMore}" )

                    if clickMore % 20 == 0:
                        time.sleep( 10 )        # Take a break


                # Output File
                outputFile:str = abbrCode + "-" + city.replace( " ", "-" ) + "-jobPostings.html"
                saveHTMLtoFile( outputFile )
                time.sleep( 3 )


                # Close Browser
                pyautogui.moveTo( 380, 20, 0.25 )
                pyautogui.click( button='middle' )


                # Update Database - City is Updated with new date
                todaysDate = ( date.today( ) ).strftime( "%m-%d-%Y" )
                updateQuery:str = f"""
                UPDATE jobbank_data_cities_province
                SET scrapTimeStamp = "{todaysDate}"
                WHERE searchKey = "{city}, {provinceStr}"
                """

                mycursor.execute( updateQuery )
                mydb.commit( )

                
                # Debugging Notes
                print( outputFile )
                print( searchLink )
                print( f"Update DB | Rows affected {mycursor.rowcount}" )
                print( f"End or Processing {city} city..." )

                raise SystemExit
            else:
                continue


print( "\n======================")
print( " Program End" )
print( "======================\n")
# {'YT': 338, 'SK': 3989, 'PE': 384, 'NU': 103, 'NS': 2817, 'NL': 1773, 'BC': 34619, 'AB': 30819, 'MB': 3508, 'NB': 2097, 'QC': 15253, 'ON': 44742, 'NT': 211}
