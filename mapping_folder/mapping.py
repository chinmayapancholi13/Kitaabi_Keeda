import os
import sys

# book_no = float(sys.argv[1])

def main_function(book_no):
	hall_no = 1
	shelf_no = 1

	if (book_no>=664.024 and book_no <=677.99) or (book_no>=678.00 and book_no<=999.00):
		hall_no = 1
		shelf_no = 1


	elif (book_no>=658.542 and book_no <=660.284) or (book_no>=660.284 and book_no<=664.02):
		hall_no = 1
		shelf_no = 2

	elif (book_no>=625.132 and book_no <=656.99) or (book_no>=657.00 and book_no<=658.54):
		hall_no = 1
		shelf_no = 3

	elif (book_no>=624.151 and book_no <=624.99) or (book_no>=625.00 and book_no<=629.132):
		hall_no = 1
		shelf_no = 4


	elif (book_no>=621.4021 and book_no <=621.99) or (book_no>=622.00 and book_no<=624.151):
		hall_no = 1
		shelf_no = 5

	elif (book_no>=621.3815 and book_no <=621.382) or (book_no>=621.383 and book_no<=621.402):
		hall_no = 1
		shelf_no = 6


	elif (book_no>=621.381 and book_no <=621.3815) or (book_no>=621.3815 and book_no<=621.3815):
		hall_no = 1
		shelf_no = 7

	elif (book_no>=621.310 and book_no <=621.367) or (book_no>=621.367 and book_no<=621.381):
		hall_no = 1
		shelf_no = 8

	elif (book_no>=620.11 and book_no <=620.199) or (book_no>=620.2 and book_no<=621.310):
		hall_no = 1
		shelf_no = 9


	elif (book_no>=547.192 and book_no <=619.99) or (book_no>=620.00 and book_no<=620.11):
		hall_no = 1
		shelf_no = 10

	elif (book_no>=547.135 and book_no <=551.470) or (book_no>=551.48 and book_no<=574.192):
		hall_no = 1
		shelf_no = 11

	elif (book_no>=546.00 and book_no <=547.00) or (book_no>=547.00 and book_no<=547.13):
		hall_no = 1
		shelf_no = 12

	elif (book_no>=541.00 and book_no <=541.30) or (book_no>=541.30 and book_no<=546.00):
		hall_no = 1
		shelf_no = 13

	elif (book_no>=532.00 and book_no <=536.00) or (book_no>=536.20 and book_no<=540.99):
		hall_no = 1
		shelf_no = 14

	elif (book_no>=523.00 and book_no <=530.99) or (book_no>=531.00 and book_no<=532.00):
		hall_no = 1
		shelf_no = 15

	elif (book_no>=515.00 and book_no <=518.024) or (book_no>=518.024 and book_no<=522.99):
		hall_no = 1
		shelf_no = 16


	# elif (book_no>=339.00 and book_no <=510.246) or (book_no>=510.246 and book_no<=514.99):
	# 	hall_no = 1
	# 	shelf_no = 17

	# elif (book_no>=5.20 and book_no <=169.99) or (book_no>=74.00 and book_no<=338.99):
	# 	hall_no = 1
	# 	shelf_no = 18


	elif (book_no>=1.00 and book_no <=4.60) or (book_no>=4.60 and book_no<=5.133):
		hall_no = 1
		shelf_no = 19




	elif (book_no>=100 and book_no <=150) or (book_no>=150 and book_no<=153.4):
		hall_no = 3
		shelf_no = 1


	elif (book_no>=153.4 and book_no <=177) or (book_no>=179 and book_no<=294):
		hall_no = 3
		shelf_no = 2

	elif (book_no>=294 and book_no <=300.1) or (book_no>=300.18 and book_no<=301.2):
		hall_no = 3
		shelf_no = 3

	elif (book_no>=301.2 and book_no <=301.36) or (book_no>=301.36 and book_no<=303.1):
		hall_no = 3
		shelf_no = 4

	elif (book_no>=303.3 and book_no <=307.76) or (book_no>=307.76 and book_no<=311):
		hall_no = 3
		shelf_no = 5

	elif (book_no>=311 and book_no <=320.9) or (book_no>=320.9 and book_no<=325):
		hall_no = 3
		shelf_no = 6

	elif (book_no>=327 and book_no <=330.015) or (book_no>=330.015 and book_no<=330.9):
		hall_no = 3
		shelf_no = 7

	elif (book_no>=330.9 and book_no <=330.954) or (book_no>=330.954 and book_no<=331.8):
		hall_no = 3
		shelf_no = 8

	elif (book_no>=331.82 and book_no <=330.954) or (book_no>=330.954 and book_no<=331.8):
		hall_no = 3
		shelf_no = 9

	elif (book_no>=333.79 and book_no <=336.2) or (book_no>=336.2 and book_no<=338.17):
		hall_no = 3
		shelf_no = 10

	elif (book_no>=338.171 and book_no <=338.6) or (book_no>=338.6 and book_no<=338.9):
		hall_no = 3
		shelf_no = 11

	elif (book_no>=338.9 and book_no <=343) or (book_no>=344 and book_no<=362.1):
		hall_no = 3
		shelf_no = 12

	elif (book_no>=362.1 and book_no <=370.1) or (book_no>=370.2 and book_no<=375.4):
		hall_no = 3
		shelf_no = 13

	elif (book_no>=375.42 and book_no <=378) or (book_no>=380 and book_no<=400):
		hall_no = 3
		shelf_no = 14


	elif (book_no>=400 and book_no <=429) or (book_no>=430 and book_no<=499):
		hall_no = 3
		shelf_no = 15


	elif (book_no>=631.1 and book_no <=631.33) or (book_no>=630 and book_no<=631.2):
		hall_no = 4
		shelf_no = 1


	elif (book_no>=631.53 and book_no <=633.36) or (book_no>=633.4 and book_no<=637.1):
		hall_no = 4
		shelf_no = 2


	elif (book_no>=637.1 and book_no <=651.81) or (book_no>=652 and book_no<=658):
		hall_no = 4
		shelf_no = 3

	elif (book_no>=658 and book_no <=658.054) or (book_no>=658.054042 and book_no<=658.1552):
		hall_no = 4
		shelf_no = 4

	elif (book_no>=658.1553 and book_no <=658.315207) or (book_no>=658.32 and book_no<=658.403):
		hall_no = 4
		shelf_no = 5

	elif (book_no>=658.403 and book_no <=658.4083) or (book_no>=658.409 and book_no<=658.562):
		hall_no = 4
		shelf_no = 6

	elif (book_no>=658.562 and book_no <=658.8) or (book_no>=658.8 and book_no<=660):
		hall_no = 4
		shelf_no = 7

	elif (book_no>=660 and book_no <=660.281) or (book_no>=660.2812 and book_no<=660.2844):
		hall_no = 4
		shelf_no = 8

	elif (book_no>=660.2844 and book_no <=660.634) or (book_no>=660.65 and book_no<=663.4062):
		hall_no = 4
		shelf_no = 9


	elif (book_no>=629.3 and book_no <=629.8) or (book_no>=629.802 and book_no<=629.895):
		hall_no = 4
		shelf_no = 10

	else:
		hall_no = 3
		shelf_no = 7

	hall_1 = ""

	hall_3 = ""

	hall_4 = ""

	hall_all =  ""

	if hall_no == 1:
		hall_all = "CL-All.png"

		hall_3 = "CL-3_00.png"

		hall_4 = "CL-4_0.png"

		hall_1 = "CL-1_"+str(shelf_no)+".png"

	elif hall_no == 3:
		hall_all = "CL-All-1.png"

		hall_3 = "CL-3_"+str(shelf_no)+".png"

		hall_1 = "CL-1_0.png"

		hall_4 = "CL-4_0.png"

	elif hall_no == 4:
		hall_all = "CL-All-1.png"

		hall_3 = "CL-3_0.png"

		hall_1 = "CL-1_0.png"

		hall_4 = "CL-4_"+str(shelf_no)+".png"


	os.system("cp /home/chinmaya13/CodeFundo_2017/fb-messenger-bot/mapping_folder/images_1/"+hall_all+" /home/chinmaya13/CodeFundo_2017/fb-messenger-bot/mapping_folder/images/CL-All.png")
	os.system("cp /home/chinmaya13/CodeFundo_2017/fb-messenger-bot/mapping_folder/images_1/"+hall_1+" /home/chinmaya13/CodeFundo_2017/fb-messenger-bot/mapping_folder/images/CL-1.png")
	os.system("cp /home/chinmaya13/CodeFundo_2017/fb-messenger-bot/mapping_folder/images_1/"+hall_3+" /home/chinmaya13/CodeFundo_2017/fb-messenger-bot/mapping_folder/images/CL-3.png")
	os.system("cp /home/chinmaya13/CodeFundo_2017/fb-messenger-bot/mapping_folder/images_1/"+hall_4+" /home/chinmaya13/CodeFundo_2017/fb-messenger-bot/mapping_folder/images/CL-4.png")




# if __name__ == "__main__":main()