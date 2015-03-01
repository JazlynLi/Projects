def reference():
	for n in range (0, 60):
		if possibility > 0.5:
			n += 1
		else:
			return n
	int reference[][] = int[n][]
	for i in range(0, n):
		num_roll, poss = highest_possibility(i, num_samples) # number of rolls that has the highest possibility
	return reference[][]

def baseline(score, num_rolls):
	ref[][] = reference[][]
	# length = len.ref
	loop = 100//len.ref
	for i in range(0, loop):
		a = 100 - (loop + 1)*len.ref
		b = 100 - loop*len.ref  
		for k in range(a, b):
			num_rolls = reference[len.ref - k]
			plus = int(roll_dice(nium_rolls, dice))
			k += plus
			score += plus

	baseline[] = 

			

def highest_possibility(n, num_samples = 1000):
	poss = 0
	difference = n
	for i in range(1, 10):
		k = 0
		total = 0
		while k < num_samples:
			k += 1
			total += roll_dice(i)
		temp_poss = total/num_samples
		difference = abs(temp_poss - n)
		if difference < n:
			poss = temp_poss
			num_roll = i
	return num_roll, poss


