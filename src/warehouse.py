import json
import queue
from algo import Algo
import time

class Warehouse():
	#This is a grid-based warehouse, which has size = rows x cols
	def __init__(self, grid):
		self.grid = grid
		self.robots = []
		self.goods = []
		self.requests = queue.Queue()
		self.requests_hold = 5
		
	def load_data(self, data_path):
		with open (data_path, 'rb') as file:
			json_object = file.read()
			data = json.loads(json_object)
			return data
	
	def load_robots(self, robots_path):
		robots = self.load_data(robots_path)
		self.robots = [tuple(robots[i]['pos']) for i in range(len(robots))]
		self.grid.walls += self.robots
			
	def load_goods(self, goods_path):
		goods = self.load_data(goods_path)
		self.goods = [tuple(goods[i]['pos']) for i in range(len(goods))]
		
	def load_requests(self, requests_path):
		requests = self.load_data(requests_path)
		for request in requests:
			self.requests.put({tuple(request['src']): tuple(request['dest'])})
			
	def maintain(self):
		algo = Algo(self)
		count = 0
		while True:
			if not self.requests.empty():
				if count <= self.requests_hold:
					count += 1
					algo.A_star_search()
					count -= 1
				else:
					#Sleep somethings
					time.sleep(0.05)
			else:
				#Sleep somethings
				time.sleep(0.05)