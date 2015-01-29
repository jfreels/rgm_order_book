import sys
from operator import itemgetter
from operator import attrgetter


class Add_Order(object):
	"""Add order class."""
	
	def __init__(self, details):
		self.details = details.split()
		self.timestamp = int(self.details[0])
		self.action = str(self.details[1])
		self.order_id = str(self.details[2])
		self.side = str(self.details[3])
		self.price = float(self.details[4])
		self.size = int(self.details[5])


class Reduce_Order(object):
	"""Reduce order class."""

	def __init__(self, details):
		self.details = details.split()
		self.timestamp = int(self.details[0])
		self.action = str(self.details[1])
		self.order_id = str(self.details[2])
		self.size = int(self.details[3])


class Order_Book(object):
	"""Order Book class."""
		
	def __init__(self, target_size):
		self.target_size = target_size
		self.orders = []
		self.current_timestamp = None
		self.total_size_pre_order = 0
		self.total_size_post_order = 0
		self.my_side = None
		self.total_potential_price_pre_trade = 0
		self.total_potential_price_post_trade = 0


	def check_size(self):
		"""Check the size of the book.
		Return the value.
		"""

		size = 0
		for order in self.orders:
			size += order.size

		return size


	def check_total_price(self):
		"""How much would it cost to execute an order of target_size shares?
		Return the value.
		"""

		if self.total_size_post_order < self.target_size:
			return 'NA'

		if self.total_size_post_order >= self.target_size:
			total_price = 0
			still_to_execute = self.target_size
			while still_to_execute > 0:
				for i, order in enumerate(self.orders):
					subtotal_price = 0
					if still_to_execute == 0:
						break
					# if less shares available than we want to buy/sell
					elif order.size <= still_to_execute: 
						subtotal_price += order.size * order.price # buy/sell all available shares
						still_to_execute -= order.size # reduce shares we need by order.size
					# if more shares available than we want to buy/sell
					elif order.size > still_to_execute:
						# buy/sell all the shares
						subtotal_price += still_to_execute * order.price
					 	# reduce # of shares we need to 0
						still_to_execute = 0
					else:
						print('error')
				
					total_price += subtotal_price

			return total_price 


	def add_order(self, order):
		"""Add an order to the book.
		Update the total size of the book.
		Update the total price to execute an order of target_size shares.
		Log the timestamp of the order.
		"""

		# what's the current size of the book?
		self.total_size_pre_order = self.check_size()
		# what's the current prize of the book (up to target_price shares)
		self.total_potential_price_pre_trade = self.check_total_price()

		self.update_timestamp(order) # update time stamp
		self.orders.append(order) # add the order to the book

		
	def update_timestamp(self, order):
		"""Update the self.current_timestamp with the latest order.timestamp."""
		
		self.current_timestamp = order.timestamp


	def check_trade(self):
		"""Check book for total size > target_size.
		Return boolean.
		"""

		return self.total_size_post_order >= self.target_size


	def reduce_order(self, order):
		"""Perform a reduce order.
		Update book size pre and post order.
		Update timestamp.
		"""

		# what's the current size of the book?
		self.total_size_pre_order = self.check_size()
		# what's the current prize of the book (up to target_price shares)
		self.total_potential_price_pre_trade = self.check_total_price()
		self.update_timestamp(order) # update timestamp

		reduce_order_id = order.order_id
		reduce_order_size = order.size
		for order in self.orders:
			if reduce_order_id == order.order_id:
				order.size -= reduce_order_size

		self.remove_empty() # remove empty orders
		# size of order book after order added
		self.total_size_post_order = self.check_size()
		# what's the prize of the book (up to target_price shares) after order
		self.total_potential_price_post_trade = self.check_total_price()

	
	def remove_empty(self):
		"""Remove any orders in the book with a size <= 0."""
		for i, order in enumerate(self.orders):
			if order.size <= 0:
				del self.orders[i]


	def send_output(self):
		"""Send the timestamp, order side (buy/sell), and expense/income to standard output."""

		try:
			price = '{0:.2f}'.format(self.total_potential_price_post_trade)
		except ValueError:
			price = self.total_potential_price_post_trade
		sys.stdout.write('{} {} {}\n'.format(self.current_timestamp, self.my_side, price))


	def show_book(self):
		"""Print the orders in the book."""

		for i, orders in enumerate(self.orders):
			print('#{}: {}'.format(i+1, orders.details))
		print('\n')


	def show_book_details(self):
		"""Show details of the book."""

		print('Timestamp: {}'.format(self.current_timestamp))
		print('Our Side: {}'.format(self.my_side))
		print('Total Size Pre: {}'.format(self.total_size_pre_order))
		print('Total Size Post: {}'.format(self.total_size_post_order))
		print('Total Price Pre: {}'.format(self.total_potential_price_pre_trade))
		print('Total Price Post: {}'.format(self.total_potential_price_post_trade))


class Buy_Book(Order_Book):
	"""Buy book class."""

	def __init__(self, target_size):
		self.target_size = target_size
		self.orders = []
		self.my_side = 'S'
		self.total_size_pre_order = 0
		self.total_size_post_order = 0
		self.total_potential_price_pre_trade = 0
		self.total_potential_price_post_trade = 0
	

	def sort_orders(self):
		"""Sort the book based on the price (highest to lowest)
		and then the timestamp (earliest to latest).
		"""
		self.orders = sorted(self.orders, key=attrgetter('timestamp'))
		self.orders = sorted(self.orders, key=attrgetter('price'), reverse=True)
		#self.orders = sorted(self.orders, key=lambda order: order.timestamp)

		#print('<><><> BOOK AFTER ADD ORDER <><><>')
		#self.show_book() # print the book

		# size of order book after order added
		self.total_size_post_order = self.check_size()
		# what's the prize of the book (up to target_price shares) after order
		self.total_potential_price_post_trade = self.check_total_price()


class Sell_Book(Order_Book):
	"""Sell book class."""

	def __init__(self, target_size):
		self.target_size = target_size
		self.orders = []
		self.my_side = 'B'
		self.total_size_pre_order = 0
		self.total_size_post_order = 0
		self.total_potential_price_pre_trade = 0
		self.total_potential_price_post_trade = 0


	def sort_orders(self):
		"""Sort the book based on the price (lowest to highest)
		and then the timestamp (earliest to latest).
		"""

		self.orders = sorted(self.orders, key=attrgetter('price','timestamp'))

		#print('<><><> BOOK AFTER ADD ORDER <><><>')
		#self.show_book() # print the book

		# size of order book after order added
		self.total_size_post_order = self.check_size()
		# what's the prize of the book (up to target_price shares) after order
		self.total_potential_price_post_trade = self.check_total_price()


def add_logic(order, order_book):
	"""Logic when an add order enters standard input."""

	order_book.add_order(order) # add the order
	order_book.sort_orders() # sort the orders
	if order_book.total_potential_price_pre_trade != order_book.total_potential_price_post_trade:
		order_book.send_output() # send output to stdout (timestamp, side, total_price)

def reduce_logic(order, order_book):
	"""Logic when a reduce order enters standard input."""

	order_book.reduce_order(order) # reduce the order
	if order_book.total_potential_price_pre_trade != order_book.total_potential_price_post_trade:
		order_book.send_output() # send output to stdout (timestamp, side, total_price)

