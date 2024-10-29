from numpy import *
from matplotlib.pyplot import *
import os, glob, re #for handling files
import matplotlib.image as mpimg

timeseries_offset = 0.25
timeseries_edge = 30
speedToAnalyze = 15.6



#load the offsets
offsets = loadtxt('casestudy_data/road_positions.txt')
offsets+=0.25#adjust for initial offset in world file
print("offsets are:")
print(offsets)

maxRoll90 = zeros(len(offsets))
maxTq90 = zeros(len(offsets))
maxSteer90 = zeros(len(offsets))
maxRoll30 = zeros(len(offsets))
maxTq30 = zeros(len(offsets))
maxSteer30 = zeros(len(offsets))
success30 = zeros(len(offsets))
success90 = zeros(len(offsets))

# figure()
for filename in glob.glob('casestudy_data/safetyedge_data_offset_*.txt'):
   with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
      print(filename)
      #split filename to determine what kind of test this was
      fname_split = filename[0:-4].split('_')
      print(fname_split)
      #what offset is this
      offsetind = int(fname_split[4])
      #what slant is this
      if(len(fname_split)==9):
          slantnow = int(fname_split[6])
          speednow = float(fname_split[8])/10.0
      else:
          speednow=10
          slantnow = int(fname_split[6])
      #give us the data
      data = loadtxt(filename,delimiter=",")
      if((speednow==speedToAnalyze) and (offsets[offsetind]==timeseries_offset) and (slantnow == timeseries_edge) ):
          fig3 = figure(figsize=(8,8),dpi=100)
          subplot(3,1,1)
          plot(data[:,0],data[:,1],'k')
          ylabel('Steer Torque (Nm)')
          title('Speed: '+str(speedToAnalyze)+' m/s; offset: '+str(offsets[offsetind])+'m; edge angle: '+str(slantnow)+' deg')
          subplot(3,1,2)
          plot(data[:,0],data[:,4],'k')
          ylabel('Steer Angle (rad)')
          subplot(3,1,3)
          plot(data[:,0],data[:,3],'k')
          ylabel('Roll Angle (rad)')
          xlabel('Time (s)')
          fig3.tight_layout()
          savefig("Figures/5_casestudy_timeseries_speed_"+str(speedToAnalyze*10)+'_offset_'+str(offsetind)+'_edge_'+str(slantnow)+".png",dpi=1000)


      # data file structure:
      #str(simtime)+","+str(T)+","+str(U)+","+str(roll)+","+str(steerangle)+","+str(rollRate)+","+str(steerRate)+","+str(rollInt)+","+str(stepVal)+","+str(yaw)+","+str(latPos)+"\r\n")
      print(slantnow,offsetind)
      maxtq = max(abs(data[:,1]))
      maxsteer = max(abs(data[:,4]))
      maxroll = max(abs(data[:,3]))
      success = maxroll<1.57 #did the vehicle fall over or not
      print(maxtq,maxsteer,maxroll)
      if(slantnow == 90 and speednow==speedToAnalyze):
          print("analyzing Speed "+str(speednow)+" slant "+str(slantnow)+" offset "+str(offsetind))
          if(success):
              maxTq90[offsetind] = maxtq
              maxSteer90[offsetind] = maxsteer
              maxRoll90[offsetind] = maxroll
          else:
              maxTq90[offsetind] = NaN
              maxSteer90[offsetind] = NaN
              maxRoll90[offsetind] = NaN
          success90[offsetind] = success
          # if(maxroll<1):
          #     subplot(3,2,1)
          #     plot(data[:,0],data[:,1],'k')
          #     xlabel('time (s)')

      elif(slantnow==30):
          if(success):
              maxTq30[offsetind] = maxtq
              maxSteer30[offsetind] = maxsteer
              maxRoll30[offsetind] = maxroll
          else:
              maxTq30[offsetind] = NaN
              maxSteer30[offsetind] = NaN
              maxRoll30[offsetind] = NaN
          success30[offsetind] = success

fig1 = figure(figsize=(16, 4), dpi=100)

subplot(1,4,1)
### FOR SUCCESS MATRIX USE BELOW
# plot(offsets,success90,'k-o',offsets,success30,'r-x',markerfacecolor='none',mew=2,markersize=12)
# grid('on')
# xlabel('edge lateral offset (m)',fontsize=14)
# ylabel('Success (0=Failure)',fontsize=14)
# legend(['90 degree edge','30 degree edge'],loc='right')
# title('a',fontsize=14)
####FOR EXAMPLE IMAGE USE BELOW
img=mpimg.imread('Figures/5_safetyedge_world_traversing.png')
imshow(img)
axis('off')
title('a',fontsize=14)

subplot(1,4,2)
axis('on')
plot(offsets,maxTq90,'ko',offsets,maxTq30,'rx',markerfacecolor='none',mew=2,markersize=12)
grid('on')
legend(['90 degree edge','30 degree edge'])
xlabel('edge lateral offset (m)',fontsize=14)
ylabel('maximum steer torque (Nm)',fontsize=14)
title('b',fontsize=14)
# legend(['90 degree edge','30 degree edge'])

# figure()
subplot(1,4,3)
plot(offsets,maxSteer90*180/pi,'ko',offsets,maxSteer30*180/pi,'rx',markerfacecolor='none',mew=2,markersize=12)
xlabel('edge lateral offset (m)',fontsize=14)
ylabel('maximum steer angle (degrees)',fontsize=14)
grid('on')
title('c',fontsize=14)
# legend(['90 degree edge','30 degree edge'])

# figure()
subplot(1,4,4)
plot(offsets,maxRoll90*180/pi,'ko',offsets,maxRoll30*180/pi,'rx',markerfacecolor='none',mew=2,markersize=12)
xlabel('edge lateral offset (m)',fontsize=14)
ylabel('maximum Roll angle (degrees)',fontsize=14)
grid('on')
title('d',fontsize=14)

fig1.tight_layout()
savefig("Figures/5_casestudy_panel1_speed_"+str(speedToAnalyze*10)+".png",dpi=1000)


fig2 = figure(figsize=(12,8), dpi=100)
title("Lane changes over 3 inch transition at "+str(speedToAnalyze)+" m/s")
subplot(2,2,1)
### FOR SUCCESS MATRIX USE BELOW
plot(offsets,success90,'k-o',offsets,success30,'r-x',markerfacecolor='none',mew=2,markersize=12)
grid('on')
xlabel('edge lateral offset (m)',fontsize=14)
ylabel('Success (0=Failure)',fontsize=14)
legend(['90 degree edge','30 degree edge'],loc='right')
# title('',fontsize=14)
####FOR EXAMPLE IMAGE USE BELOW
# img=mpimg.imread('Figures/5_safetyedge_world_traversing.png')
# imshow(img)
# axis('off')
# title('a',fontsize=14)

subplot(2,2,2)
axis('on')
plot(offsets,maxTq90,'ko',offsets,maxTq30,'rx',markerfacecolor='none',mew=2,markersize=12)
grid('on')
legend(['90 degree edge','30 degree edge'])
xlabel('edge lateral offset (m)',fontsize=14)
ylabel('maximum steer torque (Nm)',fontsize=14)
title('b',fontsize=14)
# legend(['90 degree edge','30 degree edge'])

# figure()
subplot(2,2,3)
plot(offsets,maxSteer90*180/pi,'ko',offsets,maxSteer30*180/pi,'rx',markerfacecolor='none',mew=2,markersize=12)
xlabel('edge lateral offset (m)',fontsize=14)
ylabel('maximum steer angle (degrees)',fontsize=14)
grid('on')
# title('c',fontsize=14)
# legend(['90 degree edge','30 degree edge'])

# figure()
subplot(2,2,4)
plot(offsets,maxRoll90*180/pi,'ko',offsets,maxRoll30*180/pi,'rx',markerfacecolor='none',mew=2,markersize=12)
xlabel('edge lateral offset (m)',fontsize=14)
ylabel('maximum Roll angle (degrees)',fontsize=14)
grid('on')
# title('d',fontsize=14)

fig2.tight_layout()
savefig("Figures/5_casestudy_presentation_speed"+str(speedToAnalyze*10)+".png",dpi=1000)



show()
