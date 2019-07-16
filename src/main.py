from grid import Grid
from warehouse import Warehouse
from threading import Thread

def main():
	#Initial grid
	width = 10
	height = 10
	grid = Grid(width, height)
	
	#Initial warehouse
	requests_path = r'../requests/requests.json'
	robots_path = r'../warehouse/robots.json'
	goods_path = r'../warehouse/goods.json'
	warehouse = Warehouse(grid)
	warehouse.load_robots(robots_path)
	warehouse.load_goods(goods_path)
	warehouse.load_requests(requests_path)
	'''
	print (warehouse.robots)
	print (warehouse.goods)
	while not warehouse.requests.empty():
		print (warehouse.requests.get())
	'''
	wh_maintain_thread = Thread(target=warehouse.maintain, args=(tuple(1,1)))
	wh_maintain_thread.start()
	
if __name__ == '__main__':
	main()
	