class MatConf:
    def __init__(self):
        self.__conf = {}

    def creaConf(self, test):
        if test not in self.__conf:
            self.__conf[test] = {}
            self.__conf[test][test] = 0

    def meteConf(self, test, reco):     # se llama conf.meteConf('test', 'reco')
        if test not in self.__conf:
            self.__conf[test]={}

        if reco not in self.__conf[test]:
            self.__conf[test][reco] = 0

        self.__conf[test][reco] += 1

    def __call__(self, test, reco):     # se llama con conf('test','reco')
        if test not in self.__conf:
            return None

        if reco not in self.__conf[test]:
            return 0

        return self.__conf[test][reco]

    def exac(self):     #se llama conf.exac()
        corr = 0
        total = 0
        for test in self.__conf:
            if test in self.__conf[test]:
                corr += self.__conf[test][test]

            total += sum(self.__conf[test].values())   # veces que tendriamos que haver reconocido a test

        exac = corr / total

        return exac

    def eff(self):
        eft = 0
        i = 0

        for test in self.__conf:
            corr = self.__conf[test][test]
            total = sum(self.__conf[test].values())  # veces que tendriamos que haver reconocido a test
            effi = corr / total
            eft += effi
            print('Eficiencia locutor:', test, effi)
            i += 1
        et = eft/i
        print('Eficiencia total', et)


    def print(self):        # conf.print()
        setTest = set(self.__conf.keys())
        setReco = set(setTest)
        for test in setTest:
            setReco |= set(self.__conf[test].keys())

        setTest = sorted(setTest)
        setReco = sorted(setReco)


        for reco in setReco:
            print('\t', reco, end = '')
        print('')

        for test in setTest:
            print(test, end = '')
            for reco in setReco:
                print('\t', self(test, reco), end = '')
            print('')

    def save(self):
        setTest = set(self.__conf.keys())
        setReco = set(setTest)
        for test in setTest:
            setReco |= set(self.__conf[test].keys())

        setTest = sorted(setTest)
        setReco = sorted(setReco)

        matriz = ''

        for reco in setReco:
            matriz += '\t' + reco
        matriz += '\n'

        for test in setTest:
            matriz += test
            for reco in setReco:
                matriz += '\t' + str(self(test, reco))
            matriz += '\n'
        return matriz