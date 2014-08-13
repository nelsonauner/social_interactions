engage_list = []
#These are global, so be careful. 
background_colour = (255,255,255)
room_1 = 200
room_2 = 600

(width, height) = (800, 800)
LIME = (153, 255, 0) 
drag = 0.999
elasticity = 1
#gravity = (math.pi, 0.002)
#create conferences here. 
conferences = False
tolerance = 20 #How close to be to target? 
prob_phone = .5  #probability of using phone vs. roaming the conference, if spontaneously get bored
prob_roam_to_phone = .01
prob_phone_to_roam = .1
duration_phone = 5 #average duration of phone use
walking_speed = 5
engage_distance = 1.5 # (distance required to engage)