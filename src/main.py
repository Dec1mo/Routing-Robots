from grid import Grid
from warehouse import Warehouse
from threading import Thread

def main():
	#Initial grid
	width = 10
	height = 10
	grid = Grid(width, height)

	#Initial warehouse
	robots_path = r'../warehouse/robots.json'
	goods_path = r'../warehouse/goods.json'
	requests_path = r'../requests/requests.json'
	goals = set([(0, 0), (0, 3), (0, 6), (0, 9)])
	warehouse = Warehouse(grid, goals)
	warehouse.load_robots(robots_path)
	warehouse.load_goods(goods_path)
	warehouse.load_requests(requests_path)
	
	warehouse.maintain()
	
	
if __name__ == '__main__':
	main()
	