# -*- coding: utf-8 -*-
# This file is part of AYAB.
#
#    AYAB is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    AYAB is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with AYAB.  If not, see <http://www.gnu.org/licenses/>.
#
#    Copyright 2013, 2014 Sebastian Oliva, Christian Obersteiner, Andreas Müller
#    https://bitbucket.org/chris007de/ayab-apparat/

from ayab_communication import AyabCommunication
import ayab_image
import time
import logging
from ayab.plugins.knitting_plugin import KnittingPlugin
from PyQt4 import QtGui, QtCore

from ayab_options import Ui_DockWidget


class AyabPluginControl(KnittingPlugin):

  def onknit(self, e):
    logging.debug("called onknit on AyabPluginControl")
    #TODO: handle error behaviour.
    self.__knitImage(self.__image, self.conf)

  def onconfigure(self, e):
    logging.debug("called onconfigure on TestingKnittingPlugin")
    conf = self.get_configuration_from_ui(self.__parent_ui)
    #TODO: detect if previous conf had the same image to avoid re-generating.
    try:
      self.__image = ayab_image.ayabImage(self.conf["filename"], self.conf["num_colors"])
    except:
      self.__notify_user("You need to set an image.", "error")
      return

    if conf.get("start_needle") and conf.get("stop_needle"):
      self.__image.setKnitNeedles(conf.get("start_needle"), conf.get("stop_needle"))
      if conf.get("alignment"):
        self.__image.setImagePosition(conf.get("alignment"))
    if conf.get("start_line"):
      self.__image.setStartLine(conf.get("start_line"))

    self.validate_configuration(conf)

    return

  def validate_configuration(self, conf):
    if conf.get("start_needle") and conf.get("stop_needle"):
      if conf.get("start_needle") > conf.get("stop_needle"):
        self.__notify_user("Invalid needle start and end.", "warning")
    if conf.get("start_line") > self.__image.imgHeight():
      self.__notify_user("Start Line is larger than the image.")

  def onfinish(self, e):
    logging.info("Finished Knitting.")
    pass

  def __wait_for_user_action(self, message="", message_type="info"):
    """Sends the display_blocking_pop_up_signal QtSignal to main GUI thread, blocking it."""
    self.__parent_ui.emit(QtCore.SIGNAL('display_blocking_pop_up_signal(QString, QString)'), message, message_type)

  def __notify_user(self, message="", message_type="info"):
    """Sends the display_pop_up_signal QtSignal to main GUI thread, not blocking it."""
    self.__parent_ui.emit(QtCore.SIGNAL('display_pop_up_signal(QString, QString)'), message, message_type)

  def __emit_progress(self, percent):
    """Sends the updateProgress QtSignal."""
    self.__parent_ui.emit(QtCore.SIGNAL('updateProgress(int)'), int(percent))

  def setup_ui(self, parent_ui):
    """Sets up UI elements from ayab_options.Ui_DockWidget in parent_ui."""
    self.__parent_ui = parent_ui
    self.options_ui = Ui_DockWidget()
    self.dock = parent_ui.ui.knitting_options_dock  # findChild(QtGui.QDockWidget, "knitting_options_dock")
    self.options_ui.setupUi(self.dock)
    self.setup_behaviour_ui()

  def setup_behaviour_ui(self):
    """Connects methods to UI elements."""
    conf_button = self.options_ui.configure_button  # Used instead of findChild(QtGui.QPushButton, "configure_button")
    conf_button.clicked.connect(self.conf_button_function)

  def conf_button_function(self):
    self.configure()

  def cleanup_ui(self, parent_ui):
    """Cleans up UI elements inside knitting option dock."""
    #dock = parent_ui.knitting_options_dock
    dock = self.dock
    cleaner = QtCore.QObjectCleanupHandler()
    cleaner.add(dock.widget())
    self.__qw = QtGui.QWidget()
    dock.setWidget(self.__qw)

  def get_configuration_from_ui(self, ui):
    """Creates a configuration dict from the ui elements.

    Returns:
      dict: A dict with configuration.

    """

    self.conf = {}
    color_line_text = ui.findChild(QtGui.QSpinBox, "color_edit").value()
    self.conf["num_colors"] = int(color_line_text)
    start_line_text = ui.findChild(QtGui.QSpinBox, "start_line_edit").value()
    self.conf["start_line"] = int(start_line_text)
    start_needle_text = ui.findChild(QtGui.QSpinBox, "start_needle_edit").value()
    self.conf["start_needle"] = int(start_needle_text)
    stop_needle_text = ui.findChild(QtGui.QSpinBox, "stop_needle_edit").value()
    self.conf["stop_needle"] = int(stop_needle_text)
    alignment_text = ui.findChild(QtGui.QComboBox, "alignment_combo_box").currentText()
    self.conf["alignment"] = alignment_text
    machine_type_text = ui.findChild(QtGui.QComboBox, "machine_type_box").currentText()
    self.conf["machine_type"] = str(machine_type_text)
    #serial_port_dropdown is on main gui frame
    serial_port_text = ui.findChild(QtGui.QComboBox, "serial_port_dropdown").currentText()
    self.conf["portname"] = str(serial_port_text)
    self.conf["portname"] = "/dev/ttyACM0"
    # getting file location from textbox
    # FIXME: this should be sent at onconfigure
    filename_text = ui.findChild(QtGui.QLineEdit, "filename_lineedit").text()
    self.conf["filename"] = str(filename_text)
    logging.debug(self.conf)
    #TODO: add more config options
    return self.conf

  def __init__(self):
    super(AyabPluginControl, self).__init__({})
    # KnittingPlugin.__init__(self)

    #Copying from ayab_control
    self.__API_VERSION = 0x03
    self.__ayabCom = AyabCommunication()

    self.__formerRequest = 0
    self.__lineBlock = 0

###Copied from ayab_control
#####################################

  def __setBit(self, int_type, offset):
      mask = 1 << offset
      return(int_type | mask)

  def __setPixel(self, bytearray, pixel):
      numByte = int(pixel / 8)
      bytearray[numByte] = self.__setBit(
          int(bytearray[numByte]), pixel - (8 * numByte))
      return bytearray

  def __checkSerial(self):
        time.sleep(1)  # TODO if problems in communication, tweak here

        line = self.__ayabCom.read_line()

        if line != '':
            msgId = ord(line[0])
            if msgId == 0xC1:    # cnfStart
                # print "> cnfStart: " + str(ord(line[1]))
                return ("cnfStart", ord(line[1]))

            elif msgId == 0xC3:  # cnfInfo
                # print "> cnfInfo: Version=" + str(ord(line[1]))
                logging.debug("Detected device with" + str(ord(line[1])))
                return ("cnfInfo", ord(line[1]))

            elif msgId == 0x82:  # reqLine
                # print "> reqLine: " + str(ord(line[1]))
                return ("reqLine", ord(line[1]))

            else:
                self.__printError("unknown message: " + line[:])  # drop crlf
                return ("unknown", 0)
        return("none", 0)

  def __cnfLine(self, lineNumber):
        imgHeight = self.__image.imgHeight()
        color = 0
        indexToSend = 0
        sendBlankLine = False
        lastLine = 0x00

        # TODO optimize performance
        # initialize bytearray to 0x00
        bytes = bytearray(25)
        for x in range(0, 25):
            bytes[x] = 0x00

        if lineNumber < 256:
            # TODO some better algorithm for block wrapping
            # if the last requested line number was 255, wrap to next block of
            # lines
            if self.__formerRequest == 255 and lineNumber == 0:
                self.__lineBlock += 1
            # store requested line number for next request
            self.__formerRequest = lineNumber
            reqestedLine = lineNumber

            # adjust lineNumber with current block
            lineNumber = lineNumber \
                + (self.__lineBlock * 256)

            #########################
            # decide which line to send according to machine type and amount of colors
            # singlebed, 2 color
            if self.__machineType == 'single' \
                    and self.__numColors == 2:

                # color is always 0 in singlebed,
                # because both colors are knitted at once
                color = 0

                # calculate imgRow
                imgRow = lineNumber + self.__startLine

                # 0   1   2   3   4 .. (imgRow)
                # |   |   |   |   |
                # 0 1 2 3 4 5 6 7 8 .. (imageExpanded)
                indexToSend = imgRow * 2

                # Check if the last line of the image was requested
                if imgRow == imgHeight - 1:
                    lastLine = 0x01

            # doublebed, 2 color
            elif self.__machineType == 'double' \
                    and self.__numColors == 2:

                # calculate imgRow
                imgRow = int(lineNumber / 2) + self.__startLine

                # 0 0 1 1 2 2 3 3 4 4 .. (imgRow)
                # 0 1 2 3 4 5 6 7 8 9 .. (lineNumber)
                # | |  X  | |  X  | |
                # 0 1 3 2 4 5 7 6 8 9 .. (imageExpanded)
                lenImgExpanded = len(self.__image.imageExpanded())
                indexToSend = self.__startLine * 2

                # TODO more beautiful algo
                if lineNumber % 4 == 1 or lineNumber % 4 == 2:
                    color = 1
                else:
                    color = 0

                if (lineNumber - 2) % 4 == 0:
                    indexToSend += lineNumber + 1

                elif (lineNumber - 2) % 4 == 1:
                    indexToSend += lineNumber - 1
                    if (imgRow == imgHeight - 1) \
                            and (indexToSend == lenImgExpanded - 2):
                        lastLine = 0x01
                else:
                    indexToSend += lineNumber
                    if (imgRow == imgHeight - 1) \
                            and (indexToSend == lenImgExpanded - 1):
                        lastLine = 0x01

            # doublebed, multicolor
            elif self.__machineType == 'double' \
                    and self.__numColors > 2:

                # calculate imgRow
                imgRow = int(
                    lineNumber / (self.__numColors * 2)) + self.__startLine

                if (lineNumber % 2) == 0:
                    color = (lineNumber / 2) % self.__numColors
                    indexToSend = (imgRow * self.__numColors) + color
                    logging.debug("COLOR" + str(color))
                else:
                    sendBlankLine = True

                # TODO Check assignment
                if imgRow == imgHeight - 1 \
                        and (indexToSend == lenImgExpanded - 1):
                    lastLine = 0x01
            #########################

            # assign pixeldata
            imgStartNeedle = self.__image.imgStartNeedle()
            imgStopNeedle = self.__image.imgStopNeedle()

            # set the bitarray
            for col in range(0, 200):
                if color == 0 \
                        and self.__machineType == 'double':
                    if col < imgStartNeedle \
                            or col > imgStopNeedle:
                        bytes = self.__setPixel(bytes, col)

            for col in range(0, self.__image.imgWidth()):
                pxl = (self.__image.imageExpanded())[indexToSend][col]
                # take the image offset into account
                if pxl == True and sendBlankLine == False:
                    bytes = self.__setPixel(
                        bytes, col + self.__image.imgStartNeedle())

            # TODO implement CRC8
            crc8 = 0x00

            # send line to machine
            self.__ayabCom.cnf_line(reqestedLine, bytes, lastLine, crc8)

            # screen output
            msg = str((self.__image.imageExpanded())[indexToSend])
            msg += ' Image Row: ' + str(imgRow)
            msg += ' (indexToSend: ' + str(indexToSend)
            msg += ', reqLine: ' + str(reqestedLine)
            msg += ', lineNumber: ' + str(lineNumber)
            msg += ', lineBlock:' + str(self.__lineBlock) + ')'
            logging.debug(msg)
            #sending line progress to gui
            progress_int = 100 * float(reqestedLine + 1)/self.__image.imgHeight()
            self.__emit_progress(progress_int)

        else:
            logging.error("requested lineNumber out of range")

        if lastLine:
            return 1  # image finished
        else:
            return 0  # keep knitting

  def __knitImage(self, pImage, pOptions):
      self.__formerRequest = 0
      self.__image = pImage
      self.__startLine = pImage.startLine()

      self.__numColors = pOptions["num_colors"]
      self.__machineType = pOptions["machine_type"]

      API_VERSION = self.__API_VERSION
      curState = 's_init'
      oldState = 'none'

      if not self.__ayabCom.open_serial(pOptions["portname"]):
          logging.error("Could not open serial port")
          return

      while True:
          # TODO catch keyboard interrupts to abort knitting
          rcvMsg, rcvParam = self.__checkSerial()
          if curState == 's_init':
              if oldState != curState:
                  self.__ayabCom.req_info()

              if rcvMsg == 'cnfInfo':
                  if rcvParam == API_VERSION:
                      curState = 's_start'
                      self.__wait_for_user_action("Please init machine")
                  else:
                      logging.error("wrong API version: " + str(rcvParam)
                                        + (" (expected: )") + str(API_VERSION))
                      return

          if curState == 's_start':
              if oldState != curState:
                  self.__ayabCom.req_start(self.__image.knitStartNeedle(),
                                           self.__image.knitStopNeedle())

              if rcvMsg == 'cnfStart':
                  if rcvParam == 1:
                      curState = 's_operate'
                      self.__wait_for_user_action("Ready to Operate")
                  else:
                      logging.error("device not ready")
                      return

          if curState == 's_operate':
              if rcvMsg == 'reqLine':
                  imageFinished = self.__cnfLine(rcvParam)
                  if imageFinished:
                      curState = 's_finished'

          if curState == 's_finished':
              self.__wait_for_user_action("Image finished")
              return

          oldState = curState

      return
