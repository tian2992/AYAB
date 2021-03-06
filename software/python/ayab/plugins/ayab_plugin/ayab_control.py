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
import os
from ayab.plugins.knitting_plugin import KnittingPlugin
from PyQt4 import QtGui, QtCore

from ayab_options import Ui_DockWidget
import serial.tools.list_ports


class AyabPluginControl(KnittingPlugin):

  def onknit(self, e):
    logging.debug("called onknit on AyabPluginControl")
    self.__knitImage(self.__image, self.conf)
    self.finish()

  def onconfigure(self, e):
    logging.debug("called onconfigure on AYAB Knitting Plugin")
    #print ', '.join("%s: %s" % item for item in vars(e).items())
    #FIXME: substitute setting parent_ui from self.__parent_ui
    #self.__parent_ui = e.event.parent_ui
    parent_ui = self.__parent_ui

    #Start to knit with the bottom first
    pil_image = parent_ui.pil_image.rotate(180)

    conf = self.get_configuration_from_ui(parent_ui)
    #TODO: detect if previous conf had the same image to avoid re-generating.

    try:
      self.__image = ayab_image.ayabImage(pil_image, self.conf["num_colors"])
    except:
      self.__notify_user("You need to set an image.", "error")
      return

    if conf.get("start_needle") and conf.get("stop_needle"):
      self.__image.setKnitNeedles(conf.get("start_needle"), conf.get("stop_needle"))
      if conf.get("alignment"):
        self.__image.setImagePosition(conf.get("alignment"))
    if conf.get("start_line"):
      self.__image.setStartLine(conf.get("start_line"))

    if self.validate_configuration(conf):
      parent_ui.ui.widget_knitcontrol.setEnabled(True)
      parent_ui.ui.knit_button.setEnabled(True)
      self.__emit_progress(0, 0, self.__image.imgHeight())
    return

  def validate_configuration(self, conf):
    if conf.get("start_needle") and conf.get("stop_needle"):
      if conf.get("start_needle") > conf.get("stop_needle"):
        self.__notify_user("Invalid needle start and end.", "warning")
        return False
    if conf.get("start_line") > self.__image.imgHeight():
      self.__notify_user("Start Line is larger than the image.")
      return False

    if conf.get("portname") == '':
      self.__notify_user("Please choose a valid port.")
      return False

    return True

  def onfinish(self, e):
    logging.info("Finished Knitting.")
    self.__close_serial()
    self.__parent_ui.resetUI()
    self.__parent_ui.emit(QtCore.SIGNAL('updateProgress(int,int,int)'), 0, 0, 0)

  def cancel(self):
    self._knitImage = False
    #self.finish()

  def __close_serial(self):
    try:
      self.__ayabCom.close_serial()
      logging.debug("Closing Serial port successful.")
    except:
      logging.debug("Closing Serial port failed. Was it ever open?")

  def onerror(self, e):
    #TODO add message info from event
    logging.error("Error while Knitting.")
    self.__close_serial()

  def __wait_for_user_action(self, message="", message_type="info"):
    """Sends the display_blocking_pop_up_signal QtSignal to main GUI thread, blocking it."""
    self.__parent_ui.emit(QtCore.SIGNAL('display_blocking_pop_up_signal(QString, QString)'), message, message_type)

  def __notify_user(self, message="", message_type="info"):
    """Sends the display_pop_up_signal QtSignal to main GUI thread, not blocking it."""
    self.__parent_ui.emit(QtCore.SIGNAL('display_pop_up_signal(QString, QString)'), message, message_type)

  def __emit_progress(self, percent, done, total):
    """Sends the updateProgress QtSignal."""
    self.__parent_ui.emit(QtCore.SIGNAL('updateProgress(int,int,int)'), int(percent), int(done), int(total))

  def setup_ui(self, parent_ui):
    """Sets up UI elements from ayab_options.Ui_DockWidget in parent_ui."""
    self.set_translator()
    self.__parent_ui = parent_ui
    self.options_ui = Ui_DockWidget()
    self.dock = parent_ui.ui.knitting_options_dock  # findChild(QtGui.QDockWidget, "knitting_options_dock")
    self.options_ui.setupUi(self.dock)
    self.setup_behaviour_ui()

  def set_translator(self):
    dirname = os.path.dirname(__file__)
    self.translator = QtCore.QTranslator()
    self.translator.load(QtCore.QLocale.system(), "ayab_options", ".", dirname, ".qm")
    app = QtCore.QCoreApplication.instance()
    app.installTranslator(self.translator)

  def unset_translator(self):
    app = QtCore.QCoreApplication.instance()
    app.removeTranslator(self.translator)

  def populate_ports(self, combo_box=None, port_list=None):
    if not combo_box:
      combo_box = self.__parent_ui.findChild(QtGui.QComboBox, "serial_port_dropdown")
    if not port_list:
      port_list = self.getSerialPorts()

    combo_box.clear()

    def populate(combo_box, port_list):
      for item in port_list:
        #TODO: should display the info of the device.
        combo_box.addItem(item[0])
    populate(combo_box, port_list)


  def setup_behaviour_ui(self):
    """Connects methods to UI elements."""
    conf_button = self.options_ui.configure_button  # Used instead of findChild(QtGui.QPushButton, "configure_button")
    conf_button.clicked.connect(self.conf_button_function)


    self.populate_ports()
    refresh_ports = self.options_ui.refresh_ports_button
    refresh_ports.click.connect(self.populate_ports)

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
    self.unset_translator()

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

    start_needle_color = ui.findChild(QtGui.QComboBox, "start_needle_color").currentText()
    start_needle_text = ui.findChild(QtGui.QSpinBox, "start_needle_edit").value()

    if(start_needle_color == "orange"):
      self.conf["start_needle"] = 100 - int(start_needle_text)
    elif(start_needle_color == "green"):
      self.conf["start_needle"] = 99 + int(start_needle_text)

    stop_needle_color = ui.findChild(QtGui.QComboBox, "stop_needle_color").currentText()
    stop_needle_text = ui.findChild(QtGui.QSpinBox, "stop_needle_edit").value()

    if(stop_needle_color == "orange"):
      self.conf["stop_needle"] = 100 - int(stop_needle_text)
    elif(stop_needle_color == "green"):
      self.conf["stop_needle"] = 99 + int(stop_needle_text)


    alignment_text = ui.findChild(QtGui.QComboBox, "alignment_combo_box").currentText()
    self.conf["alignment"] = alignment_text

    self.conf["inf_repeat"] = \
        int(ui.findChild(QtGui.QCheckBox, "infRepeat_checkbox").isChecked())

    machine_type_text = ui.findChild(QtGui.QComboBox, "machine_type_box").currentText()
    self.conf["machine_type"] = str(machine_type_text)

    serial_port_text = ui.findChild(QtGui.QComboBox, "serial_port_dropdown").currentText()
    self.conf["portname"] = str(serial_port_text)
    # getting file location from textbox
    filename_text = ui.findChild(QtGui.QLineEdit, "filename_lineedit").text()
    self.conf["filename"] = str(filename_text)
    logging.debug(self.conf)
    ## Add more config options.
    return self.conf

  def getSerialPorts(self):
      """
      Returns a list of all USB Serial Ports
      """
      return list(serial.tools.list_ports.grep("USB"))

  def __init__(self):
    super(AyabPluginControl, self).__init__({})
    # KnittingPlugin.__init__(self)

    #Copying from ayab_control
    self.__API_VERSION = 0x03
    self.__ayabCom = AyabCommunication()

    self.__formerRequest = 0
    self.__lineBlock = 0

  def __del__(self):
    self.__close_serial()

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
                logging.debug("Detected device with API v" + str(ord(line[1])))
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

            # when knitting infinitely, keep the requested 
            # lineNumber in its limits
            if self.__infRepeat:
              lineNumber = lineNumber % imgHeight

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
            if imgStartNeedle < 0:
              imgStartNeedle = 0

            imgStopNeedle = self.__image.imgStopNeedle()
            if imgStopNeedle > 199:
              imgStopNeedle = 199

            # set the bitarray
            if color == 0 \
                    and self.__machineType == 'double':
                for col in range(0, 200):
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
            if self.__infRepeat:
              self.__ayabCom.cnf_line(reqestedLine, bytes, 0, crc8)
            else:
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
            progress_int = 100 * float(imgRow)/self.__image.imgHeight()
            self.__emit_progress(progress_int, imgRow, imgHeight)

        else:
            logging.error("requested lineNumber out of range")

        if lastLine:
          if self.__infRepeat:
              self.__lineBlock = 0
              return 0 # keep knitting
          else:
              return 1  # image finished
        else:
            return 0  # keep knitting

  def __knitImage(self, pImage, pOptions):
      self.__formerRequest = 0
      self.__image = pImage
      self.__startLine = pImage.startLine()

      self.__numColors = pOptions["num_colors"]
      self.__machineType = pOptions["machine_type"]
      self.__infRepeat = pOptions["inf_repeat"]

      API_VERSION = self.__API_VERSION
      curState = 's_init'
      oldState = 'none'

      if not self.__ayabCom.open_serial(pOptions["portname"]):
          logging.error("Could not open serial port")
          return

      self._knitImage = True
      while self._knitImage:
          # TODO catch keyboard interrupts to abort knitting
          # TODO: port to state machine or similar.
          rcvMsg, rcvParam = self.__checkSerial()
          if curState == 's_init':
              if oldState != curState:
                  self.__ayabCom.req_info()

              if rcvMsg == 'cnfInfo':
                  if rcvParam == API_VERSION:
                      curState = 's_start'
                      self.__wait_for_user_action("Please init machine. (Set the carriage to mode KC-I or KC-II and move the carriage over the left turn mark).")
                  else:
                      self.__notify_user("Wrong API.")
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
                      self.__wait_for_user_action("Device not ready, configure and try again.")
                      logging.error("device not ready")
                      return

          if curState == 's_operate':
              if rcvMsg == 'reqLine':
                  imageFinished = self.__cnfLine(rcvParam)
                  if imageFinished:
                      curState = 's_finished'

          if curState == 's_finished':
              self.__wait_for_user_action("Image transmission finished. Please knit until you hear the double beep sound.")
              return

          oldState = curState

      return
