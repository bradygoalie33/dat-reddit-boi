import requests
import json
API_KEY = 'J2YBhFl7nOmshtfhApDXZrqLIg3Gp1XVUOCjsnG6JYVznDzok6'
# https://wordsapiv1.p.mashape.com/words/example/definitions
# test_file_object = open('/Users/bradygroharing/DatRedditBoi/wordlists/testWords.txt', 'U')
file_object  = open('/Users/bradygroharing/DatRedditBoi/wordlist/google-10000-english-usa-no-swears-short.txt', 'r')
write_file = open('/Users/bradygroharing/DatRedditBoi/wordlist/shortWords.txt', 'w')
error_file = open('/Users/bradygroharing/DatRedditBoi/wordlist/shortErrors.txt', 'w')

#
for line in file_object:
    word = line.replace(' ', '').replace('\n', '').replace('\r', '')
    response = requests.get('https://wordsapiv1.p.mashape.com/words/' + word + '?mashape-key=' + API_KEY)
    if response.status_code == 200 :
        print('success: ' + word)
        jData = json.loads(response.content)
        write_file.write(str(jData) + '\n$$')
    else :
        print('error: ' + str(response.status_code) + ' word: ' + word)
        error_file.write(word + '\n')
file_object.close()
write_file.close()
error_file.close()