import examples_includes

# First import the Utils module
import gamelib.Utils as Utils

# Then get creative!

# you directly print colored messages:
print("France flag is "+Utils.blue_bright('blue ')+Utils.white_bright('white ')+Utils.red_bright('red')+"!")

# Each color function has 3 variations : regular, dim and bright
print( Utils.yellow_dim('This is dim.')+Utils.yellow(' This is regular.')+Utils.yellow_bright(' This is bright.') )

# Now, the color functions are just that: functions. So you can store the results in a variable and use them:
flashymagy = Utils.magenta_bright('This is a rather flashy magenta...')

print('Now that is a colored message in a variable: '+flashymagy)