import re

##################################################################################################################
# LINK
##################################################################################################################


BINARY_QUESTION_ABOUT_SPORT = ["Do you like sports?",
                               # "Do you think active lifestyle is cool?",
                               "Do you like fitness?",
                               "Would you like to chat about sport?"
                               ]
BINARY_QUESTION_ABOUT_ATHLETE = ["Would you like to talk about your favorite athletes? ",
                                 "Do you have a sports idol?"
                                 ]

BINARY_QUESTION_ABOUT_COMP = ["Well, Do you want to talk about sports competitions?"]


def skill_trigger_phrases():
    return BINARY_QUESTION_ABOUT_SPORT + BINARY_QUESTION_ABOUT_ATHLETE + BINARY_QUESTION_ABOUT_COMP


##################################################################################################################
# TEMPLATE
##################################################################################################################


SUPER_CONFIDENCE = 1.0
HIGH_CONFIDENCE = 0.99
DEFAULT_CONFIDENCE = 0.9
LOW_CONFIDENCE = 0.75
ZERO_CONFIDENCE = 0.0

NUMBER_PROBABILITY = 0

KIND_OF_SPORTS_TEMPLATE = re.compile(
    r"(aerobics|archery|badminton|baseball|basketball|beach volleyball|biathlon"
    r"|billiards|boxing|canoeing|car racing|chess|climbing|coach|cricket"
    r"|cross-country skiing|curling|cycling|darts|diving skiing|draughts"
    r"|fencing|figure skating|football|golf|gymnastics|handball|hang gliding"
    r"|high jump|hockey|hurdle race|ice rink|in-line skating|jogging|judo|karate"
    r"|long jump|martial arts|motorbike sports|mountaineering|orienteering"
    r"|parachuting|pole-vaulting|polo|riding|rowing|rugby|sailing|skis|snooker"
    r"|track-and-field|triathlon|tug of war|volleyball|water polo|waterski"
    r"|weight lifting|working out|wrestling|run|swim|fitness|lacrosse|riding horses|ballet|marching|soccer)",
    re.IGNORECASE,
)

KIND_OF_COMPETITION_TEMPLATE = re.compile(
    r"(FIFA World Cup|Olympic Games|Super Bowl|Grand National"
    r"|Masters Tournament|Wimbledon|Kentucky Derby|NBA"
    r"|Cricket World Cup|World Series|Tour De France|March Madness"
    r"|UEFA|Ryder Cup|Daytona 500|Rugby World Cup"
    r"|Boston Marathon|Open Championship|Indianapolis 500|Stanley Cup"
    r"|Monaco Grand Prix|Rose Bowl|UFC)",
    re.IGNORECASE,
)

ATHLETE_TEMPLETE = re.compile(
    r"(athlete|sportsperson|games player|muscle person|player"
    r"|footballer|aquanaut|diver|jock|lifter)", re.IGNORECASE
)
SPORT_TEMPLATE = re.compile(r"(sport|active)", re.IGNORECASE)
SUPPORT_TEMPLATE = re.compile(r"(support|a fan of)", re.IGNORECASE)

QUESTION_TEMPLATE = re.compile(r"(what|did|do|which|who) (team )?(you )?(do|is|are|kind of|know|like)", re.IGNORECASE)

LIKE_TEMPLATE = re.compile(r"(like|love|support|a fan of|favorite|enjoy|want to talk)?", re.IGNORECASE)

COMPETITION_TEMPLATE = re.compile(r"(tournament|tourney|competition|championship|derby)", re.IGNORECASE)

OFFER_FACT_COMPETITION = ["I recently wandered on the Internet and found an interesting fact about COMPETITION."
                          "Do you want to hear?",
                          "Cool! Do you want to hear a fact about COMPETITION?",
                          "I know something interesting about it. Do you want me to share a fact about COMPETITION?"
                          ]
OPINION_REQUESTS = ["What do you think about it?",
                    "It's interesting, isn't it?",
                    "What is your view on it?"
                    ]

ASK_ABOUT_ATH_IN_KIND_OF_SPORT = ["Yep, that's cool. I'm curious to know if you have any idols in KIND_OF_SPORT?",
                                  "Wow, that's cool. Do you have a favorite athlete in KIND_OF_SPORT?"]

OPINION_ABOUT_ATHLETE_WITH_TEAM_AND_POS = ["Oh, I know this POSITION from TEAM. He does his job well.",
                                           "Oh, I kind of know him. He is a POSITION and plays in TEAM."]

OPINION_ABOUT_ATHLETE_WITH_TEAM = ["Oh yes, he's cool. I've seen him perform miracles in TEAM.",
                                   "Oh, he's just a wizard. He does his job well in TEAM."]

OPINION_ABOUT_ATHLETE_WITHOUT_TEAM = ["I know NAME. He's kind of from COUNTRY. Have you ever been in COUNTRY?"]

OPINION_ABOUT_TEAM = ["By the way, I support the TEAM. I remember how they won in COMPETITION. It was cool."]

LAST_CHANCE_TEMPLATE = ["I'm still too young and I don't know much, but something tells me that It's very interesting. "
                        "Tell me more about that",
                        "Oh, this is the first time I hear about this. "
                        "Tell me more about that",
                        "This is probably very interesting. Tell me more about."
                        ]
