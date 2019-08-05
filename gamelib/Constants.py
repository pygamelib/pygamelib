"""
Accessible constants are the following:

General purpose:
 * HAC_GAME_LIB_VERSION 

Directions:
 * UP     
 * DOWN   
 * LEFT   
 * RIGHT  
 * DRUP   
 * DRDOWN 
 * DLUP   
 * DLDOWN 

Permissions:
 * PLAYER_AUTHORIZED       
 * NPC_AUTHORIZED          
 * ALL_PLAYABLE_AUTHORIZED 
 * NONE_AUTHORIZED         

UI positions:
 * POS_TOP                 
 * POS_BOTTOM              
 * ORIENTATION_HORIZONTAL  
 * ORIENTATION_VERTICAL   

Actuators states:
 * ACT_RUNNING
 * ACT_PAUSED
 * ACT_STOPPED 

"""

# Main version
HAC_GAME_LIB_VERSION = '2019.5a7'
# Directions
UP     = 10000001
DOWN   = 10000010
LEFT   = 10000011
RIGHT  = 10000100
DRUP   = 10000101
DRDOWN = 10000110
DLUP   = 10000111
DLDOWN = 10001000

# Permissions
PLAYER_AUTHORIZED       = 10001001
NPC_AUTHORIZED          = 10001010
ALL_PLAYABLE_AUTHORIZED = 10001011
NONE_AUTHORIZED         = 10001100

# UI positions
POS_TOP                 = 10001101
POS_BOTTOM              = 10001110
ORIENTATION_HORIZONTAL  = 10001111
ORIENTATION_VERTICAL    = 10010000


# Actuators states
ACT_RUNNING             = 10010001
ACT_PAUSED              = 10010010
ACT_STOPPED             = 10010011