import csv
import datetime


class StorageService:
    def __init__(self, storagePath, filename):
        self.storagePath = storagePath
        self.filename = filename
        self.storageRowIndex = 0

        self.storageWriter = None
        self.storeFile = None

    def start(self):
        self.storeFile = open(self.storagePath +
                              (self.__class__.__name__ if self.filename is None else self.filename) +
                              "_" + str(datetime.datetime.now().date()) + ".csv", 'a')
        self.storageWriter = csv.writer(self.storeFile, dialect='excel')

    def isStorageInitialized(self):
        return self.storeFile is not None

    def stop(self):
        self.storeFile.close()
        self.storageWriter = None
        self.storeFile = None

    def store(self, data, dataType, failFast=True):
        if self.storeFile is not None and self.storageWriter is not None:
            try:
                # for unknown reason fileis clsoed when it's initialized in self.start :(

                self.storeFile = open(self.storagePath +
                                      (self.__class__.__name__ if self.filename is None else self.filename) +
                                      "_" + str(datetime.datetime.now().date()) + ".csv", 'a')
                self.storageWriter = csv.writer(self.storeFile, dialect='excel')

                self.storageRowIndex += 1
                self.storageWriter.writerow([self.storageRowIndex, datetime.datetime.now(), dataType, str(data[1])])
            except Exception as e:  # todo: error handling!
                print(e)
        else:
            if failFast:
                raise Exception("StorageService is not running!")