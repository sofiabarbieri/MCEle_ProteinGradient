import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation
from matplotlib import animation
import numpy as np
from scipy import optimize
import os
from ROOT import *

point1 = [5, 20]
point2 = [45, 20]
x_values = [point1[0], point2[0]]
y_values = [point1[1], point2[1]]
class plot2D():
  
  def __init__(self, number, limits, limits_spheroid, v_mex5_slow, v_mex5_fast):
    
    self.klast = 0.
    self.profilelast = []
    self.x = [0] * number
    self.y = [0] * number
    self.limits = limits
    self.list_m_fit_pre = []
    self.number = number
    self.center_y = (limits_spheroid[1][1]-limits_spheroid[0][1])/2
    
    global fig, fig1, fig2, fig_id1, fig_id2, fig_id_ratio, fig_root_based, fig_movie
    fig = plt.figure()
    fig_id1 = plt.figure()
    fig_id_ratio = plt.figure()
    
    fig_root_based = plt.figure()


    fig.set_tight_layout(True)
    fig_id1.set_tight_layout(True)
    fig_id_ratio.set_tight_layout(True)
    fig_root_based.set_tight_layout(True)
    
    plt.grid(True)
    plt.subplots_adjust(hspace = 1,wspace = 0.6)

    self.ims_movie1 = []
    self.ims_movie2 = []
    self.data_movie_1 = []
    self.data_movie_2 = []
    

#   ROOT Stuff
    
    self.v_slow = v_mex5_slow
    self.v_fast = v_mex5_fast
    

  def Update(self, particles, sliceD, slice_depth):
    del self.x[:]
    del self.y[:]
    if (sliceD== True):
        for index, item in enumerate (particles):
            if (item.z > float(self.center_y)-float(slice_depth)/2. and item.z  < float(self.center_y)+float(slice_depth)/2.):
                    self.x.append(item.x)
                    self.y.append(item.y)
    else:
        for index, item in enumerate (particles):            
            self.x.append(item.x)
            self.y.append(item.y)
    self.Plot()
    print len(self.x)
    
  def UpdateCpp(self, x_list, y_list, z_list, sliceD, slice_depth):
    del self.x[:]
    del self.y[:]
    if (sliceD== True):
        for index, item in enumerate (x_list):
            if (z_list[index] > float(self.center_y)-float(slice_depth)/2. and z_list[index]  < float(self.center_y)+float(slice_depth)/2.):
                    self.x.append(x_list[index])
                    self.y.append(y_list[index])
    else:
        for index, item in enumerate (x_list):            
            self.x.append(x_list[index])
            self.y.append(y_list[index])
    self.Plot()
    
    
  def Plot(self):
    
    fig.clf()

    self.ax1 = fig.add_subplot(2,1,1)
    hist, xbins, ybins, im = self.ax1.hist2d(self.x, self.y, bins=self.limits[0][1], range=self.limits)
    self.ax1.set_title("2D distribution MEX-5") 
    self.ax1.set_xlabel("Long axis (um)")
    self.ax1.set_ylabel("Short axis (um)")
    fig.colorbar(im)
    oneD = []
    
    density = self.limits[0][1]/self.limits[0][1]
    

    self.ax1.plot(x_values, y_values)
    
    xbins_line = []
    for xbin in range (point1[0]/density, point2[0]/density):
      oneD.append((hist[xbin][point2[1]/density]))
      xbins_line.append(float(xbin-point1[0]/density))
    xbins = xbins[:xbins.shape[0]-1]
    xbins = xbins/np.max(xbins)
    xbins_line = xbins_line/np.max(xbins_line)
    xbins = xbins_line         

    
    oneD = oneD/np.max(oneD)
    
    self.profilelast = oneD
    
    self.ax2 = fig.add_subplot(2,2,3)
    self.ax2.plot(xbins, oneD)
    params, params_covariance = optimize.curve_fit(self.fit_func, xbins, oneD, bounds=((-np.inf, -np.inf), (np.inf,np.inf)))
    hist2 = self.ax2.plot(xbins,self.fit_func(xbins, params[0], params[1]), label='Fit')
    self.ax2.set_title(" MEX-5 gradient intensity")
    self.ax2.set_ylabel("Normal. intensity (a.u.)")
    self.ax2.set_xlabel("Normal. embryo length")

    self.list_m_fit_pre.append(params[0])
    
    self.klast = (params[0])


    t_pre = np.arange(len(self.list_m_fit_pre))
    self.ax3 = fig.add_subplot(2,2,4)
    self.ax3.plot(t_pre, self.list_m_fit_pre, marker='', linewidth=1, alpha=0.9)
    self.ax3.set_title("Slope vs time MEX-5")
    self.ax3.set_ylabel("Intensity gradient (dI/dx)")
    self.ax3.set_xlabel("Time (s)")


    fig.canvas.draw()

    plt.show(block=False)
    plt.pause(0.1)
        

    #
  def conc_calcCpp(self, X_list, Y_list, Z_list, id_list):
    
    
    fig_id1.clf()
    
    fig_id_ratio.clf()
    
    id0_slice = []
    id1_slice = []
    
    id0 = []
    id1 = []
    xbins_line = []
    
    x1 = [] 
    y1 = []
    x2 = [] 
    y2 = []
    x3 = [] 
    y3 = []
    
    for index, item in enumerate (X_list):
      if (id_list[index]==0):
        x1.append(X_list[index])
        y1.append(Y_list[index])
      elif (id_list[index]==1):
        x2.append(X_list[index])
        y2.append(Y_list[index])
      x3.append(X_list[index])
      y3.append(Y_list[index])

    
    self.ax_id0 = fig_id1.add_subplot(3,1,1)

    hist, xbins, ybins, im = self.ax_id0.hist2d(x1, y1, bins=self.limits[0][1], range=self.limits)
    self.ax_id0.set_title("2D concentration MEX-5s")
    self.ax_id0.set_xlabel("Long axis (um)")
    self.ax_id0.set_ylabel("Short axis (um)")
    fig_id1.colorbar(im)

 
    self.ax_id1 = fig_id1.add_subplot(3,1,2)
    hist1, xbins1, ybins1, im1 = self.ax_id1.hist2d(x2, y2, bins=self.limits[0][1], range=self.limits)
    self.ax_id1.set_title("2D concentration MEX-5f")
    self.ax_id1.set_xlabel("Long axis (um)")
    self.ax_id1.set_ylabel("Short axis (um)")
    fig_id1.colorbar(im1)

    self.ax_id2 = fig_id1.add_subplot(3,1,3)
    hist2, xbins2, ybins2, im2 = self.ax_id2.hist2d(x3, y3, bins=self.limits[0][1], range=self.limits)
    self.ax_id2.set_title("2D concentration MEX-5")
    self.ax_id2.set_xlabel("Long axis (um)")
    self.ax_id2.set_ylabel("Short axis (um)")
    fig_id1.colorbar(im2)


    self.data_movie_1 = hist2.T
    
    
    density = self.limits[0][1]/self.limits[0][1]


    for xbin in range (0, len(xbins)-1):
        id0_slice.append((hist[xbin][15/density]))
        id1_slice.append((hist1[xbin][15/density]))
        xbins_line.append(xbin)
        
    for xbin in range (0, len(xbins)-1):
        id0.append((sum(hist[xbin][:])))
        id1.append((sum(hist1[xbin][:])))

    ratio = np.divide(id0_slice, id1_slice)
    ratio2 = np.divide(id0, id1)
    

    self.ax_id_ratio = fig_id_ratio.add_subplot(3,2,1)
    self.ax_id_ratio.plot(xbins_line, ratio)
    self.ax_id_ratio.set_title("Ratio, integrat. on Z")
    self.ax_id_ratio.set_ylabel("Ratio MEX-5s/MEX-5f")
    self.ax_id_ratio.set_xlabel("Embryo length (um)")
    
    self.ax_id_ratio2 = fig_id_ratio.add_subplot(3,2,2)
    self.ax_id_ratio2.plot(xbins_line, ratio2)
    self.ax_id_ratio2.set_title("Ratio, integrat. on Y and Z")
    self.ax_id_ratio2.set_ylabel("Ratio MEX-5s/MEX-5f")
    self.ax_id_ratio2.set_xlabel("Embryo length (um)")   
    
    self.ax_id_conc = fig_id_ratio.add_subplot(3,2,3)
    self.ax_id_conc.plot(xbins_line, id0, 'r', label="MEX-5s")
    self.ax_id_conc.plot(xbins_line, id1, 'b', label="MEX-5f")
    self.ax_id_conc.set_title("# MEX-5 p.les, integrat. on Y and Z")
    self.ax_id_conc.set_ylabel("# p.les MEX-5s , MEX-5f")
    self.ax_id_conc.set_xlabel("Embryo length (um)")
    self.ax_id_conc.legend(loc="upper right", frameon=False)

    self.ax_id_slice = fig_id_ratio.add_subplot(3,2,4)
    self.ax_id_slice.plot(xbins_line, id0_slice, 'r', label="MEX-5s")
    self.ax_id_slice.plot(xbins_line, id1_slice, 'b', label="MEX-5f")
    self.ax_id_slice.set_title("# MEX-5 p.les, integrat. on Z")
    self.ax_id_slice.set_ylabel("# p.les MEX-5s , MEX-5f")
    self.ax_id_slice.set_xlabel("Embryo length (um)")
    self.ax_id_slice.legend(loc="upper right", frameon=False)
    
    mex5_slow = np.array(id0_slice)/self.number
    mex5_fast = np.array(id1_slice)/self.number
    mex5_tot = mex5_slow+mex5_fast
    
    self.ax_id_slice_conc = fig_id_ratio.add_subplot(3,2,5)
    self.ax_id_slice_conc.plot(xbins_line, mex5_tot, 'g', label="Tot. concentr.")
    self.ax_id_slice_conc.plot(xbins_line, mex5_slow, 'r', label="MEX-5s")
    self.ax_id_slice_conc.plot(xbins_line, mex5_fast, 'b', label="MEX-55f")

    self.ax_id_slice_conc.set_title("MEX-5 concentrat., integrat. on Z")
    self.ax_id_slice_conc.set_ylabel("Conc. MEX-5s + MEX-5f")
    self.ax_id_slice_conc.set_xlabel("Embryo length (um)")
    self.ax_id_slice_conc.legend(loc="upper right", frameon=False)    
    
    fig_id_ratio.canvas.draw()

        #root stuff
    self.histo3DSlow = TH3F("plot3D-Slow", "plot3D-Slow", 50, 0, 50, 30 , 0, 30, 30, 0, 30 )
    self.histo3DFast = TH3F("plot3D-Fast", "plot3D-Fast", 50, 0, 50, 30 , 0, 30, 30, 0, 30 )

    x_3d = np.array(X_list)
    y_3d = np.array(Y_list)
    z_3d = np.array(Z_list)
    for xbin in range (0, len(x_3d)):
      if (id_list[xbin]==0):
        self.histo3DSlow.Fill(x_3d[xbin], y_3d[xbin], z_3d[xbin] )
      else:
        self.histo3DFast.Fill(x_3d[xbin], y_3d[xbin], z_3d[xbin] )


    slow_content = []
    fast_content = []
    for x_bin in range (1, 51):
       slow_content.append(self.histo3DSlow.GetBinContent(x_bin,15,15))
       fast_content.append(self.histo3DFast.GetBinContent(x_bin,15,15))

    max_arr = np.array(slow_content)+np.array(fast_content)
    
    self.data_movie_2 = max_arr/np.max(max_arr)

    fig_root_based.clf()
    
    ratio3 = np.divide(slow_content, fast_content)
    

    self.ax_id_ratio3 = fig_root_based.add_subplot(2,2,1)
    self.ax_id_ratio3.plot(xbins_line, ratio3)
    self.ax_id_ratio3.set_title("Ratio, Central Voxel")
    self.ax_id_ratio3.set_ylabel("Ratio MEX-5s/MEX-5f")
    self.ax_id_ratio3.set_xlabel("Embryo length (um)")
    
    
    v_average = (np.array(slow_content)*self.v_slow+np.array(fast_content)*self.v_fast)/(np.array(slow_content)+np.array(fast_content))
    
    conc_root_mex5_slow = np.array(slow_content)/self.number
    conc_root_mex5_fast = np.array(fast_content)/self.number
    
    self.ax_id_conc_root = fig_root_based.add_subplot(2,2,2)
    self.ax_id_conc_root.plot(xbins_line, conc_root_mex5_slow, 'r', label="MEX-5 slow")
    self.ax_id_conc_root.plot(xbins_line, conc_root_mex5_fast, 'b', label="MEX-5 fast")
    self.ax_id_conc_root.set_title("MEX-5 concentr.,  Central voxel")
    self.ax_id_conc_root.set_ylabel("Concentr. MEX-5s , MEX-5f")
    self.ax_id_conc_root.set_xlabel("Embryo length (um)")
    self.ax_id_conc_root.legend(loc="upper right", frameon=False)
    
    
    
    self.av_velocity = fig_root_based.add_subplot(2,2,3)
    self.av_velocity.plot(xbins_line, v_average)
    self.av_velocity.set_title("Mean MEX-5 velocity, Central Voxel")
    self.av_velocity.set_ylabel("Mean velocity MEX-5s, MEX-5f")
    self.av_velocity.set_xlabel("Embryo length (um)")
    
    
    fig_root_based.canvas.draw()
    
    plt.show(block=False)
    plt.pause(0.1)
    
    return ratio2.tolist(), conc_root_mex5_slow.tolist(), conc_root_mex5_fast.tolist(), v_average.tolist()
  
  def FillDrawMovie(self):
    self.ims_movie1.append(self.data_movie_1)
    self.ims_movie2.append(self.data_movie_2)

  def DrawMovie(self, path):

    fig, ax=plt.subplots()
    container = []

    for i in range(len(self.ims_movie1)):
        container.append([plt.imshow(self.ims_movie1[i])])
    im_ani = animation.ArtistAnimation(fig, container, interval=50, blit=False)
    im_ani.save(os.path.join(path,'2DMex5.gif'), writer='imagemagick', fps=10, dpi=50)

    fig2, a2x=plt.subplots()
    container2 = []

    for i in range(len(self.ims_movie2)):
        plotty, = a2x.plot(self.ims_movie2[i], color='blue')
        container2.append([plotty])
    im_ani2 = animation.ArtistAnimation(fig2, container2, interval=50, blit=False)
    im_ani2.save(os.path.join(path,'Gradient.gif'), writer='imagemagick', fps=10, dpi=50)
    print "done"
    
    plt.show(block=False)
    
  def fit_func(self, x, a, b):
    return (a*x+b)
