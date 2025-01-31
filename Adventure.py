import datetime
import math

CLASSESINORDER = {'1':'Magician','2':'Jester','3':'Bard','4':'Pirate','5':'Fae','6':'Mystic','7':'Wildshaper','8':'Cleric'}
EMOJIS = {"magician":"<:MAGE:1224412539602079925>","jester":"<:JESTER:1224412538721009715>","bard":"<:BARD:1224412499106070558>","pirate":"<:PIRATE:1224412559550189669>","fae":"<:FAE:1224412501773389987>","mystic":"<:MYSTIC:1224412558287437834>","wildshaper":"<:WILDHSHAPER:1224412540512239678>","cleric":"<:CLERIC:1224412500465025074>"}

def scaleValue(minV, maxV, percentage):
    percentage = min(100, max(0, percentage))

    return minV + (maxV - minV) * (percentage / 100)

def find_percentage(number, min_value, max_value):
    percentage = ((number - min_value) / (max_value - min_value)) * 100
    return percentage

def getEmoji(id:int):
    return "<"

def maxLevel():
    return 300

def getLimits():
    limits = [(0, 0)]
    maxLimit = 300
    for x in range(maxLimit):
        limits.append((limits[len(limits)-1][1], (((x) * 400) + 75)+(limits[len(limits)-1][1])))
    limits.remove((0, 0))
    return limits

def getLevel(expNumber):
    limits = [(0, 0)]
    maxLimit = 300
    for x in range(maxLimit):
        limits.append((limits[len(limits)-1][1], (((x) * 400) + 75)+(limits[len(limits)-1][1])))
    limits.remove((0, 0))
    res = None
    for idx, ele in enumerate(limits):
        if expNumber >= ele[0] and expNumber <= ele[1]:
            res = idx
            break
    if expNumber > max(limits[len(limits)-1]):
        return [-1, -1]
    elif expNumber < min(limits[0]):
        return [-2, -2]
    else:
        return [res, limits[res][1], limits[res][0]]
# for x in getLimits():
#    exp = x[0]
#    expLeft = x[1]-exp
#    print(math.ceil(expLeft/40))
def font(letter, fontIndex):
    ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    string = f'''{ALPHABET}\n𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ
𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ
🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉
𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙
ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ'''
    alphabets = string.splitlines()
    if letter in ALPHABET:
        tIndex = ALPHABET.index(letter)
        return alphabets[fontIndex][tIndex]
    else:
        return letter


def getClass(classIndex):
    if len(str(classIndex)) == 2:
        enchant = '(Enchanted)'
    else:
        enchant = ''
    try:
        if int(classIndex) == 0:
            return ['None Yet', '', '']
        else:
            return [CLASSESINORDER[f'{str(classIndex)[0]}'], EMOJIS[CLASSESINORDER[f'{str(classIndex)[0]}'].lower()], enchant]
    except:
        return [-1]

def timestamproundedf(plus):
    dt = datetime.datetime.now()
    timestamp = dt.replace(tzinfo=None).timestamp()
    timestamprounded = int(timestamp) + (plus)
    return timestamprounded