import sys
import glob
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List


# ==============================================
#  CONSTANTS
# ==============================================
from modules.CADGeo import *


# ==============================================
#  Functions
# ==============================================
def cleanHREF( link:List ) -> str:
    copy = link.copy( )
    if copy[0] == '/':
        del copy[0]

    return ''.join( copy )


def cleanCommas( title:str ) -> str:
    return title.replace( ",", "" )


def cleanDate( date:str ) -> str:
    return '-'.join( date.replace( ",", "" ).split( ) )





# ==============================================
#  MAIN - Program Begin Execution
# ==============================================
countOfPosts:int = 0
allJobPostings   = glob.glob( "./unparsedHTML/*.html" )

print( "\n\n" )
print( "Program Begin Executing...\n" )

for x in allJobPostings:
    provinceAbbv:str = x.split( '-' )[0][-2:]
    provinceFull:str = getProvinceFullString( provinceAbbv )
    domain:str       = "https://www.jobbank.gc.ca/"
    todaysDate       = datetime.today().strftime('%m-%d-%Y')
    htmlDoc:str      = ""
    parseResult:List = []
    outputFileName   = provinceAbbv + "-" + todaysDate + ".txt"


    with open( x, 'r', encoding='utf-8' ) as myFile:
        htmlDoc = myFile.read( )

        soup = BeautifulSoup( htmlDoc, 'lxml' )
        articleList = soup.find_all( "article" )
        countOfPosts += len( articleList )
        print( f"Lenght of Article List: {len(articleList)}\n" )

        for article in articleList:
            # print( "\n\n" )
            articleResult:List = []

            anchorTag   = article.find( 'a' )
            jobTitleTag = article.find( 'span', class_='noctitle' )
            unorderList = article.find( 'ul' )
            postDateTag = unorderList.find( 'li', class_='date' )
            businessTag = unorderList.find( 'li', class_='business' )
            locationTag = unorderList.find( 'li', class_='location' )
            salaryTag   = unorderList.find( 'li', class_='salary' )


            articleID = article['id'].replace( 'article-', '' )
            aHref     = cleanHREF( list( anchorTag['href'] ) )
            jobTitle  = list( jobTitleTag )[0].strip( )
            postDate  = cleanDate( postDateTag.text.strip( ) )
            business  = businessTag.text.strip( )
            salary    = ' '.join( list( salaryTag )[-1].split( ) )

            location  = list( locationTag )[-1].strip( ).split( " " )
            location  = ' '.join( location[0:len(location)-1] )

            if location.lower( ) == "various":
                continue

            # location  = location.encode( 'utf-8' )


            articleResult.append( articleID )
            articleResult.append( domain + aHref )
            articleResult.append( jobTitle )
            articleResult.append( postDate )
            articleResult.append( business )
            articleResult.append( provinceFull )
            articleResult.append( location )
            articleResult.append( salary )

            parseResult.append( articleResult )
            
       
    # ==============================================
    #  MAIN - Write results to file
    # ==============================================
    with open( "./rawData/" + outputFileName, 'w', encoding='utf-8' ) as mySaveFile:
        headerList = [ 'JobId', 'Link', 'Job Title', 'Post Date', 'Business', 'Province/State', 'City', 'Salary']
        mySaveFile.write( '|'.join( headerList ) + "\n" )

        for listing in parseResult:
            mySaveFile.write(  '|'.join( list( listing ) ) + "\n" )
    

print( "\nProgram End..." )
print( f"Total Posting Processed: {countOfPosts}")
print( "\n\n" )
