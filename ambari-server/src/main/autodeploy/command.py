#!/usr/bin/python
#coding=utf-8

import sys, getopt

###
#  命令选项
#
#  longName: 命令选项的完整名称，必须是合法的标识符字符串，前面可以使用--引导，如--file或file
#  defaultValue: 选项对应的默认值，设置为None表示该选项为开关选项，如--version
#  optional: 是否为可选项，defaultValue只在optional = True时生效
#  shortName: 命令选项的缩写名称，默认设置为longName的第一个字符，前面可以使用-引导，如-h
###
class Option:
  def __init__(self, longName, defaultValue = "", optional = True, shortName = "", comment = ""):

    if longName[0:2] == "--":
      longName = longName[2:]

    if not (self.validName(longName)):
      raise Exception("initial error: invalid long option name '{0}'".format(longName))

    if shortName == "":
      shortName = longName[0]

    if shortName[0:1] == "-":
      shortName = shortName[1:]

    if not (self.validName(shortName)):
      raise Exception("initial error: invalid short option name '{0}'".format(shortName))
      
    self.shortName = shortName
    self.longName = longName
    self.needValue = defaultValue != None
    self.defaultValue = defaultValue
    self.optional = optional
    self.comment = comment

  def validName(self, name):
    if len(name) == 0 or name[0].isdigit():
      return False
    else:
      for ch in name.split("_"):
        if not ch.isalnum():
          return False

    return True

  def match(self, option, value):
    if option[0:1] == "-":
      option = option[1:]

    if option[0:1] == "-":
      option = option[1:]

    return option == self.shortName or option == self.longName

  def __str__(self):
    shortInfo = "-{0}".format(self.shortName)
    longInfo = "--{0}".format(self.longName)
    valueInfo = self.defaultValue
    if self.defaultValue != None:
      if self.defaultValue == "":
        valueInfo = "<value>"
      shortInfo += " " + valueInfo
      longInfo += "=" + valueInfo
    optionalInfo = "*" if not self.optional else " "

    info = "{0} or {1}    {2}    {3}".format(shortInfo, longInfo, optionalInfo, self.comment)
    return info


###
#  命令
#
#  options: 保存了所有命令选项对象
#  添加了合法命令选项后，Command会生成对应名称的属性。如添加--file选项，经过命令解析后，可以使用Command().file获取选项的值
###
class Command:

  def __init__(self):
    self.options = []
    self.addOption(Option("version", defaultValue = None, comment = "show deploy tool's version"))
    self.addOption(Option("help", defaultValue = None, comment = "show this help message"))

  def helpInfo(self):
    info = "Usage: {0} [options]\nOptions:\n".format("COMMAND")
    for option in self.options:
      info += "    {0}\n".format(option)

    return info

  def addOption(self, option):
    self.options.append(option)

    if option.needValue:
      self.__dict__[option.longName] = option.defaultValue
    else:
      self.__dict__[option.longName] = False
    

  def parse(self):

    shortOptions = ""
    longOptions = []
    for option in self.options:
      shortOption = option.shortName + ":" if option.needValue else option.shortName
      longOption = option.longName + "=" if option.needValue else option.longName
      shortOptions += shortOption
      longOptions.append(longOption)

    try:
      opts, args = getopt.getopt(sys.argv[1:], shortOptions, longOptions)
      if len(args) != 0:
        raise Exception("command error: invalid argument {0}".format(args[0]))
    except getopt.GetoptError, e:
      raise Exception("command error: {0}".format(e))

    if len(opts) == 0:
      print self.helpInfo()
      sys.exit(0)
  
    for option in self.options:
      for op, value in opts:
        if option.match(op, value):
          self.__dict__[option.longName] = value if option.needValue else True

    if self.help or self.version:
      return

    unused = True
    for option in self.options:
      unused = True
      for op, value in opts:
        if option.match(op, value):
          unused = False
      if unused and not option.optional:
        raise Exception("command error: option --{0} is not optional, must be given a value".format(option.longName))

  def __str__(self):
      encode = ""
      for option in self.options:
        name = option.longName
        value = self.__dict__[name]
        value = "'" + value + "'" if option.needValue else str(value)
        encode += name + " = " + value + ", "

      encode = encode[:-2]
      return "[" + encode + "]"


###
#  使用范例
#  $python command.py --file=hello
#  hello
###
if __name__ == '__main__':

  cmd = Command() # 创建命令对象
  cmd.addOption(Option("file")) # 添加选项
  cmd.parse() # 解析命令参数
  print cmd.file # 打印命令参数的值



