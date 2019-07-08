#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

class Decoder:
    '''
        Cette classe decode une trame de sigfox
        Elle rend accessible les informations decodées au moyen du getter getDatas()
        Son constructeur prend directement en parametres les strings de la trame sigfox
    '''


    def __init__(self, trame, debug=False):
        self._datas = {}
        self._trame = bytes.fromhex(trame)
        self._payloadType = 0

        # Referencement des data extractables
        self._dataInfos = {
            "Downlink" :    (self._trame, 0b100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000),
            "Turbidity" :   (self._trame, 0b011111111111000000000000000000000000000000000000000000000000000000000000000000000000000000000000),
            "GPSLat" :      (self._trame, 0b000000000000111111111111111111110000000000000000000000000000000000000000000000000000000000000000),
            "Acceleration" :(self._trame, 0b000000000000000000000000000000001110000000000000000000000000000000000000000000000000000000000000),
            "GPSLong" :     (self._trame, 0b000000000000000000000000000000000001111111111111111111000000000000000000000000000000000000000000),
            "GPSLongSign" : (self._trame, 0b000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000),
            "GPSlatSign" :  (self._trame, 0b000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000),
            "pH" :          (self._trame, 0b000000000000000000000000000000000000000000000000000000001111111000000000000000000000000000000000),
            "InnerWater" :  (self._trame, 0b000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000),
            "Pression" :    (self._trame, 0b000000000000000000000000000000000000000000000000000000000000000011111111111110000000000000000000),
            "Conductance" : (self._trame, 0b000000000000000000000000000000000000000000000000000000000000000000000000000001111111111100000000),
            "Temperature" : (self._trame, 0b000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011111110),
            "OuterWater" :  (self._trame, 0b000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
        }

        # Initialisation du logger
        if (debug):
            self._initLog()
        else:
            self._initLog(logging.WARNING)

        self._decodeSpecific()

    def _decodeSpecific(self):
        '''
            Appelle la fonction correspondant au type de package
        '''
        switcher = {
            0 : self._decodeType0
        }

        func = switcher.get(0, lambda : "Type de trame invalide") #self._payloadType a calculer et mettre a la place de 0 pour plus de payloadType
        return func()

    def _decodeType0(self):
        self._decodeData("Downlink", self._dataInfos["Downlink"])
        self._decodeData("Turbidity", self._dataInfos["Turbidity"])
        self._decodeData("GPSLat", self._dataInfos["GPSLat"])
        self._decodeData("Acceleration", self._dataInfos["Acceleration"])
        self._decodeData("GPSLong", self._dataInfos["GPSLong"])
        self._decodeData("GPSLongSign", self._dataInfos["GPSLongSign"])
        self._decodeData("GPSlatSign", self._dataInfos["GPSlatSign"])
        self._decodeData("pH", self._dataInfos["pH"])
        self._decodeData("InnerWater", self._dataInfos["InnerWater"])
        self._decodeData("Pression", self._dataInfos["Pression"])
        self._decodeData("Conductance", self._dataInfos["Conductance"])
        self._decodeData("Temperature", self._dataInfos["Temperature"])
        self._decodeData("OuterWater", self._dataInfos["OuterWater"])

    def _decodeData(self, key, dataInfo):
        #self.datas[key] = self._getDecWithMask(self.trame[-1], 0xFF)
        self._datas[key] = self._getDecWithMask(dataInfo[0], dataInfo[1])
        self.logger.debug("{} :: {}".format(key, self._datas[key]))

    def getDatas(self):
        '''
            Cette fonction renvoi un dictionnaire qui contient toutes les données
            extraites, selon le type de trame
        '''
        return self._datas

    def _getDecWithMask(self, byte, mask):
        '''
            Cette fonction retourne la valeur decimale des bits selectionnes d'un byte
            par le masque transmis en paramètre
            byte est de type 'int' ou 'bytes'
            mask est de type 'int'
        '''
        if (mask == 0):
            return None

        if (isinstance(byte, bytes)):
            byte = int.from_bytes(byte, byteorder='little')

        dec = byte & mask
        while (mask & 1 == 0):
            mask = mask >> 1
            dec  = dec >> 1
        return dec

    # création de l'objet logger qui va nous servir à écrire dans les logs
    def _initLog(self, level=logging.DEBUG):
        self.logger = logging.getLogger()

# Pour tester
if (__name__ == "__main__"):
    trame = "C1FBF34FBB464A4D3456F747"

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    inst = Decoder(trame)
