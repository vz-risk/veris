import logging


def updateLogger(cfg=None, formatDesign=None, dateFmt=None):
  logger = logging.getLogger()
  FORMAT = '%(asctime)19s - %(processName)s - %(process)d {0}- %(levelname)s - %(message)s'
  logging_remap = {'error': logging.ERROR, 'warning':logging.WARNING, 'critical':logging.CRITICAL, 'info':logging.INFO, 'debug':logging.DEBUG,
                   50: logging.CRITICAL, 40: logging.ERROR, 30: logging.WARNING, 20: logging.INFO, 10: logging.DEBUG, 0: logging.CRITICAL}
  if cfg is not None:
    log_level = logging_remap[cfg['log_level']]
    log_file = cfg.get('log_file', None)
  else:
    log_level = logging.DEBUG
    log_file = None
  logger.setLevel(log_level)
  handlers = logger.handlers
  if formatDesign is None:
    formatter = logging.Formatter(FORMAT.format(""), datefmt=dateFmt)
  else:
    formatter = logging.Formatter(FORMAT.format("- " + formatDesign + " "), datefmt=dateFmt)
  streamHandlerPresent = False
  fileHandlerPresent = False
  for handler in handlers:
    if type(handler) == logging.StreamHandler and streamHandlerPresent is not True:
      handler.setLevel(log_level)
      handler.setFormatter(formatter)
      streamHandlerPresent = True
    elif type(handler) == logging.FileHandler and fileHandlerPresent is not True:
      if log_file is not None:
        if handler.baseFilename != log_file:
          logger.removeHandler(handler)
        else:
          handler.setLevel(log_level)
          handler.setFormatter(formatter)
          fileHandlerPresent = True
    else:
      logger.removeHandler(handler)
      logging.debug("Removing handler of type {0}.".format(type(handler)))
  if streamHandlerPresent is not True:
    sh = logging.StreamHandler()
    sh.setLevel(log_level)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    logging.debug("No stream handler found.  Adding handler.")
  if fileHandlerPresent is not True and log_file is not None:
    fh = logging.FileHandler(log_file)
    fh.setLevel(log_level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logging.debug("No file handler found and log_file set to {0}. Adding file handler.".format(log_file))

updateLogger()
