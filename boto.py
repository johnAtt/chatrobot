"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request, response
import json
import random
from profanityfilter import ProfanityFilter
from weather import Weather, Unit

pf = ProfanityFilter()
counter = 0
dict_of_list = {
    "love": ["considerate","loving","affectionate","tender","sensitive","devoted",
                "Passionate", "attracted","admiration","touched","warm","sympathy","love","close","comforted"],
    "happy": ["great","joy","lucky","fortunate","overjoyed","delighted","gleeful",
                "important", "thankful", "festive", "satisfied","happy","glad","sunny","cheerful","merry","elated","good","like"],
    "anger": ["annoyed", "apathetic", "bored", "certain", "cold", "critical", "displeased", "frustrated","impatient",
                "indifferent","irritated","peeved","rankled"],
    "business": ["services","bill","capital","cash","check","fund","pay","payment","property","salary","wage","wealth",
                 "banknote","bankroll","bucks","coin","finances","funds","gold"],
    "sadness" : [ "homesick","sad","unhappy","depression","depress","melancholy"]
}
joke_list = ["There are only 10 types of people in the world: those that understand binary and those that don’t.",
                "Computers make very fast, very accurate mistakes.",
                "Be nice to the nerds, for all you know they might be the next Bill Gates!",
                "Artificial intelligence usually beats real stupidity.",
                "How do you call a programmer from Finland ?  Nerdic....",
                "Chuck Norris write code... That optimizes itself.",
                "A programmer died in the shower, the instructions on the shampoo bottle said: Lather, Rinse, Repeat",]


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    global counter
    user_message = request.POST.get('msg')
    split_message= user_message.split()
    city = split_message[-1]
    lower_message = user_message.lower()
    if not request.get_cookie("visit"):
        counter += 1
        my_animation = "waiting"
        my_msg = "i am so happy to meet you {}, you can ask me about weather(weather + city), or even a joke".format(lower_message)
        response.set_cookie('visit', "known")
    elif counter == 0:
        counter += 1
        my_animation = "excited"
        my_msg = " i am so happy to see you again {}, you can ask me about weather, or even a joke".format(lower_message)
    elif weather_message(lower_message):
        weather = Weather(unit=Unit.CELSIUS)
        location = weather.lookup_by_location(city)
        condition = location.condition
        my_animation = "ok"
        my_msg = "the weather in {} is {}".format(city, condition.text)
    elif bad_words(lower_message):
        my_animation = "heartbroke"
        my_msg = random.choice(["you mean", 'it is how war begins', "be careful i know where you live"])
    elif good_jokes(lower_message):
        my_animation = "laughing"
        my_msg = random.choice(joke_list)
    elif any(word in lower_message for word in ['how are you doing', 'how are you', "what's up"]):
        my_animation = "giggling"
        my_msg = random.choice(["i am so fine today, what about you ?", 'Yo', "hola", "yea dude"])
    else:
        my_animation, my_msg = check_feelings(lower_message)
    return json.dumps({"animation": my_animation, "msg": my_msg})


def weather_message(lower_message):
    if any(word in lower_message for word in ['weather', 'forecast']):
        return True
    else:
        return False


def bad_words(lower_message):
    if pf.is_profane(lower_message):
        return True
    else:
        return False


def good_jokes(lower_message):
    if any(word in lower_message for word in ['joke', 'want to laugh', "make me smile", "be fun","laugh","fun"]):
        return True
    else:
        return False


def check_feelings(lower_message):
    if any(word in lower_message for word in dict_of_list["love"]):
        my_animation = "inlove"
        my_msg = random.choice(["i think i am falling in love with you", "what about a first date .. you and me ?"])
    elif any(word in lower_message for word in dict_of_list["happy"]):
        my_animation = "dancing"
        my_msg = random.choice(["it's so nice to see you like that", "after all you ve been through, finally you smile"])
    elif any(word in lower_message for word in dict_of_list["anger"]):
        my_animation = "crying"
        my_msg = random.choice(["you sounds so upset, i do not like that", "what can i do to make you feel better my friend?"])
    elif any(word in lower_message for word in dict_of_list["business"]):
        my_animation = "money"
        my_msg = random.choice(["can not wait for our collaboration to make us rich", "let's get richhhhhh"])
    elif any(word in lower_message for word in dict_of_list["sadness"]):
        my_animation = "dog"
        my_msg = random.choice(["i can give you a dog, you ll feel better with a friend"])
    else:
        my_animation = "confused"
        my_msg = random.choice(["mmm be more specific please", "my constructor made me really sensitive, speak to me about your feelings",
                                "ask me for a joke", "ask me about the weather in a specific city(weather+city)",
                                "can you say 'i love you'", "speak to me about money", "do you feel depress",
                                ""])
    return my_animation, my_msg


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "no", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
