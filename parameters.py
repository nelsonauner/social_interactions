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
tolerance = 20 #How close to be to assigned goal to register (in pixels..) 
prob_phone = .4  #probability of using phone vs. roaming the conference, if spontaneously get bored
prob_roam_to_phone = .002  #if roaming, spontaneously use phone? 
prob_phone_to_roam = .001  #if on phone, probability to stop?
duration_phone = 5 #not used..
walking_speed = 5
engage_distance = 1.5 # (distance required to engage)
number_of_particles = 150
phone_penalty = 5 #harder to talk to someone when you're on the phone
friendly_parameter = 5 #the higher it is, the more likely you are to talk to someone less famous/outside of your group
number_of_groups = 3
affinity_parameter = 5 #talk to your group, mostly