import logging

log = logging

class LogToFile( object ):
	"""docstring for LogToFile"""
	def __init__( self, filename = "log.log" ):
		super(LogToFile, self).__init__()
		self.filename = filename + ".log"
		log.basicConfig( filename = self.filename, level = log.DEBUG, format='%(asctime)s | %(levelname)s | : %(message)s ', datefmt='%m/%d/%Y %I:%M:%S %p' )

	def debug( self, msg ):
		log.debug( msg )

	def info( self, msg ):
		log.info( msg )

	def warning( self, msg ):
		log.warning( msg )

	def error( self, msg ):
		log.error( msg )

	def critical( self, msg ):
		log.critical( msg )

if __name__ == '__main__':
	logObj = LogToFile("HELLO")
	logObj.info("HELLO")
	logObj.debug("HELLO")
	logObj.warning("HELLO")
	logObj.error("HELLO")
	logObj.critical("HELLO")