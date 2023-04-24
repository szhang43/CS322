"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#

def calc_hour(time): 
   # converts hours into time and minutes as a tuple
   time *= 60
   hour = 0
   while (time >= 60): 
      time -= 60
      hour += 1
   return hour, round(time)
   
def calc_time(my_dict, control_dist_km, brevet_dist_km = None, brevet_start_time = None):
   time = 0 # Keeps track of the total time
   dis_left = control_dist_km # the distance left

   for i in my_dict: # for looping through the dictionary being passed in
      section_len = i[1] - i[0] # section length: 200 - 0, 400 - 200, 600 - 400 , etc
      if section_len <= dis_left: # checking if the section length is <= the total distance left
         time += section_len / my_dict[i] # adding the time computed with the approprite speed
         dis_left -= section_len # subtracting the amount traveled from distance left
      else:  # once the section length is greater than distance left
         time = time +( (control_dist_km - i[0]) / my_dict[i]) # add the last stage to the time
         dis_left -= control_dist_km - i[0] # subtract the distance left 
         break # break and return 
   return time # return the accumulated time calculated

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
   """
   Args:
      control_dist_km:  number, control distance in kilometers
      brevet_dist_km: number, nominal distance of the brevet
         in kilometers, which must be one of 200, 300, 400, 600,
         or 1000 (the only official ACP brevet distances)
      brevet_start_time:  An arrow object
   Returns:
      An arrow object indicating the control open time.
      This will be in the same time zone as the brevet start time.
   """
   _max = {(0, 200) : 34, (200, 400) : 32, (400, 600) : 30, 
            (600, 1000) : 28, (1000, 1300) : 26} # maximum speed limits
   
   # Clipping
   if control_dist_km < 1: # if control distance is less than one, then distance is 0
      control_dist_km = 0
   if control_dist_km > brevet_dist_km: # set to brevet distance if control distance is greater
      control_dist_km = brevet_dist_km

   time = calc_time(_max, control_dist_km) # call the time calc time function, computes time in hours
   # print("Open Time")
   # print("")
   hour, mins = calc_hour(time) # call calc hour function to format time into hour, mins
   # print("Open Time")
   # print(f"Hours: {hour}, Minutes: {mins}")
   open_time = brevet_start_time.shift(hours=hour, minutes = mins) # shift starting from the start time
   # print(open_time)
   return open_time # return shifted time


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
   """
   Args:
      control_dist_km:  number, control distance in kilometers
         brevet_dist_km: number, nominal distance of the brevet
         in kilometers, which must be one of 200, 300, 400, 600, or 1000
         (the only official ACP brevet distances)
      brevet_start_time:  An arrow object
   Returns:
      An arrow object indicating the control close time.
      This will be in the same time zone as the brevet start time.
   """
   _min = {(0,600):15, (600, 1000) : 11.428, (1000, 1300): 13.333}
   end_time = {200: 13.5, 300: 20, 400: 27, 600:40, 1000:75} # minimum speed
  
   # time = calc_time(_min, control_dist_km)
   time = 0 # accumulated time 
   dis_left = control_dist_km # setting distance left to control time 

   # Clipping
   if control_dist_km < 1: # set control distance to 0 if it is <= 0
      dis_left = 0
   if control_dist_km > brevet_dist_km: # set control distance to brevet distance if it is greater than brevet
      control_dist_km = brevet_dist_km

   # set the close time when control is 0
   if dis_left == 0: # ends exactly one hour later
      time += 1 # adding 1 hour to time
   # set the closing time according to the brevet distance
   

   if dis_left <= 60: # Special case for when the start of the race is between 0 to 60 km
      time = (dis_left / 20) + 1 # special case, minimum speed it 20 plus 1 hour
      hour, mins = calc_hour(time) # call calc hour to format to hour , mins
      # print("Close Time")
      # print(f"Hours: {hour}, Minutes: {mins}")
      close_time = brevet_start_time.shift(hours=hour, minutes = mins) # shift the time from start time
      # print("Close time is:", close_time)
      # print(hour, mins)
      return close_time # return shifted time

   if control_dist_km == brevet_dist_km: # checks for the total brevet distance rade length
      # print(control_dist_km)
      time = end_time[brevet_dist_km] # total race time based on distance is set instead of the standard
      hour, mins = calc_hour(time) # convert to hour, mins format
      # print("Close Time")
      # print(f"Hours: {hour}, Minutes: {mins}")
      close_time = brevet_start_time.shift(hours=hour, minutes = mins) # shift close time from start time
      # print("Close time is:", close_time)
      # print(hour, mins)
      return close_time # return shifted time for the end of the race
   
   time = calc_time(_min, dis_left) # otherswise, calculate as normal with calc time function returning hour
 
   
   hour, mins = calc_hour(time) # convert time to hours, min
   # print("Close Time")
   # print(f"Hours: {hour}, Minutes: {mins}")
   close_time = brevet_start_time.shift(hours=hour, minutes = mins) # shift the time from start time to close time
   # print("Close time is:", close_time)
   # print(hour, mins)
   return close_time # return shifted time
   
# if __name__ == "__main__":
#    t = arrow.get('2023-02-16T00:00:00')

   
  

   