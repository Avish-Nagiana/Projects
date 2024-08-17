from main import say
import pywhatkit
import webbrowser
import wikipedia

def search_google(query):
    """
    Function to search something using google
    """
    if "google".lower() in query.lower():
        import wikipedia as googleScrap
        # Replacing some words in query
        query = query.replace("dorothea","")
        query = query.replace("google search","")
        query = query.replace("google","")
        say("This is what I found on google")

        try:
            # Using search() from pywhatkit
            pywhatkit.search(query)
            # Google scraping and fetch the summary
            result = googleScrap.summary(query,1)
            # Speaking the result
            say(result)

        except:
            say("No speakable output available")

def search_youtube(query):
    """
    Function to play something on YouTube
    """
    if "youtube".lower() in query.lower():
        say("This is what I found for your search!")
        # Replacing some words in query
        query = query.replace("youtube search","")
        query = query.replace("youtube","")
        query = query.replace("dorothea","")
        # Creating the link to open
        web = "https://www.youtube.com/results?search_query=" + query
        # Using webbrowser to open the link
        webbrowser.open(web)
        # Playing the video on youtube
        pywhatkit.playonyt(query)
        say("It should be done anytime now.")

def search_wikipedia(query):
    """
    Function to search something on wikipedia
    """
    if "wikipedia".lower() in query.lower():
        say("Searching from wikipedia....")
        # Replacing some words in the query
        query = query.replace("wikipedia","")
        query = query.replace("search wikipedia","")
        query = query.replace("dorothea","")
        # Getting the results' summary from wikipedia
        results = wikipedia.summary(query,sentences = 2)
        say("According to wikipedia..")
        # Printing and saying the results
        print(results)
        say(results)