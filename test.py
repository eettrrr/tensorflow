import MeCab
import re
from datetime import datetime
from pykospacing import spacing

userAlias = [
    ['또띠', '또땨', '또오띠', '또오땨'],
    ['럼블', '럼브리', '럼브레'],
    ['나무', '나무니', '나문', '나문이'],
    ['몽실', '몽시리', '몽쉴'],
    ['베리', '베뤼'],
    ['우엉', '웡', '우웡'],
    ['진우', '찌누', '지누', '찐우'],
    ['전채', '쩐채', '쩌언채', '쩐체']
]
posTable = {
    'NNG': '일반_명사',
    'NNP': '고유_명사',
    'NNB': '의존_명사',
    'NNBC': '단위를_나타내는_명사',
    'NR': '수사',
    'NP': '대명사',
    'VV': '동사',
    'VA': '형용사',
    'VX': '보조_용언',
    'VCP': '긍정_지정사',
    'VCN': '부정_지정사',
    'MM': '관형사',
    'MAG': '일반_부사',
    'MAJ': '접속_부사',
    'IC': '감탄사',
    'JKS': '주격_조사',
    'JKC': '보격_조사',
    'JKG': '관형격_조사',
    'JKO': '목적격_조사',
    'JKB': '부사격_조사',
    'JKV': '호격_조사',
    'JKQ': '인용격_조사',
    'JX': '보조사',
    'JC': '접속_조사',
    'EP': '선어말_어미',
    'EF': '종결_어미',
    'EC': '연결_어미',
    'ETN': '명사형_전성_어미',
    'ETM': '관형형_전성_어미',
    'XPN': '체언_접두사',
    'XSN': '명사_파생_접미사',
    'XSV': '동사_파생_접미사',
    'XSA': '형용사_파생_접미사',
    'XR': '어근',
    'SF': '마침표_물음표_느낌표',
    'SE': '줄임표',
    'SSO': '여는_괄호',
    'SSC': '닫는_괄호',
    'SC': '구분자',
    'SL': '외국어',
    'SH': '한자',
    'SN': '숫자',
    'SY': '기타기호'
}

posRemoveTable = {
    # 'NNG': '일반_명사',
    # 'NNP': '고유_명사',
    # 'NNB': '의존_명사',
    # 'NNBC': '단위를_나타내는_명사',
    # 'NR': '수사',
    # 'NP': '대명사',
    # 'VV': '동사',
    # 'VA': '형용사',
    # 'VX': '보조_용언',
    'VCP': '긍정_지정사',
    'VCN': '부정_지정사',
    # 'MM': '관형사',
    # 'MAG': '일반_부사',
    # 'MAJ': '접속_부사',
    # 'IC': '감탄사',
    'JKS': '주격_조사',
    'JKC': '보격_조사',
    'JKG': '관형격_조사',
    'JKO': '목적격_조사',
    'JKB': '부사격_조사',
    'JKV': '호격_조사',
    'JKQ': '인용격_조사',
    'JX': '보조사',
    'JC': '접속_조사',
    # 'EP': '선어말_어미',
    # 'EF': '종결_어미',
    # 'EC': '연결_어미',
    # 'ETN': '명사형_전성_어미',
    # 'ETM': '관형형_전성_어미',
    # 'XPN': '체언_접두사',
    # 'XSN': '명사_파생_접미사',
    # 'XSV': '동사_파생_접미사',
    # 'XSA': '형용사_파생_접미사',
    # 'XR': '어근',
    # 'SF': '마침표_물음표_느낌표',
    # 'SE': '줄임표',
    # 'SSO': '여는_괄호',
    # 'SSC': '닫는_괄호',
    # 'SC': '구분자',
    # 'SL': '외국어',
    # 'SH': '한자',
    # 'SN': '숫자',
    # 'SY': '기타기호'
}

posInterestingTable = {
    'NNG': '일반_명사',
    'NNP': '고유_명사',
    'NNB': '의존_명사',
    #    'NNBC': '단위를_나타내는_명사',
    'NR': '수사',
    'NP': '대명사',
    # 'VV': '동사',
    # 'VA': '형용사',
    #    'VX': '보조_용언',
    # 'VCP': '긍정_지정사',
    # 'VCN': '부정_지정사',
    # 'MM': '관형사',
    # 'MAG': '일반_부사',
    # 'MAJ': '접속_부사',
    # 'IC': '감탄사',
    #    'JKS': '주격_조사',
    #    'JKC': '보격_조사',
    #    'JKG': '관형격_조사',
    #    'JKO': '목적격_조사',
    # 'JKB': '부사격_조사',
    # 'JKV': '호격_조사',
    # 'JKQ': '인용격_조사',
    # 'JX': '보조사',
    # 'JC': '접속_조사',
    # 'EP': '선어말_어미',
    # 'EF': '종결_어미',
    # 'EC': '연결_어미',
    # 'ETN': '명사형_전성_어미',
    # 'ETM': '관형형_전성_어미',
    # 'XPN': '체언_접두사',
    # 'XSN': '명사_파생_접미사',
    # 'XSV': '동사_파생_접미사',
    # 'XSA': '형용사_파생_접미사',
    'XR': '어근',
    # 'SF': '마침표_물음표_느낌표',
    # 'SE': '줄임표',
    # 'SSO': '여는_괄호',
    # 'SSC': '닫는_괄호',
    # 'SC': '구분자',
    # 'SL': '외국어',
    # 'SH': '한자',
    # 'SN': '숫자',
    # 'SY': '기타기호'
    'LAST': 'LAST'
}


class TimeContents(object):
    def __init__(self, ID=None):
        self.ID = ID
        self.consTime = []
        self.consContents = []

    def append_contents(self, consTime, contents):
        self.consTime.append(consTime)
        self.consContents.append(contents)

    def get_average_length(self):
        total_length = 0
        for count_idx in range(0, len(self.consTime)):
            total_length = total_length + len(self.consContents[count_idx])
        return total_length / len(self.consTime)

    def get_average_word_count(self):
        total_count = 0
        for count_idx in range(0, len(self.consTime)):
            total_count += len(self.consContents[count_idx].split())
        return total_count / len(self.consTime)

    def get_max_sequence_minutes(self):
        starttime = self.consTime[0]
        newstarttime = starttime
        max_sequence = 1
        cur_sequence = 1
        for count_idx in range(1, len(self.consTime)):
            if (self.consTime[count_idx] - self.consTime[count_idx - 1]).total_seconds() <= 60:
                cur_sequence += 1
            else:
                if max_sequence < cur_sequence:
                    max_sequence = cur_sequence
                    lasttime = self.consTime[count_idx - 1]
                    starttime = newstarttime
                newstarttime = self.consTime[count_idx]
                cur_sequence = 1

        if max_sequence < cur_sequence:
            max_sequence = cur_sequence
        return max_sequence, starttime, lasttime

    def get_max_sequence_minutes_range(self):
        starttime = self.consTime[0]
        newstarttime = starttime
        max_sequence = 1
        cur_sequence = 1
        for count_idx in range(1, len(self.consTime)):
            if (self.consTime[count_idx] - self.consTime[count_idx - 1]).total_seconds() <= 60:
                if self.consTime[count_idx] != self.consTime[count_idx - 1]:
                    cur_sequence += 1
            else:
                if max_sequence < cur_sequence:
                    max_sequence = cur_sequence
                    lasttime = self.consTime[count_idx - 1]
                    starttime = newstarttime
                newstarttime = self.consTime[count_idx]
                cur_sequence = 1

        if max_sequence < cur_sequence:
            max_sequence = cur_sequence
        return max_sequence, starttime, lasttime

    def get_time_minute_histogram(self):
        minute_histogram = {}
        for count_idx in range(1, len(self.consTime)):
            interval = round((self.consTime[count_idx] - self.consTime[count_idx - 1]).total_seconds() / 60)
            if interval in minute_histogram:
                minute_histogram[interval] += 1
            else:
                minute_histogram[interval] = 1
        return sorted(minute_histogram.items())

    def get_number_of_sharp_search(self):
        computed_count = 0
        for count_idx in range(0, len(self.consContents)):
            if self.consContents[count_idx].find('샵검색') != -1 and self.consContents[count_idx].find('#') != -1:
                computed_count += 1
        return computed_count

    def get_word_frequency(self):
        word_histogram_short = {}
        for count_idx in range(0, len(self.consTime)):
            tag_origin = meCab.parse(self.consContents[count_idx])
            tag_out = tag_origin

            tag_out_list = tag_out.split('\n')

            for for_word in tag_out_list:
                is_inserted = False
                for POS in posInterestingTable.keys():
                    if for_word.find(POS) != -1:
                        is_inserted = True
                        break
                if not is_inserted:
                    continue

                for POS in posTable.keys():
                    for_word = for_word.replace(POS, posTable[POS])

                for_word = for_word.replace('\t', ',')
                for_word_last = for_word.split(',')[0] + '-' + for_word.split(',')[1]
                if for_word_last in word_histogram_short:
                    word_histogram_short[for_word_last] += 1
                else:
                    word_histogram_short[for_word_last] = 1

        return sorted(word_histogram_short.items(), key=lambda x: x[1], reverse=True)


f = open("full.txt", 'r', encoding='UTF8')

indexLine = 0

meCab = MeCab.Tagger()

IDDictionary = {}
contentsArray = []

numberOfUsers = 0

intervalTable = {}

conversationTable = {}

previousTime = datetime(2019, 5, 5, 20, 46, 0)

while True:
    # if indexLine > 20:
    #     break

    readLine = f.readline()
    if not readLine:
        break
    # print(indexLine, readLine)
    indexLine = indexLine + 1

    if indexLine < 5:
        continue

    if readLine.find(',') == -1 or readLine.find(':') == -1 or readLine[0:4] != '2019':
        continue

    timeLine = readLine.split(',')[0]
    IDLine = ""
    contentsLine = ""
    if len(readLine.split(',')[1].split(':')) > 1:
        IDLine = readLine.split(',')[1].split(':')[0].strip()
        contentsLine = readLine.split(',')[1][readLine.split(',')[1].find(':') + 2:].strip()

    #    print("1.time:" + timeLine, "2.ID:" + IDLine, "3.content:" + contentsLine)

    splitTimeLine = re.split(' |:', timeLine)

    extYear = int(splitTimeLine[0][:4])
    extMonth = int(splitTimeLine[1][:-1])
    extDate = int(splitTimeLine[2][:-1])

    extHour = int(splitTimeLine[4])
    if extHour == 12:
        extHour = 0
    if splitTimeLine[3] == '오후':
        extHour = extHour + 12

    extMinute = int(splitTimeLine[5])

    thisTime = datetime(extYear, extMonth, extDate, extHour, extMinute, 0)

    if thisTime not in conversationTable:
        conversationTable[thisTime] = 1

    computedInterval = round((thisTime - previousTime).total_seconds() / 60)

    if computedInterval in intervalTable:
        intervalTable[computedInterval] += 1
    else:
        intervalTable[computedInterval] = 1

    previousTime = thisTime

    # print(thisTime)

    if IDLine not in IDDictionary:
        IDDictionary[IDLine] = numberOfUsers
        contentsArray.append(TimeContents(IDLine))
        numberOfUsers = numberOfUsers + 1

    contentsArray[IDDictionary[IDLine]].append_contents(thisTime, contentsLine)

    # tagOut = meCab.parse(contentsLine).split()
    # countWord = 0
    # for word in tagOut:
    #     print(countWord, word)
    #     countWord = countWord + 1

    # for idx in range(0, len(splitLine) - 1):
    #    print(idx, splitLine[idx])
    # for token in splitLine:

for idx in range(0, numberOfUsers):
    thisUser = contentsArray[idx]
    resultShort = thisUser.get_word_frequency()
    [maxsequencelength, maxsequencestarttime, maxsequencetime] = thisUser.get_max_sequence_minutes()
    [maxsequencelengthrange, maxsequencestarttimerange, maxsequencetimerange] = thisUser.get_max_sequence_minutes_range()
    print(thisUser.ID,
          "average length", thisUser.get_average_length(),
          "\nnumber of contents", len(thisUser.consContents),
          "\naverage word count", thisUser.get_average_word_count(),
          "\nmax sequence", maxsequencelength, maxsequencestarttime, maxsequencetime,
          "\nmax sequence range", maxsequencelengthrange, maxsequencestarttimerange, maxsequencetimerange,
          "\nhistogram", thisUser.get_time_minute_histogram(),
          "\n# search", thisUser.get_number_of_sharp_search())
    for word in resultShort:
        if word[1] > 50:
            print(word)
    print("\n\n")

for intervals in sorted(intervalTable.keys()):
    print(intervals, intervalTable[intervals])

print(round((previousTime - datetime(2019, 5, 5, 20, 46, 0)).total_seconds() / 60), len(conversationTable),
      len(conversationTable) / round((previousTime - datetime(2019, 5, 5, 20, 46, 0)).total_seconds() / 60))

f.close()
