import requests
import textdistance


class PuregymAPIClient():
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'PureGym/1523 CFNetwork/1312 Darwin/21.0.0'}
    authed = False
    home_gym_id = None
    gyms = None
    
    def login(self, email, pin):
        self.session = requests.session()
        data = {
            'grant_type': 'password',
            'username': email,
            'password': pin,
            'scope': 'pgcapi',
            'client_id': 'ro.client'
        }
        response = self.session.post('https://auth.puregym.com/connect/token', headers=self.headers, data=data)
        if response.status_code == 200:
            self.auth_json = response.json()
            self.authed = True
            self.headers['Authorization'] = 'Bearer '+self.auth_json['access_token']
        else:
            return response.raise_for_status()
    
    def get_list_of_gyms(self):
        if not self.authed:
            return PermissionError('Not authed: call login(email, pin)')
        response = self.session.get(f'https://capi.puregym.com/api/v1/gyms/', headers=self.headers)
        if response.status_code == 200:
            self.gyms = {i['name'].replace(' ', '').replace('-', '').lower(): i['id'] for i in response.json()}
        else:
            return ValueError('Response '+str(response.status_code))
    
    def get_gym(self, gym_name):
        """returns corrected gym name and its ID"""
        gym_name = gym_name.replace(' ', '').replace('-', '').lower()
        if self.gyms is None:
            self.get_list_of_gyms()
        return max(list(self.gyms.items()), key=lambda x: textdistance.levenshtein.similarity(gym_name, x[0]))

    def get_home_gym(self):
        if not self.authed:
            return PermissionError('Not authed: call login(email, pin)')

        response = self.session.get('https://capi.puregym.com/api/v1/member', headers=self.headers)
        if response.status_code == 200:
            self.home_gym_id = response.json()['homeGymId']
        else:
            return ValueError('Response '+str(response.status_code))
    
    def get_gym_attendance(self, gym, return_name=False):
        if not self.authed:
            return PermissionError('Not authed: call login(email, pin)')
        if gym is None:
            if self.home_gym_id is None:
                self.get_home_gym()
            gym_id = self.home_gym_id
        elif isinstance(gym, int):
            gym_id = gym
            gym = None
        else:
            gym, gym_id = self.get_gym(gym)  # name->id
        response = self.session.get(f'https://capi.puregym.com/api/v1/gyms/{gym_id}/attendance', headers=self.headers)
        if response.status_code == 200:
            n = response.json()['totalPeopleInGym']
            if return_name:
                return n, gym
            return n
        else:
            return response.raise_for_status()

    def get_member_activity(self):
        if not self.authed:
            return PermissionError("Not authed: call login(email, pin)")

        response = self.session.get("https://capi.puregym.com/api/v1/member/activity", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return ValueError("Response " + str(response.status_code))


GYM_DICT ={
    "aberdeenkittybrewster": 69,
    "aberdeenrubislaw": 206,
    "aberdeenshiprow": 12,
    "aberdeenwellingtoncircle": 195,
    "aintree": 91,
    "airdrie": 395,
    "aldershotwestgateretailpark": 304,
    "alloa": 335,
    "altrincham": 223,
    "andover": 268,
    "ashfordwarrenretailpark": 303,
    "ashtonunderlyne": 83,
    "aylesbury": 281,
    "ballymena": 365,
    "banburycrossretailpark": 175,
    "bangornorthernireland": 171,
    "bangorwales": 336,
    "barnsley": 421,
    "barnstaple": 264,
    "basildon": 242,
    "bathspringwharf": 277,
    "bathvictoriapark": 323,
    "bedfordheights": 84,
    "belfastadelaidestreet": 224,
    "belfastboucherroad": 80,
    "belfaststanne'ssquare": 8,
    "bicester": 288,
    "billericay": 88,
    "birminghamarcadiancentre": 211,
    "birminghambeaufortpark": 190,
    "birminghamcitycentre": 10,
    "birminghamlongbridge": 213,
    "birminghammaypole": 202,
    "birminghamsnowhillplaza": 139,
    "birminghamwest": 7,
    "bishopauckland": 422,
    "blackburnthemall": 160,
    "bletchley": 245,
    "blyth": 356,
    "borehamwood": 68,
    "boston": 354,
    "bournemouthmallardroadretailpark": 307,
    "bournemouththetriangle": 21,
    "bracknell": 306,
    "bradfordidle": 92,
    "bradfordthornbury": 70,
    "bridgwater": 227,
    "brierleyhill": 114,
    "brightoncentral": 82,
    "brightonlondonroad": 205,
    "bristolabbeywoodretailpark": 265,
    "bristolbarrowroad": 178,
    "bristolbrislington": 209,
    "bristoleastgate": 333,
    "bristolharbourside": 53,
    "bristoluniongate": 79,
    "broadstairswestwoodgatewayretailpark": 342,
    "bromborough": 291,
    "bromsgroveretailpark": 262,
    "buckingham": 210,
    "burgesshill": 273,
    "burnham": 126,
    "bury": 198,
    "byfleet": 379,
    "caerphilly": 373,
    "camberley": 182,
    "cambridgegraftoncentre": 207,
    "cambridgeleisurepark": 99,
    "cannockorbitalretailpark": 380,
    "canterburysturryroad": 185,
    "canterburywincheap": 298,
    "cardiffbay": 230,
    "cardiffcentral": 22,
    "cardiffgate": 180,
    "cardiffwesternavenue": 315,
    "chatham": 48,
    "chelmsfordmeadows": 219,
    "cheshuntbrookfieldshoppingpark": 327,
    "chester": 183,
    "chippenham": 328,
    "cirencesterretailpark": 311,
    "coalville": 423,
    "colchesterretailpark": 272,
    "coleraine": 381,
    "colne": 159,
    "consett": 362,
    "corby": 228,
    "coventrybishopstreet": 74,
    "coventryskydome": 24,
    "coventrywarwickshireshoppingpark": 166,
    "crayford": 287,
    "crewegrandjunctionretailpark": 324,
    "dagenham": 407,
    "denton": 72,
    "derbycitycentre": 101,
    "derbykingswayretailpark": 404,
    "derrylondonderry": 103,
    "dewsbury": 414,
    "didcot": 261,
    "doncaster": 372,
    "dover": 382,
    "dudleytipton": 140,
    "dumfries": 348,
    "dundee": 29,
    "dunfermline": 193,
    "durhamarnison": 343,
    "durhamcityretailpark": 415,
    "eastgrinstead": 216,
    "eastkilbride": 23,
    "eastbourne": 383,
    "edinburghcraigleithretailpark": 317,
    "edinburghexchangecrescent": 176,
    "edinburghfortkinnaird": 203,
    "edinburghoceanterminal": 16,
    "edinburghquartermile": 4,
    "edinburghwaterfront": 144,
    "edinburghwest": 36,
    "elgin": 386,
    "epsom": 59,
    "evesham": 284,
    "exeterbishopscourt": 266,
    "exeterforestreet": 208,
    "falkirk": 384,
    "fareham": 217,
    "folkestone": 254,
    "galashiels": 360,
    "gateshead": 27,
    "glasgowbathstreet": 6,
    "glasgowcharingcross": 61,
    "glasgowclydebank": 152,
    "glasgowgiffnock": 357,
    "glasgowhopestreet": 157,
    "glasgowmilngavie": 397,
    "glasgowrobroyston": 25,
    "glasgowshawlands": 31,
    "glasgowsilverburn": 197,
    "glossop": 279,
    "gloucesterquedgeley": 302,
    "gloucesterretailpark": 137,
    "granthamdiscoveryretailpark": 321,
    "gravesend": 258,
    "greatyarmouth": 349,
    "grimsby": 45,
    "halifax": 28,
    "harlow": 66,
    "harrogate": 32,
    "hatfield": 396,
    "haverhill": 276,
    "haywardsheath": 359,
    "heanor": 370,
    "hednesfordcannock": 220,
    "hemelhempstead": 269,
    "henley": 154,
    "hereford": 249,
    "hitchin": 235,
    "hullanlaby": 204,
    "invernessinshesretailpark": 316,
    "ipswichbuttermarket": 163,
    "ipswichravenswood": 376,
    "kettering": 391,
    "kirkby": 363,
    "kirkcaldy": 290,
    "knaresborough": 355,
    "leamingtonspa": 270,
    "leedsbramley": 38,
    "leedscitycentrenorth": 57,
    "leedscitycentresouth": 3,
    "leedshunslet": 221,
    "leedskirkstallbridge": 40,
    "leedsregentstreet": 42,
    "leedsthorpepark": 201,
    "leicesterstgeorgesway": 156,
    "leicesterwalnutstreet": 17,
    "lichfield": 244,
    "lincolncarltoncentre": 350,
    "lincolnstmarkscentre": 44,
    "linlithgow": 364,
    "lisburnlaganbank": 173,
    "liverpoolbrunswick": 174,
    "liverpoolcentral": 96,
    "liverpooledgelane": 387,
    "livingston": 81,
    "llantrisant": 409,
    "londonacton": 172,
    "londonaldgate": 147,
    "londonangel": 283,
    "londonbank": 286,
    "londonbayswater": 130,
    "londonbeckton": 229,
    "londonbermondsey": 46,
    "londonborough": 232,
    "londonbowwharf": 231,
    "londonbromley": 169,
    "londoncamberwellnewroad": 161,
    "londoncamberwellsouthamptonway": 257,
    "londoncamden": 236,
    "londoncanarywharf": 110,
    "londoncatfordrusheygreen": 339,
    "londoncharlton": 168,
    "londonclapham": 241,
    "londoncolindale": 51,
    "londoncolney": 403,
    "londoncoventgarden": 239,
    "londoncrouchend": 297,
    "londoncroydon": 196,
    "londonearlscourt": 237,
    "londoneastindiadock": 212,
    "londoneastsheen": 252,
    "londonedgware": 113,
    "londonenfield": 87,
    "londonfarringdon": 240,
    "londonfeltham": 385,
    "londonfinchley": 134,
    "londonfinsburypark": 89,
    "londonfulham": 248,
    "londongreatportlandstreet": 106,
    "londongreenwich": 26,
    "londongreenwichmovement": 49,
    "londonhammersmithpalais": 95,
    "londonhayes": 253,
    "londonholborn": 107,
    "londonhollowayroad": 112,
    "londonhoxton": 314,
    "londonilford": 60,
    "londonkentishtown": 127,
    "londonkidbrookevillage": 275,
    "londonkingston": 406,
    "londonlambeth": 109,
    "londonlewisham": 222,
    "londonleytonstone": 289,
    "londonlimehouse": 187,
    "londonmarylebone": 135,
    "londonmonument": 296,
    "londonmuswellhill": 118,
    "londonnorthfinchley": 13,
    "londonorpingtoncentral": 50,
    "londonoval": 19,
    "londonpalmersgreen": 347,
    "londonparkroyal": 188,
    "londonpiccadilly": 119,
    "londonputney": 62,
    "londonsevensisters": 405,
    "londonshoreditchhighstreet": 150,
    "londonsidcup": 358,
    "londonsouthkensington": 123,
    "londonsouthgate": 128,
    "londonstpauls": 129,
    "londonstratford": 332,
    "londonstreatham": 329,
    "londonswisscottage": 341,
    "londonsydenham": 120,
    "londontottenhamcourtroad": 214,
    "londontowerhill": 233,
    "londontwickenham": 308,
    "londonvictoria": 148,
    "londonwall": 141,
    "londonwandsworth": 15,
    "londonwaterloo": 238,
    "londonwembley": 85,
    "londonwhitechapel": 234,
    "londonwimbledon": 389,
    "londonwoolwich": 345,
    "loughborough": 125,
    "lutonanddunstable": 111,
    "macclesfieldsilkroad": 325,
    "maidenhead": 368,
    "maidstonethemall": 309,
    "maldonblackwaterretailpark": 271,
    "manchesterburynewroad": 215,
    "manchestercheethamhillretailpark": 326,
    "manchesterdebdale": 186,
    "manchestereccles": 167,
    "manchesterexchangequay": 71,
    "manchesterfirststreet": 366,
    "manchestermarketstreet": 162,
    "manchestermoston": 63,
    "manchesterspinningfields": 1,
    "manchesterstretford": 52,
    "manchesterurbanexchange": 20,
    "mansfield": 65,
    "merthyrtydfil": 392,
    "miltonkeyneskingstoncentre": 319,
    "miltonkeyneswinterhill": 39,
    "motherwell": 76,
    "newbarnet": 117,
    "newbury": 322,
    "newcastleeldongarden": 115,
    "newcastlelongbenton": 54,
    "newcastlestjames": 191,
    "newportwales": 11,
    "newry": 177,
    "newtownabbey": 93,
    "northallerton": 338,
    "northamptoncentral": 43,
    "northamptonwestonfavell": 260,
    "northolt": 124,
    "northwich": 121,
    "norwichaylshamroad": 251,
    "norwichcastlemall": 259,
    "norwichriverside": 293,
    "nottinghambasford": 34,
    "nottinghambeeston": 94,
    "nottinghamcastlemarina": 243,
    "nottinghamcolwick": 402,
    "nottinghamwestbridgford": 330,
    "nuneaton": 179,
    "oldham": 142,
    "ormskirk": 346,
    "oxfordcentral": 131,
    "oxfordtemplarsshoppingpark": 158,
    "paisley": 143,
    "peterboroughbrotherhoodretailpark": 331,
    "peterboroughserpentinegreenshoppingcentre": 352,
    "plymouthalexandraroad": 55,
    "plymouthmarshmills": 267,
    "poole": 98,
    "porttalbot": 401,
    "portishead": 334,
    "portsmouthcommercialroad": 33,
    "portsmouthnorthharbour": 181,
    "preston": 56,
    "purley": 151,
    "rayleigh": 278,
    "readingbasingstokeroad": 58,
    "readingcalcot": 301,
    "readingcavershamroad": 97,
    "redditch": 138,
    "redditchringway": 399,
    "rochdale": 116,
    "romford": 280,
    "runcorn": 184,
    "rushden": 378,
    "saffronwalden": 255,
    "salford": 86,
    "salisbury": 256,
    "selby": 410,
    "sevenoaks": 351,
    "sheffieldcitycentresouth": 5,
    "sheffieldcrystalpeaks": 393,
    "sheffieldmeadowhallretailpark": 353,
    "sheffieldmillhouses": 75,
    "sheffieldnorth": 73,
    "shrewsburymeolebrace": 398,
    "sittingbourne": 416,
    "solihullsearsretailpark": 320,
    "southruislip": 411,
    "southamptonbitterne": 9,
    "southamptoncentral": 146,
    "southamptonshirley": 108,
    "southendfossettspark": 247,
    "southport": 388,
    "stalbans": 274,
    "stivescambridgeshire": 377,
    "stafford": 155,
    "staines": 64,
    "stevenage": 246,
    "stirling": 102,
    "stockportnorth": 299,
    "stockportsouth": 47,
    "stokeontrenteast": 67,
    "stokeontrentnorth": 18,
    "stowmarket": 312,
    "stratforduponavon": 367,
    "sunderland": 170,
    "suttoncoldfield": 122,
    "suttontimessquare": 164,
    "swindonmanningtonretailpark": 218,
    "swindonstratton": 292,
    "tamworth": 394,
    "taunton": 344,
    "telford": 226,
    "tonbridge": 199,
    "torquaybridgeretailpark": 313,
    "trowbridge": 340,
    "tunbridgewells": 104,
    "tyldesley": 337,
    "uttoxeter": 369,
    "wakefield": 90,
    "walsall": 35,
    "walsallcrownwharf": 361,
    "waltononthames": 30,
    "warringtoncentral": 77,
    "warringtonnorth": 14,
    "waterlooville": 294,
    "watfordwaterfieldsretailpark": 400,
    "westbromwich": 37,
    "westthurrock": 165,
    "westonsupermare": 263,
    "widnes": 225,
    "wirralbidstonmoss": 194,
    "wisbech": 295,
    "witney": 310,
    "woking": 105,
    "wolverhamptonbentleybridge": 2,
    "wolverhamptonsouth": 41,
    "worcester": 200,
    "wrexham": 78,
    "yate": 371,
    "yeovilhoundstoneretailpark": 318,
    "york": 132
  }

GYM_IDS = [339, 286, 296, 168, 120, 222, 129]
def run_server(client: PuregymAPIClient):
    import time
    import sys
    import os
    import logging


    run = True

    logging.basicConfig(filename="logs_"+time.strftime("%Y%m%d-%H%M%S"),
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

    logging.info("Scraping data")

    logger = logging.getLogger('PUREGYM_SCRAPER')

    HEADER="time,"+",".join(map(str, GYM_IDS))
    logger.info(HEADER)

    while run:
        try:
            all_attendance = [str(client.get_gym_attendance(gym_id)) for gym_id in GYM_IDS]
            logline = ",".join(all_attendance)
            logger.info(logline)

            time.sleep(270)
        except KeyboardInterrupt:
            print('Killing program')
            try:
                sys.exit(130)
            except SystemExit:
                os._exit(130)



if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('email')
    parser.add_argument('pin')
    parser.add_argument('--gym', default=None)
    args = parser.parse_args()
    
    client = PuregymAPIClient()
    client.login(args.email, args.pin)

    # print(client.get_gym_attendance(args.gym))
    # print(client.get_member_activity()) # {'totalDuration': 501, 'averageDuration': 55, 'totalVisits': 9, 'totalClasses': 0, 'isEstimated': False, 'lastRefreshed': '2024-02-19T00:03:30.0456427Z'}

    run_server(client=client)