import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score,confusion_matrix,f1_score
import pandas as pd
import numpy as np
import random
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from deap import creator, base, tools, algorithms
import sys
df1 = pd.read_csv("spamham.csv")
df = df1.where((pd.notnull(df1)), '')

df.loc[df["Category"] == 'ham', "Category",] = 1
df.loc[df["Category"] == 'spam', "Category",] = 0

df_x = df['Message']
df_y = df['Category']
############################################################
def avg(l):
    """
    Returns the average between list elements
    """
    return (sum(l)/float(len(l)))


def getFitness(individual, X, y):
    """
    Feature subset fitness function
    """

    if(individual.count(0) != len(individual)):
        # get index with value 0
        cols = [index for index in range(
            len(individual)) if individual[index] == 0]

        # get features subset
        X_parsed = X
        X_subset = pd.get_dummies(X_parsed)

        # apply classification algorithm
        clf = LogisticRegression()

        return (avg(cross_val_score(clf,X_subset,y,cv=5)),)
    
return(0,0)


def geneticAlgorithm(X, y, n_population, n_generation):
    
    # create individual
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # create toolbox
    toolbox = base.Toolbox()
    toolbox.register("attr_bool", random.randint, 0, 1)
    toolbox.register("individual", tools.initRepeat,
                     creator.Individual, toolbox.attr_bool, len(X))
    toolbox.register("population", tools.initRepeat, list,
                     toolbox.individual)
    toolbox.register("evaluate", getFitness, X=X, y=y)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    # initialize parameters
    pop = toolbox.population(n=n_population)
    hof = tools.HallOfFame(n_population * n_generation)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)

    # genetic algorithm
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2,
                                   ngen=n_generation, stats=stats, halloffame=hof,
                                   verbose=True)

    # return hall of fame
    return hof


def bestIndividual(hof, X, y):
    
    maxAccurcy = 0.0
    for individual in hof:
        if(individual.fitness.values > maxAccurcy):
            maxAccurcy = individual.fitness.values
            _individual = individual

    _individualHeader = [list(X)[i] for i in range(
        len(_individual)) if _individual[i] == 1]
    return _individual.fitness.values, _individual, _individualHeader


def getArguments():
    dfPath = 'spamham.csv'
    pop = 10
    gen = 2
    return dfPath, pop, gen

dataframePath, n_pop, n_gen = getArguments()
y = df_y
X = df_x
individual = [1 for i in range(len(X))]
hof = geneticAlgorithm(X, y, n_pop, n_gen)
print('Individual: \t\t' + str(individual))
############################################################
x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, train_size=0.8, test_size=0.2, random_state=4)


tfvec = TfidfVectorizer(min_df=1, stop_words='english', lowercase=True)
x_trainFeat = tfvec.fit_transform(x_train)
x_testFeat = tfvec.transform(x_test)


y_trainSvm = y_train.astype('int')
classifierModel = LinearSVC()
classifierModel.fit(x_trainFeat, y_trainSvm)
predResult = classifierModel.predict(x_testFeat)


y_trainGnb = y_train.astype('int')
classifierModel2 = MultinomialNB()
classifierModel2.fit(x_trainFeat, y_trainGnb)
predResult2 = classifierModel2.predict(x_testFeat)


y_test = y_test.astype('int')
actual_Y = y_test.as_matrix()

print("~~~~~~~~~~SVM RESULTS~~~~~~~~~~")
print("Accuracy Score using SVM: {0:.4f}".format(accuracy_score(actual_Y, predResult)*100))
print("F Score using SVM: {0: .4f}".format(f1_score(actual_Y, predResult, average='macro')*100))
cmSVM=confusion_matrix(actual_Y, predResult)
print("Confusion matrix using SVM:")
print(cmSVM)
print("~~~~~~~~~~MNB RESULTS~~~~~~~~~~")
print("Accuracy Score using MNB: {0:.4f}".format(accuracy_score(actual_Y, predResult2)*100))
print("F Score using MNB:{0: .4f}".format(f1_score(actual_Y, predResult2, average='macro')*100))
cmMNb=confusion_matrix(actual_Y, predResult2)
print("Confusion matrix using MNB:")
print(cmMNb)
######################################################3
import sys
import time

try:
    from nltk import wordpunct_tokenize
    from nltk.corpus import stopwords
except ImportError:
    print('[!] You need to install nltk (http://nltk.org/index.html)')

def calculate_languages_ratios(text):
    languages_ratios = {}
    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]

    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)

        languages_ratios[language] = len(common_elements) # language "score"

    return languages_ratios

def detect_language(text):
    ratios = calculate_languages_ratios(text)
    most_rated_language = max(ratios, key=ratios.get)
    return most_rated_language

def load_bad_words():
    badwords_list=[]
    lang_file = open('english.csv','rb')
    for word in lang_file:
        badwords_list.append(word.lower().strip('\n'))
    return badwords_list

def load_file(filename):
	file=open(filename,'rb')
	return file

text = input('enter english text here....')
print('-----------------Input Text-----------------')
print(text)
print('--------------------------------------------\n')

language = detect_language(text)
print('\n')
time.sleep(1)

time.sleep(1)
print('Checking for bad words in '+language.upper()+' language...')
print( '**********************************************************\n')

#badwords = load_bad_words()
badwords = ["abbo",
"abo",
"abortion",
"abuse",
"addict",
"addicts",
"adult",
"africa",
"african",
"alla",
"allah",
"alligatorbait",
"amateur",
"american",
"anal",
"analannie",
"analsex",
"angie",
"angry",
"anus",
"arab",
"arabs",
"areola",
"argie",
"aroused",
"arse",
"arsehole",
"asian",
"ass",
"assassin",
"assassinate",
"assassination",
"assault",
"assbagger",
"assblaster",
"assclown",
"asscowboy",
"asses",
"assfuck",
"assfucker",
"asshat",
"asshole",
"assholes",
"asshore",
"assjockey",
"asskiss",
"asskisser",
"assklown",
"asslick",
"asslicker",
"asslover",
"assman",
"assmonkey",
"assmunch",
"assmuncher",
"asspacker",
"asspirate",
"asspuppies",
"assranger",
"asswhore",
"asswipe",
"athletesfoot",
"attack",
"australian",
"babe",
"babies",
"backdoor",
"backdoorman",
"backseat",
"badfuck",
"balllicker",
"balls",
"ballsack",
"banging",
"baptist",
"barelylegal",
"barf",
"barface",
"barfface",
"bast",
"bastard",
"bazongas",
"bazooms",
"beaner",
"beast",
"beastality",
"beastial",
"beastiality",
"beatoff",
"beat-off",
"beatyourmeat",
"beaver",
"bestial",
"bestiality",
"bi",
"biatch",
"bible",
"bicurious",
"bigass",
"bigbastard",
"bigbutt",
"bigger",
"bisexual",
"bi-sexual",
"bitch",
"bitcher",
"bitches",
"bitchez",
"bitchin",
"bitching",
"bitchslap",
"bitchy",
"biteme",
"black",
"blackman",
"blackout",
"blacks",
"blind",
"blow",
"blowjob",
"boang",
"bogan",
"bohunk",
"bollick",
"bollock",
"bomb",
"bombers",
"bombing",
"bombs",
"bomd",
"bondage",
"boner",
"bong",
"boob",
"boobies",
"boobs",
"booby",
"boody",
"boom",
"boong",
"boonga",
"boonie",
"booty",
"bootycall",
"bountybar",
"bra",
"brea5t",
"breast",
"breastjob",
"breastlover",
"breastman",
"brothel",
"bugger",
"buggered",
"buggery",
"bullcrap",
"bulldike",
"bulldyke",
"bullshit",
"bumblefuck",
"bumfuck",
"bunga",
"bunghole",
"buried",
"burn",
"butchbabes",
"butchdike",
"butchdyke",
"butt",
"buttbang",
"butt-bang",
"buttface",
"buttfuck",
"butt-fuck",
"buttfucker",
"butt-fucker",
"buttfuckers",
"butt-fuckers",
"butthead",
"buttman",
"buttmunch",
"buttmuncher",
"buttpirate",
"buttplug",
"buttstain",
"byatch",
"cacker",
"cameljockey",
"cameltoe",
"canadian",
"cancer",
"carpetmuncher",
"carruth",
"catholic",
"catholics",
"cemetery",
"chav",
"cherrypopper",
"chickslick",
"children's",
"chin",
"chinaman",
"chinamen",
"chinese",
"chink",
"chinky",
"choad",
"chode",
"christ",
"christian",
"church",
"cigarette",
"cigs",
"clamdigger",
"clamdiver",
"clit",
"clitoris",
"clogwog",
"cocaine",
"cock",
"cockblock",
"cockblocker",
"cockcowboy",
"cockfight",
"cockhead",
"cockknob",
"cocklicker",
"cocklover",
"cocknob",
"cockqueen",
"cockrider",
"cocksman",
"cocksmith",
"cocksmoker",
"cocksucer",
"cocksuck",
"cocksucked",
"cocksucker",
"cocksucking",
"cocktail",
"cocktease",
"cocky",
"cohee",
"coitus",
"color",
"colored",
"coloured",
"commie",
"communist",
"condom",
"conservative",
"conspiracy",
"coolie",
"cooly",
"coon",
"coondog",
"copulate",
"cornhole",
"corruption",
"cra5h",
"crabs",
"crack",
"crackpipe",
"crackwhore",
"crack-whore",
"crap",
"crapola",
"crapper",
"crappy",
"crash",
"creamy",
"crime",
"crimes",
"criminal",
"criminals",
"crotch",
"crotchjockey",
"crotchmonkey",
"crotchrot",
"cum",
"cumbubble",
"cumfest",
"cumjockey",
"cumm",
"cummer",
"cumming",
"cumquat",
"cumqueen",
"cumshot",
"cunilingus",
"cunillingus",
"cunn",
"cunnilingus",
"cunntt",
"cunt",
"cunteyed",
"cuntfuck",
"cuntfucker",
"cuntlick",
"cuntlicker",
"cuntlicking",
"cuntsucker",
"cybersex",
"cyberslimer",
"dago",
"dahmer",
"dammit",
"damn",
"damnation",
"damnit",
"darkie",
"darky",
"datnigga",
"dead",
"deapthroat",
"death",
"deepthroat",
"defecate",
"dego",
"demon",
"deposit",
"desire",
"destroy",
"deth",
"devil",
"devilworshipper",
"dick",
"dickbrain",
"dickforbrains",
"dickhead",
"dickless",
"dicklick",
"dicklicker",
"dickman",
"dickwad",
"dickweed",
"diddle",
"die",
"died",
"dies",
"dike",
"dildo",
"dingleberry",
"dink",
"dipshit",
"dipstick",
"dirty",
"disease",
"diseases",
"disturbed",
"dive",
"dix",
"dixiedike",
"dixiedyke",
"doggiestyle",
"doggystyle",
"dong",
"doodoo",
"doo-doo",
"doom",
"dope",
"dragqueen",
"dragqween",
"dripdick",
"drug",
"drunk",
"drunken",
"dumb",
"dumbass",
"dumbbitch",
"dumbfuck",
"dyefly",
"dyke",
"easyslut",
"eatballs",
"eatme",
"eatpussy",
"ecstacy",
"ejaculate",
"ejaculated",
"ejaculating",
"ejaculation",
"enema",
"enemy",
"erect",
"erection",
"ero",
"escort",
"ethiopian",
"ethnic",
"european",
"evl",
"excrement",
"execute",
"executed",
"execution",
"executioner",
"explosion",
"facefucker",
"faeces",
"fag",
"fagging",
"faggot",
"fagot",
"failed",
"failure",
"fairies",
"fairy",
"faith",
"fannyfucker",
"fart",
"farted",
"farting",
"farty",
"fastfuck",
"fat",
"fatah",
"fatass",
"fatfuck",
"fatfucker",
"fatso",
"fckcum",
"fear",
"feces",
"felatio",
"felch",
"felcher",
"felching",
"fellatio",
"feltch",
"feltcher",
"feltching",
"fetish",
"fight",
"filipina",
"filipino",
"fingerfood",
"fingerfuck",
"fingerfucked",
"fingerfucker",
"fingerfuckers",
"fingerfucking",
"fire",
"firing",
"fister",
"fistfuck",
"fistfucked",
"fistfucker",
"fistfucking",
"fisting",
"flange",
"flasher",
"flatulence",
"floo",
"flydie",
"flydye",
"fok",
"fondle",
"footaction",
"footfuck",
"footfucker",
"footlicker",
"footstar",
"fore",
"foreskin",
"forni",
"fornicate",
"foursome",
"fourtwenty",
"fraud",
"freakfuck",
"freakyfucker",
"freefuck",
"fu",
"fubar",
"fuc",
"fucck",
"fuck",
"fucks",
"fucka",
"fuckable",
"fuckbag",
"fuckbuddy",
"fucked",
"fuckedup",
"fucker",
"fuckers",
"fuckface",
"fuckfest",
"fuckfreak",
"fuckfriend",
"fuckhead",
"fuckher",
"fuckin",
"fuckina",
"fucking",
"fuckingbitch",
"fuckinnuts",
"fuckinright",
"fuckit",
"fuckknob",
"fuckme",
"fuckmehard",
"fuckmonkey",
"fuckoff",
"fuckpig",
"fucks",
"fucktard",
"fuckwhore",
"fuckyou",
"fudgepacker",
"fugly",
"fuk",
"fuks",
"funeral",
"funfuck",
"fungus",
"fuuck",
"gangbang",
"gangbanged",
"gangbanger",
"gangsta",
"gatorbait",
"gay",
"gaymuthafuckinwhore",
"gaysex",
"geez",
"geezer",
"geni",
"genital",
"german",
"getiton",
"gin",
"ginzo",
"gipp",
"girls",
"givehead",
"glazeddonut",
"gob",
"god",
"godammit",
"goddamit",
"goddammit",
"goddamn",
"goddamned",
"goddamnes",
"goddamnit",
"goddamnmuthafucker",
"goldenshower",
"gonorrehea",
"gonzagas",
"gook",
"gotohell",
"goy",
"goyim",
"greaseball",
"gringo",
"groe",
"gross",
"grostulation",
"gubba",
"gummer",
"gun",
"gyp",
"gypo",
"gypp",
"gyppie",
"gyppo",
"gyppy",
"hamas",
"handjob",
"hapa",
"hate",
"harder",
"hardon",
"harem",
"headfuck",
"headlights",
"hebe",
"heeb",
"hell",
"henhouse",
"heroin",
"herpes",
"heterosexual",
"hijack",
"hijacker",
"hijacking",
"hillbillies",
"hindoo",
"hiscock",
"hitler",
"hitlerism",
"hitlerist",
"hiv",
"ho",
"hobo",
"hodgie",
"hoes",
"hole",
"holestuffer",
"homicide",
"homo",
"homobangers",
"homosexual",
"honger",
"honk",
"honkers",
"honkey",
"honky",
"hook",
"hooker",
"hookers",
"hooters",
"hore",
"hork",
"horn",
"horney",
"horniest",
"horny",
"horseshit",
"hosejob",
"hoser",
"hostage",
"hotdamn",
"hotpussy",
"hottotrot",
"hummer",
"husky",
"hussy",
"hustler",
"hymen",
"hymie",
"iblowu",
"idiot",
"ikey",
"illegal",
"incest",
"insest",
"intercourse",
"interracial",
"intheass",
"inthebuff",
"israel",
"israeli",
"israel's",
"italiano",
"itch",
"jackass",
"jackoff",
"jackshit",
"jacktheripper",
"jade",
"jap",
"japanese",
"japcrap",
"jebus",
"jeez",
"jerkoff",
"jesus",
"jesuschrist",
"jew",
"jewish",
"jiga",
"jigaboo",
"jigg",
"jigga",
"jiggabo",
"jigger",
"jiggy",
"jihad",
"jijjiboo",
"jimfish",
"jism",
"jiz",
"jizim",
"jizjuice",
"jizm",
"jizz",
"jizzim",
"jizzum",
"joint",
"juggalo",
"jugs",
"junglebunny",
"kaffer",
"kaffir",
"kaffre",
"kafir",
"kanake",
"kid",
"kigger",
"kike",
"kill",
"killed",
"killer",
"killing",
"kills",
"kink",
"kinky",
"kissass",
"kkk",
"knife",
"knockers",
"kock",
"kondum",
"koon",
"kotex",
"krap",
"krappy",
"kraut",
"kum",
"kumbubble",
"kumbullbe",
"kummer",
"kumming",
"kumquat",
"kums",
"kunilingus",
"kunnilingus",
"kunt",
"ky",
"kyke",
"lactate",
"laid",
"lapdance",
"latin",
"lesbain",
"lesbayn",
"lesbian",
"lesbin",
"lesbo",
"lez",
"lezbe",
"lezbefriends",
"lezbo",
"lezz",
"lezzo",
"liberal",
"libido",
"licker",
"lickme",
"lies",
"limey",
"limpdick",
"limy",
"lingerie",
"liquor",
"livesex",
"loadedgun",
"lolita",
"looser",
"loser",
"lotion",
"lovebone",
"lovegoo",
"lovegun",
"lovejuice",
"lovemuscle",
"lovepistol",
"loverocket",
"lowlife",
"lsd",
"lubejob",
"lucifer",
"luckycammeltoe",
"lugan",
"lynch",
"macaca",
"mad",
"mafia",
"magicwand",
"mams",
"manhater",
"manpaste",
"marijuana",
"mastabate",
"mastabater",
"masterbate",
"masterblaster",
"mastrabator",
"masturbate",
"masturbating",
"mattressprincess",
"meatbeatter",
"meatrack",
"meth",
"mexican",
"mgger",
"mggor",
"mickeyfinn",
"mideast",
"milf",
"minority",
"mockey",
"mockie",
"mocky",
"mofo",
"moky",
"moles",
"molest",
"molestation",
"molester",
"molestor",
"moneyshot",
"mooncricket",
"mormon",
"moron",
"moslem",
"mosshead",
"mothafuck",
"mothafucka",
"mothafuckaz",
"mothafucked",
"mothafucker",
"mothafuckin",
"mothafucking",
"mothafuckings",
"motherfuck",
"motherfucked",
"motherfucker",
"motherfuckin",
"motherfucking",
"motherfuckings",
"motherlovebone",
"muff",
"muffdive",
"muffdiver",
"muffindiver",
"mufflikcer",
"mulatto",
"muncher",
"munt",
"murder",
"murderer",
"muslim",
"naked",
"narcotic",
"nasty",
"nastybitch",
"nastyho",
"nastyslut",
"nastywhore",
"nazi",
"necro",
"negro",
"negroes",
"negroid",
"negro's",
"nig",
"niger",
"nigerian",
"nigerians",
"nigg",
"nigga",
"niggah",
"niggaracci",
"niggard",
"niggarded",
"niggarding",
"niggardliness",
"niggardliness's",
"niggardly",
"niggards",
"niggard's",
"niggaz",
"nigger",
"niggerhead",
"niggerhole",
"niggers",
"nigger's",
"niggle",
"niggled",
"niggles",
"niggling",
"nigglings",
"niggor",
"niggur",
"niglet",
"nignog",
"nigr",
"nigra",
"nigre",
"nip",
"nipple",
"nipplering",
"nittit",
"nlgger",
"nlggor",
"nofuckingway",
"nook",
"nookey",
"nookie",
"noonan",
"nooner",
"nude",
"nudger",
"nuke",
"nutfucker",
"nymph",
"ontherag",
"oral",
"orga",
"orgasim",
"orgasm",
"orgies",
"orgy",
"osama",
"paki",
"palesimian",
"palestinian",
"pansies",
"pansy",
"panti",
"panties",
"payo",
"pearlnecklace",
"peck",
"pecker",
"peckerwood",
"pee",
"peehole",
"pee-pee",
"peepshow",
"peepshpw",
"pendy",
"penetration",
"peni5",
"penile",
"penis",
"penises",
"penthouse",
"period",
"perv",
"phonesex",
"phuk",
"phuked",
"phuking",
"phukked",
"phukking",
"phungky",
"phuq",
"pi55",
"picaninny",
"piccaninny",
"pickaninny",
"piker",
"pikey",
"piky",
"pimp",
"pimped",
"pimper",
"pimpjuic",
"pimpjuice",
"pimpsimp",
"pindick",
"piss",
"pissed",
"pisser",
"pisses",
"pisshead",
"pissin",
"pissing",
"pissoff",
"pistol",
"pixie",
"pixy",
"playboy",
"playgirl",
"pocha",
"pocho",
"pocketpool",
"pohm",
"polack",
"pom",
"pommie",
"pommy",
"poo",
"poon",
"poontang",
"poop",
"pooper",
"pooperscooper",
"pooping",
"poorwhitetrash",
"popimp",
"porchmonkey",
"porn",
"pornflick",
"pornking",
"porno",
"pornography",
"pornprincess",
"pot",
"poverty",
"premature",
"pric",
"prick",
"prickhead",
"primetime",
"propaganda",
"pros",
"prostitute",
"protestant",
"pu55i",
"pu55y",
"pube",
"pubic",
"pubiclice",
"pud",
"pudboy",
"pudd",
"puddboy",
"puke",
"puntang",
"purinapricness",
"puss",
"pussie",
"pussies",
"pussy",
"pussycat",
"pussyeater",
"pussyfucker",
"pussylicker",
"pussylips",
"pussylover",
"pussypounder",
"pusy",
"quashie",
"queef",
"queer",
"quickie",
"quim",
"ra8s",
"rabbi",
"racial",
"racist",
"radical",
"radicals",
"raghead",
"randy",
"rape",
"raped",
"raper",
"rapist",
"rearend",
"rearentry",
"rectum",
"redlight",
"redneck",
"reefer",
"reestie",
"refugee",
"reject",
"remains",
"rentafuck",
"republican",
"rere",
"retard",
"retarded",
"ribbed",
"rigger",
"rimjob",
"rimming",
"roach",
"robber",
"roundeye",
"rump",
"russki",
"russkie",
"sadis",
"sadom",
"samckdaddy",
"sandm",
"sandnigger",
"satan",
"scag",
"scallywag",
"scat",
"schlong",
"screw",
"screwyou",
"scrotum",
"scum",
"semen",
"seppo",
"servant",
"sex",
"sexed",
"sexfarm",
"sexhound",
"sexhouse",
"sexing",
"sexkitten",
"sexpot",
"sexslave",
"sextogo",
"sextoy",
"sextoys",
"sexual",
"sexually",
"sexwhore",
"sexy",
"sexymoma",
"sexy-slim",
"shag",
"shaggin",
"shagging",
"shat",
"shav",
"shawtypimp",
"sheeney",
"shhit",
"shinola",
"shit",
"shitcan",
"shitdick",
"shite",
"shiteater",
"shited",
"shitface",
"shitfaced",
"shitfit",
"shitforbrains",
"shitfuck",
"shitfucker",
"shitfull",
"shithapens",
"shithappens",
"shithead",
"shithouse",
"shiting",
"shitlist",
"shitola",
"shitoutofluck",
"shits",
"shitstain",
"shitted",
"shitter",
"shitting",
"shitty",
"shoot",
"shooting",
"shortfuck",
"showtime",
"sick",
"sissy",
"sixsixsix",
"sixtynine",
"sixtyniner",
"skank",
"skankbitch",
"skankfuck",
"skankwhore",
"skanky",
"skankybitch",
"skankywhore",
"skinflute",
"skum",
"skumbag",
"slant",
"slanteye",
"slapper",
"slaughter",
"slav",
"slave",
"slavedriver",
"sleezebag",
"sleezeball",
"slideitin",
"slime",
"slimeball",
"slimebucket",
"slopehead",
"slopey",
"slopy",
"slut",
"sluts",
"slutt",
"slutting",
"slutty",
"slutwear",
"slutwhore",
"smack",
"smackthemonkey",
"smut",
"snatch",
"snatchpatch",
"snigger",
"sniggered",
"sniggering",
"sniggers",
"snigger's",
"sniper",
"snot",
"snowback",
"snownigger",
"sob",
"sodom",
"sodomise",
"sodomite",
"sodomize",
"sodomy",
"sonofabitch",
"sonofbitch",
"sooty",
"sos",
"soviet",
"spaghettibender",
"spaghettinigger",
"spank",
"spankthemonkey",
"sperm",
"spermacide",
"spermbag",
"spermhearder",
"spermherder",
"spic",
"spick",
"spig",
"spigotty",
"spik",
"spit",
"spitter",
"splittail",
"spooge",
"spreadeagle",
"spunk",
"spunky",
"squaw",
"stagg",
"stiffy",
"strapon",
"stringer",
"stripclub",
"stroke",
"stroking",
"stupid",
"stupidfuck",
"stupidfucker",
"suck",
"suckdick",
"sucker",
"suckme",
"suckmyass",
"suckmydick",
"suckmytit",
"suckoff",
"suicide",
"swallow",
"swallower",
"swalow",
"swastika",
"sweetness",
"syphilis",
"taboo",
"taff",
"tampon",
"tang",
"tantra",
"tarbaby",
"tard",
"teat",
"terror",
"terrorist",
"teste",
"testicle",
"testicles",
"thicklips",
"thirdeye",
"thirdleg",
"threesome",
"threeway",
"timbernigger",
"tinkle",
"tit",
"titbitnipply",
"titfuck",
"titfucker",
"titfuckin",
"titjob",
"titlicker",
"titlover",
"tits",
"tittie",
"titties",
"titty",
"tnt",
"toilet",
"tongethruster",
"tongue",
"tonguethrust",
"tonguetramp",
"tortur",
"torture",
"tosser",
"towelhead",
"trailertrash",
"tramp",
"trannie",
"tranny",
"transexual",
"transsexual",
"transvestite",
"triplex",
"trisexual",
"trojan",
"trots",
"tuckahoe",
"tunneloflove",
"turd",
"turnon",
"twat",
"twink",
"twinkie",
"twobitwhore",
"uck",
"uk",
"unfuckable",
"upskirt",
"uptheass",
"upthebutt",
"urinary",
"urinate",
"urine",
"usama",
"uterus",
"vagina",
"vaginal",
"vatican",
"vibr",
"vibrater",
"vibrator",
"vietcong",
"violence",
"virgin",
"virginbreaker",
"vomit",
"vulva",
"wab",
"wank",
"wanker",
"wanking",
"waysted",
"weapon",
"weenie",
"weewee",
"welcher",
"welfare",
"wetb",
"wetback",
"wetspot",
"whacker",
"whash",
"whigger",
"whiskey",
"whiskeydick",
"whiskydick",
"whit",
"whitenigger",
"whites",
"whitetrash",
"whitey",
"whiz",
"whop",
"whore",
"whorefucker",
"whorehouse",
"wigger",
"willie",
"williewanker",
"willy",
"wn",
"wog",
"women's",
"wop",
"wtf",
"wuss",
"wuzzie",
"xtc",
"xxx",
"yankee",
"yellowman",
"zigabo",
"zipperhead"]

text_list = text.split('\n')
for sentence in text_list:
	line_number = str(text_list.index(sentence)+1)
	for key in ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']:
		sentence = sentence.replace(key,'')
	abuses=[i for i in sentence.lower().split() if i in badwords]
	if abuses == []:
		continue
	else:
		time.sleep(0.5)
		print('-- '+str(len(abuses))+' spam Words found at line number : '+line_number+' --')
		x_words=''
		for i in abuses:
			x_words+=i+', '
		print('spam Words : '+x_words[:-2])
		print('-----------------\n')
