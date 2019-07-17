import json
import queue
from algo import Algo
import time
from threading import Thread

def to_json_file(list, file_name):
	with open (file_name, 'w+') as f:
		json.dump(list, f)

class Warehouse():
	#This is a grid-based warehouse, which has size = rows x cols, a graph with (rows x cols) nodes
	def __init__(self, grid, goals):
		self.grid = grid
		self.robots = {}
		self.goods = set()
		self.requests = queue.Queue()
		self.requests_hold = 6
		self.count = 0
		self.remaining_requests = []
		self.goals = goals
		
	def load_data(self, data_path):
		with open (data_path, 'rb') as file:
			json_object = file.read()
			data = json.loads(json_object)
			return data
	
	def load_robots(self, robots_path):
		robots = self.load_data(robots_path)
		for robot in robots:
			self.robots[tuple(robot['pos'])] = None
			
	def load_goods(self, goods_path):
		goods = self.load_data(goods_path)
		for good in goods:
			self.goods.add(tuple(good['pos']))
		
	def load_requests(self, requests_path):
		requests = self.load_data(requests_path)
		for request in requests:
			self.requests.put({tuple(request['src']): tuple(request['dest'])})
			
	def maintain(self):
		algo = Algo(self)
		while True:
			if not self.requests.empty() and self.count < self.requests_hold:
				self.count += 1
				request = self.requests.get()
				self.remaining_requests.append(request)
			else:
				break
		print ('requests = ', self.remaining_requests)
		robots_states, goods_states = algo.BFS(self.remaining_requests)
		to_json_file(robots_states, r'../results/robots_states.json')
		to_json_file(goods_states, r'../results/goods_states.json')
		#These features (multithread support) will be developed in the future
		'''
		while True:
			if not self.requests.empty():
				if self.count < self.requests_hold: #Need synchronized
					self.count += 1
					request = self.requests.get()
					#Multi-thread o day?
					bfs_thread = Thread(target = algo.BFS, args = (request))
					bfs_thread.start() 
					self.count -= done_requests
				else:
					#Sleep somethings
					time.sleep(0.1)
			else:
				#Sleep somethings
				break
				time.sleep(0.05)
		'''
		
				
					
					
					
					
					
					
					
					
					
					
		