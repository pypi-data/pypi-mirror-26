import sys,json,StringIO
from webob import Response

class hfunc(object):
	def __init__(self):
		self.buf=StringIO.StringIO()
		self.content_length=0
		self.raw_packet_length=0
		self.newline=0
		self.headers={}

	def clear(self):
		self.buf.truncate(0)
		self.content_length=0
		self.raw_packet_length=0
		self.newline=0
		self.headers.clear()

	def out(self,status_code,data):
		body=json.dumps(data) #data must be dict
		res=Response()
		res.status=status_code
		res.body=body
		res.headerlist=[('Content-type','application/json')]
		res.content_length=len(body)

		sys.stdout.write("HTTP/1.1 "+str(res)+'\n')

	def read(self,**kwargs):
		if kwargs.get('max_request_size') is not None:
			max_size=kwargs.get('max_request_size')
		else:
			max_request_size=512 #default size

		for char in sys.stdin.read(1):
			if char == '\n':
				self.newline=self.newline + 1
			self.buf.write(char)

			#to prevent buffer overflow
			#	max_request_size include header size.
			if self.buf.len > max_request_size:
				self.clear()

			#If I send data to this api via iron function console, header size will be 11.
			#	any other methods will attach additional header(ex:x-forwarded-for), so in that case, header size will be more than 11.
			if self.newline >= 11 and self.content_length==0:
				request_raw=self.buf.getvalue().splitlines()
				try:
					for header in request_raw[3:-1]:
						h=header.split(':')[0]
						v=header.split(':')[1]
						self.headers[h]=v
				except Exception,e:
						self.clear()
						return [False,str(e)]

				#to calculate accurate request size, I need all headers. Task-Id is last header in request, so check it exists.
				if self.headers.get('Content-Length') != None and self.headers.get('Task-Id') != None:
					self.content_length=int(self.headers.get('Content-Length'))+1 #add 1 for last new-line, which isn't included in Content-Length header.
					self.raw_packet_length=self.buf.len+self.content_length

			#check buffer size and run
			#	what if data structure is wrong? -> then It'll not return any data until timeout.
			#	iron function will kill it when timeout reached.
			if self.buf.len == self.raw_packet_length:
				raw_body=self.buf.getvalue()[-self.content_length:]
				try:
					body=json.loads(raw_body)
					state=True
				except Exception,e:
					body=",".join((str(e),raw_body))
					state=False
				finally:
					self.clear()
					return [state,body]
