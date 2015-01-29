import sys
from operator import itemgetter
from operator import attrgetter
from pricer_classes import *

target_size = int(sys.argv[1])
buy_book = Buy_Book(target_size)
sell_book = Sell_Book(target_size)

def main():
	"""Execute the program."""
	for i, line in enumerate(sys.stdin):
		order = line.strip()
		order_action = order.split()[1]
		# ADD ORDER LOGIC
		if order_action == 'A': # logic for add order
			add_order = Add_Order(order)
			if add_order.side == 'B': # logic for a buy add order
				add_logic(add_order, buy_book)
			if add_order.side == 'S': # logic for a sell add order
				add_logic(add_order, sell_book) 
		# REDUCE ORDER LOGIC
		elif order_action == 'R': # logic for reduce order
			reduce_order = Reduce_Order(order)
			# look at both the buy book and the sell book
			for order_book in [buy_book, sell_book]:
				# look at each order in the book
				for order in order_book.orders:
					# if the reduce_order.order_id is in the order.order_id
					if reduce_order.order_id == order.order_id:
						reduce_logic(reduce_order, order_book)
						break # logic for a reduce order
		else:
			print('error')

if __name__ == '__main__':
	main()