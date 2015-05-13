__author__ = 'matthewgalligan'
import requests,random

class PhraseGenerator(object):
    '''
    The phrase generator has a single static method -- GetPhrase() this retrieves an "idiom" for use as a Pyctionary
    challenge
    '''

    #todo, support multiple phrase types
    EASY = 0
    MEDIUM = 1
    HARD = 2
    IDIOMS = 3

    @staticmethod
    def GetPhrase():
        '''
        Gets a comma delimited list from wordgenerator.net idioms list
        Chooses a random element in the list, and returns it.


        :return: A single "idiom" from the wordgenerator.net service
        '''
        response = requests.post("http://www.wordgenerator.net/application/p.php?type=1&id=idioms_popular&spaceflag=false")
        phrases = response.text.split(",")

        return random.choice(phrases)