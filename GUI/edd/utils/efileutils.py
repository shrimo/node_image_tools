import os
import tarfile
import shutil
import uuid
import time
import re
from itertools import imap


class EFileUtils:
    SEQ_REGEX = re.compile('^(?P<basename>.*[_\.])(?P<frame>\d+)(?P<extension>\..*)$')

    def __init__(self):
        return

    @staticmethod
    def checkExt(extension, mask):
        if isinstance(mask, basestring):
            return extension == mask

        if mask == None:
            return True
        try:
            for i in mask:
                if EFileUtils.checkExt(extension, i):
                    return True
        except:

            pass

        return False

    @staticmethod
    def forceDir(dir):
        try:
            if not os.path.exists(dir):
                os.makedirs(dir)
                return True
            return False

        except Exception, e:
            print e

    @staticmethod
    def getSequentialFiles(filenames):
        """
        Generator that yields the sequential files in list of filenames.
        :arg filenames: a list of filenames to search for sequential files
        :type filenames: iterable
        :yields: each valid FileSequence in filenames
        :ytype: pysequences.model.filesequence.FileSequence
        """
        results = {}
        for match in imap(EFileUtils.SEQ_REGEX.match, filenames):
            if match:
                key = '%(pad)s'.join([match.group('basename'), \
                                      match.group('extension')])
                if key not in results.keys():
                    results[key] = set()
                results[key].add(match.group('frame'))

        for name in sorted(results.keys()):
            frames = set(imap(int, results[name]))
            lengths = list(sorted(set(imap(len, results[name]))))
            if len(lengths) == 1:
                length = lengths[0]
            else:
                length = min(lengths)
            pad_kwargs = {'pad': '%%%sd' % (('0%d' % length) * bool(length != 1))}
            yield name % pad_kwargs, frames

        # end get_sequential_files

    @staticmethod
    def getFiles( searchRoot, extension=None, fullPath=True):
        fileList = []

        for root, dirs, files in os.walk(searchRoot):
            for file in files:
                if EFileUtils.checkExt(os.path.splitext(file)[1], extension):
                    if fullPath:
                        fileList.append((os.path.join(root, file)).replace("\\", "/"))
                    else:
                        fileList.append(file)
        return fileList

    @staticmethod
    def copyFile(fromDirectory, toDirectory, fileName):
        """Copy files provided by FileData from edd directory to destination directory"""
        try:
        # Copy top level file from edd to destination.
            shutil.copy(os.path.join(fromDirectory, fileName),
                        os.path.join(toDirectory, fileName))
        except Exception, e:
            print "Exception in <FileUtils.copyFiles()>:\n\t%s" % e
            return False

        return True

    @staticmethod
    def moveFile( fromDirectory, toDirectory, fileName, newFileName ):
        """Move files provided by FileData from edd directory to destination directory"""
        try:
        # Move top level file from edd to destination.
            shutil.move(os.path.join(fromDirectory, fileName),
                        os.path.join(toDirectory, newFileName))

        except Exception, e:
            print "Exception in <FileUtils.copyFiles()>:\n\t%s" % e
            return False

        return True

    @staticmethod
    def writeTarBall( ballName, content):
        tar = tarfile.open(ballName, "w:gz")
        for name in content:
            tar.add(name, recursive=False)
        tar.close()

        return ballName

    def readTarBall(self, ballName):
        tar = tarfile.open(ballName, "r:gz")
        for tarinfo in tar:
            print tarinfo.name, "is", tarinfo.size, "bytes in size and is",
            if tarinfo.isreg():
                print "a regular file."
            elif tarinfo.isdir():
                print "a directory."
            else:
                print "something else."
        tar.close()

