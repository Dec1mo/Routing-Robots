import queue
import threading

INFINITY = 99999999

def mahatan_distance(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1])

class Algo():
	def __init__(self, warehouse):
		self.warehouse = warehouse
		
	def find_dest(self, requests):
		for request in requests:
			min_dis = INFINITY
			goal_pos = list(request.keys())[0]
			if goal_pos in self.warehouse.goods:
				#Distances
				last_pos = None
				for robot_pos, robot_stat in self.warehouse.robots.items():
					if robot_stat == None:
						if mahatan_distance(robot_pos, goal_pos) < min_dis:
							min_dis = mahatan_distance(robot_pos, goal_pos)
							if last_pos != None:
								self.warehouse.robots[last_pos] = None
							self.warehouse.robots[robot_pos] = request
							last_pos = robot_pos
			#requests.remove(request)
			#Need some ways to remove done requests
	
	def small_BFS(self, start, goal, type = 0): 
		# type = 0 -> have not picked up goods
		# type = 1 -> picked up goods
		if type == 0:
			self.warehouse.grid.walls = [x for x in self.warehouse.robots.keys() if x not in self.warehouse.goals] 
		elif type == 1:
			self.warehouse.grid.walls = [x for x in (list(self.warehouse.robots.keys()) + list(self.warehouse.goods)) if x not in self.warehouse.goals]
		'''
		print (type)
		print ('walls = ', self.warehouse.grid.walls)
		'''
		frontier = queue.Queue()
		frontier.put(start)
		came_from = {}
		came_from[start] = None

		while not frontier.empty():
			current = frontier.get()

			if current == goal: 
				break           

			for next in self.warehouse.grid.neighbors(current):
				if next not in came_from:
					frontier.put(next)
					came_from[next] = current
					
		current = goal 
		path = []
		while current != start: 
		   path.append(current)
		   current = came_from[current]
		if not path:
			return None
		else:
			return path[-1]
	
	def move(self, robots_next_mov, goods_next_mov):
		updated_robots = {}
		updated_goods = {}
		remaining_robots = {}
		remaining_goods = {}
		for here, next in robots_next_mov.items():
			# print ('here = ', here)
			# print ('update = ', updated_robots)
			if next not in updated_robots:
				updated_robots[next] = here
				self.warehouse.robots[next] = self.warehouse.robots.pop(here)
			else:
				remaining_robots[here] = next
			# print ('update = ', updated_robots)
		for here, next in goods_next_mov.items():
			if next not in updated_goods:
				updated_goods[next] = here
				# print ('here = ', here)
				# print ('next = ', next)
				# print ('goods = ', self.warehouse.goods)
				self.warehouse.goods.remove(here)
				self.warehouse.goods.add(next)
				# print ('goods = ', self.warehouse.goods)
				for robot, request in self.warehouse.robots.items():
					if request != None:
						if here in request.keys():
							dest2 = list(request.items())[0][1]
							new_dest = {}
							new_dest[next] = dest2
							self.warehouse.robots[robot] = new_dest
			else:
				remaining_goods[here] = next
		return remaining_robots, remaining_goods
				
				
	def is_covered(self):
		for robot, dest in self.warehouse.robots.items():
			if dest != None:
				return False
		return True
	
	def BFS(self, requests):
		'''
		Notes: This is just a approximate algorithms - not too good
		Need more effiective algorithms here
		Known things: Robots' positions, Goods' positions and Requests
		'''
		self.find_dest(requests) # Changes directly to self.warehouse.robots
		robots_next_mov = {}
		goods_next_mov = {}
		one_state_robots = [robot for robot in self.warehouse.robots.keys()]
		one_state_goods = [good for good in self.warehouse.goods]
		robots_states = [one_state_robots]
		goods_states = [one_state_goods]
		while True:
			for robot, dest in list(self.warehouse.robots.items()):
				# (r1,r2):{(d11,d12), (d21, d22)}
				# robot     1st_dest   2nd_dest
				if dest != None:
					dest1, dest2 = list(dest.items())[0]
					next_mov = None
					if robot == dest1 and robot == dest2:
						print ('Done picked for positions = ', robot)
						print ("It's time for you to rest my loyal robot ", robot)
						self.warehouse.robots.pop(robot)
						print ("And you too, some goods, your journey has ended!")
						self.warehouse.goods.remove(robot)
					elif robot == dest1 and robot != dest2: # Picked goods
						next_mov = self.small_BFS(robot, dest2, 1)
						if next_mov != None:
							robots_next_mov[robot] = next_mov
							goods_next_mov[robot] = next_mov
					else:
						next_mov = self.small_BFS(robot, dest1, 0)
						if next_mov != None:		
							robots_next_mov[robot] = next_mov
			robots_next_mov, goods_next_mov = self.move(robots_next_mov, goods_next_mov)
			one_state_robots = [robot for robot in self.warehouse.robots.keys()]
			one_state_goods = [good for good in self.warehouse.goods]
			robots_states.append(one_state_robots)
			goods_states.append(one_state_goods)
			#print (self.warehouse.robots)
			if self.is_covered():
				break
		'''
		for goods_state in goods_states:
			print (goods_state)
			print ('len = ', len(goods_state))
		'''
		return robots_states, goods_states
	

						

		
		
		
		
		
		
		