#!/usr/bin/env python
# coding: utf-8

# ## Diffraction Spectrum of Liquid-Crystal Polarization Gratings
# 
# As a final demonstration of mode decomposition, we compute the diffraction spectrum of a [liquid-crystal](https://en.wikipedia.org/wiki/Liquid_crystal) polarization grating. These types of beam splitters use [birefringence](https://en.wikipedia.org/wiki/Birefringence) to produce diffraction orders which are [circularly polarized](https://en.wikipedia.org/wiki/Circular_polarization). We will investigate two kinds of polarization gratings: (1) a homogeneous [uniaxial](https://en.wikipedia.org/wiki/Birefringence#Uniaxial_materials) grating (commonly known as a circular-polarization grating), and (2) a [twisted-nematic](https://en.wikipedia.org/wiki/Liquid_crystal#Chiral_phases) bilayer grating as described in [Optics Letters, Vol. 33, No. 20, pp. 2287-9, 2008](https://www.osapublishing.org/ol/abstract.cfm?uri=ol-33-20-2287) ([pdf](https://www.imagineoptix.com/cms/wp-content/uploads/2017/01/OL_08_Oh-broadband_PG.pdf)). The homogeneous uniaxial grating is just a special case of the twisted-nematic grating with a nematic [director](https://en.wikipedia.org/wiki/Liquid_crystal#Director) rotation angle of φ=0°.
# 
# A schematic of the grating geometry is shown below. The grating is a 2d slab in the *xy*-plane with two parameters: birefringence (Δn) and thickness (d). The twisted-nematic grating consists of two layers of thickness d each with equal and opposite rotation angles of φ=70° for the nematic director. Both gratings contain only three diffraction orders: m=0, ±1. The m=0 order is linearly polarized and the m=±1 orders are circularly polarized with opposite chirality. For the uniaxial grating, the diffraction efficiencies for a mode with wavelength λ can be computed analytically: η<sub>0</sub>=cos<sup>2</sup>(πΔnd/λ), η<sub>±1</sub>=0.5sin<sup>2</sup>(πΔnd/λ). The derivation of these formulas is presented in [Optics Letters, Vol. 24, No. 9, pp. 584-6, 1999](https://www.osapublishing.org/ol/abstract.cfm?uri=ol-24-9-584). We will verify these analytic results and also demonstrate that the twisted-nematic grating produces a broader bandwidth response for the ±1 orders than the homogeneous uniaxial grating. An important property of these polarization gratings for e.g. display applications is that for a circular-polarized input planewave and phase delay (Δnd/λ) of nearly 0.5, there is only a single diffraction order (+1 or -1) with *opposite* chiraity to that of the input. This is also demonstrated below.
# 
# ![](https://meep.readthedocs.io/en/latest/images/polarization_grating_schematic.png)
# 
# In this example, the input is a linear-polarized planewave pulse at normal incidence with center wavelength of λ=0.54 μm. The linear polarization is in the *yz*-plane with a rotation angle of 45° counter clockwise around the *x* axis. Two sets of mode coefficients are computed in the air region adjacent to the grating for each orthogonal polarization: `ODD_Z+EVEN_Y` and `EVEN_Z+ODD_Y`, which correspond to +k<sub>y</sub> + -k<sub>y</sub> (cosine) and +k<sub>y</sub> - -k<sub>y</sub> (sine) modes. From these coefficients for linear-polarized modes, the power in the circular-polarized modes can be computed: |ODD_Z+EVEN_Y|<sup>2</sup>+|EVEN_Z+ODD_Y|<sup>2</sup>. The power is identical for the two circular-polarized modes with opposite chiralities since the input is linearly polarized and at normal incidence. The transmittance for the diffraction orders are computed from the mode coefficients. As usual, this requires a separate normalization run to compute the power of the input planewave.
# 
# The main part of the script is the function `pol_grating` which computes the mode coefficients for a grating with thickness `d`, twisted-nematic rotation angle `ph`, and periodicity `gp`. The anisotropic permittivity of the grating is specified using the [material function](https://meep.readthedocs.io/en/latest/Python_User_Interface/#medium) `lc_mat` which involves a position-dependent rotation of the diagonal ε tensor about the *x*-axis. For φ=0°, the nematic director is oriented along the *z*-axis: E<sub>z</sub> has a larger permittivity than E<sub>y</sub> where the birefringence (Δn) is 0.159. The grating has a periodicity of Λ=6.5 μm in the *y* direction.

# In[1]:


import meep as mp
import math
import numpy as np
import matplotlib.pyplot as plt

resolution = 30        # pixels/μm

dpml = 1.0             # PML thickness
dsub = 1.0             # substrate thickness
dpad = 1.0             # padding thickness

k_point = mp.Vector3(0,0,0)

pml_layers = [mp.PML(thickness=dpml,direction=mp.X)]

n_0 = 1.55
delta_n = 0.159
epsilon_diag = mp.Matrix(mp.Vector3(n_0**2,0,0),mp.Vector3(0,n_0**2,0),mp.Vector3(0,0,(n_0+delta_n)**2))

wvl = 0.54             # center wavelength
fcen = 1/wvl           # center frequency

def pol_grating(d,ph,gp,nmode):
    sx = dpml+dsub+d+d+dpad+dpml
    sy = gp

    cell_size = mp.Vector3(sx,sy,0)

    # twist angle of nematic director; from equation 1b
    def phi(p):
        xx  = p.x-(-0.5*sx+dpml+dsub)
        if (xx >= 0) and (xx <= d):
            return math.pi*p.y/gp + ph*xx/d
        else:
            return math.pi*p.y/gp - ph*xx/d + 2*ph

    # return the anisotropic permittivity tensor for a uniaxial, twisted nematic liquid crystal
    def lc_mat(p):
        # rotation matrix for rotation around x axis
        Rx = mp.Matrix(mp.Vector3(1,0,0),mp.Vector3(0,math.cos(phi(p)),math.sin(phi(p))),mp.Vector3(0,-math.sin(phi(p)),math.cos(phi(p))))
        lc_epsilon = Rx * epsilon_diag * Rx.transpose()
        lc_epsilon_diag = mp.Vector3(lc_epsilon[0].x,lc_epsilon[1].y,lc_epsilon[2].z)
        lc_epsilon_offdiag = mp.Vector3(lc_epsilon[1].x,lc_epsilon[2].x,lc_epsilon[2].y)
        return mp.Medium(epsilon_diag=lc_epsilon_diag,epsilon_offdiag=lc_epsilon_offdiag)

    geometry = [mp.Block(center=mp.Vector3(-0.5*sx+0.5*(dpml+dsub)),size=mp.Vector3(dpml+dsub,mp.inf,mp.inf),material=mp.Medium(index=n_0)),
                mp.Block(center=mp.Vector3(-0.5*sx+dpml+dsub+d),size=mp.Vector3(2*d,mp.inf,mp.inf),material=lc_mat)]

    # linear-polarized planewave pulse source
    src_pt = mp.Vector3(-0.5*sx+dpml+0.3*dsub,0,0)
    sources = [mp.Source(mp.GaussianSource(fcen,fwidth=0.05*fcen), component=mp.Ez, center=src_pt, size=mp.Vector3(0,sy,0)),
               mp.Source(mp.GaussianSource(fcen,fwidth=0.05*fcen), component=mp.Ey, center=src_pt, size=mp.Vector3(0,sy,0))]

    sim = mp.Simulation(resolution=resolution,
                        cell_size=cell_size,
                        boundary_layers=pml_layers,
                        k_point=k_point,
                        sources=sources,
                        default_material=mp.Medium(index=n_0))

    tran_pt = mp.Vector3(0.5*sx-dpml-0.5*dpad,0,0)
    tran_flux = sim.add_flux(fcen, 0, 1, mp.FluxRegion(center=tran_pt, size=mp.Vector3(0,sy,0)))

    sim.run(until_after_sources=100)

    input_flux = mp.get_fluxes(tran_flux)
    input_flux_data = sim.get_flux_data(tran_flux)

    sim.reset_meep()

    sim = mp.Simulation(resolution=resolution,
                        cell_size=cell_size,
                        boundary_layers=pml_layers,
                        k_point=k_point,
                        sources=sources,
                        geometry=geometry)

    tran_flux = sim.add_flux(fcen, 0, 1, mp.FluxRegion(center=tran_pt, size=mp.Vector3(0,sy,0)))

    sim.run(until_after_sources=300)

    res1 = sim.get_eigenmode_coefficients(tran_flux, range(1,nmode+1), eig_parity=mp.ODD_Z+mp.EVEN_Y)
    res2 = sim.get_eigenmode_coefficients(tran_flux, range(1,nmode+1), eig_parity=mp.EVEN_Z+mp.ODD_Y)
    angles = [math.degrees(math.acos(kdom.x/fcen)) for kdom in res1.kdom]

    return input_flux[0], angles, res1.alpha[:,0,0], res2.alpha[:,0,0];


# The properties of the two gratings are computed over the thickness range of 0.1 to 3.4 μm corresponding to phase delays (Δnd/λ) of approximately 0 to 1.

# In[2]:


ph_uniaxial = 0               # chiral layer twist angle for uniaxial grating
ph_twisted = 70               # chiral layer twist angle for bilayer grating
gp = 6.5                      # grating period
nmode = 5                     # number of mode coefficients to compute
dd = np.arange(0.2,3.5,0.2)   # chiral layer thickness

m0_uniaxial = np.zeros(dd.size)
m1_uniaxial = np.zeros(dd.size)
ang_uniaxial = np.zeros(dd.size)

m0_twisted = np.zeros(dd.size)
m1_twisted = np.zeros(dd.size)
ang_twisted = np.zeros(dd.size)

for k in range(len(dd)):
    input_flux, angles, coeffs1, coeffs2 = pol_grating(0.5*dd[k],math.radians(ph_uniaxial),gp,nmode)
    tran = (abs(coeffs1)**2+abs(coeffs2)**2)/input_flux
    for m in range(nmode):
        print("tran (uniaxial):, {}, {:.2f}, {:.5f}".format(m,angles[m],tran[m]))
    m0_uniaxial[k] = tran[0]
    m1_uniaxial[k] = tran[1]
    ang_uniaxial[k] = angles[1]

    input_flux, angles, coeffs1, coeffs2 = pol_grating(dd[k],math.radians(ph_twisted),gp,nmode)
    tran = (abs(coeffs1)**2+abs(coeffs2)**2)/input_flux
    for m in range(nmode):
        print("tran (twisted):, {}, {:.2f}, {:.5f}".format(m,angles[m],tran[m]))
    m0_twisted[k] = tran[0]
    m1_twisted[k] = tran[1]
    ang_twisted[k] = angles[1]


# The diffraction spectra is plotted using the script below and shown in the accompanying figure.

# In[3]:


cos_angles = [math.cos(math.radians(t)) for t in ang_uniaxial]
tran = m0_uniaxial+2*m1_uniaxial
eff_m0 = m0_uniaxial/tran
eff_m1 = (2*m1_uniaxial/tran)/cos_angles

phase = delta_n*dd/wvl
eff_m0_analytic = [math.cos(math.pi*p)**2 for p in phase]
eff_m1_analytic = [math.sin(math.pi*p)**2 for p in phase]


# In[4]:


plt.figure(dpi=150)
plt.subplot(1,2,1)
plt.plot(phase,eff_m0,'bo-',clip_on=False,label='0th order (meep)')
plt.plot(phase,eff_m0_analytic,'b--',clip_on=False,label='0th order (analytic)')
plt.plot(phase,eff_m1,'ro-',clip_on=False,label='±1 orders (meep)')
plt.plot(phase,eff_m1_analytic,'r--',clip_on=False,label='±1 orders (analytic)')
plt.axis([0, 1.0, 0, 1])
plt.xticks([t for t in np.arange(0,1.2,0.2)])
plt.xlabel("phase delay Δnd/λ")
plt.ylabel("diffraction efficiency @ λ = 0.54 μm")
plt.legend(loc='center')
plt.title("homogeneous uniaxial grating")

cos_angles = [math.cos(math.radians(t)) for t in ang_twisted]
tran = m0_twisted+2*m1_twisted
eff_m0 = m0_twisted/tran
eff_m1 = (2*m1_twisted/tran)/cos_angles

plt.subplot(1,2,2)
plt.plot(phase,eff_m0,'bo-',clip_on=False,label='0th order (meep)')
plt.plot(phase,eff_m1,'ro-',clip_on=False,label='±1 orders (meep)')
plt.axis([0, 1.0, 0, 1])
plt.xticks([t for t in np.arange(0,1.2,0.2)])
plt.xlabel("phase delay Δnd/λ")
plt.ylabel("diffraction efficiency @ λ = 0.54 μm")
plt.legend(loc='center')
plt.title("bilayer twisted-nematic grating")

plt.tight_layout()
plt.show()


# The left figure shows good agreement between the simulation results and analytic theory for the homogeneous uniaxial grating. Approximately 6% of the power in the input planewave is lost due to reflection from the grating. This value is an average over all phase delays. The total transmittance is therefore around 94%. The twisted-nematic grating, with results shown in the right figure, produces ±1 diffraction orders with nearly-constant peak transmittance over a broader bandwidth around Δnd/λ=0.5 than the homogeneous uniaxial polarization grating. This is consistent with results from the reference. The average reflectance and transmittance for the twisted-nematic grating are similar to those for the homogeneous uniaxial grating.
# 
# Finally, we demonstrate that when Δnd/λ=0.5 a circular-polarized planewave input produces just a single ±1 diffraction order. To specify a E<sub>z</sub>+iE<sub>y</sub> circular-polarized planewave requires setting the `amplitude` of the E<sub>y</sub> source to an imaginary number (from its default of 1):
# 
# ```py
# sources = [mp.Source(mp.GaussianSource(fcen,fwidth=0.05*fcen), component=mp.Ez, center=src_pt, size=mp.Vector3(0,sy,0)),
#            mp.Source(mp.GaussianSource(fcen,fwidth=0.05*fcen), component=mp.Ey, center=src_pt, size=mp.Vector3(0,sy,0), amplitude=1j)]
# ```
# 
# Note that even though the J<sub>y</sub> current amplitude is complex in this example, only its real part is used and the resulting fields are therefore still real (the default).
# 
# The figure below shows a snapshot of E<sub>z</sub> within the cell for four different cases: phase delays (Δnd/λ) of 0.5 and 1.0, and planewave circular polarization of E<sub>z</sub>+iE<sub>y</sub> and E<sub>z</sub>-iE<sub>y</sub>. The empty regions on the cell sides are PMLs. The thin solid black line denotes the boundary between the grating (on the left) and air. As expected, for Δnd/λ=0.5 there is just a single ±1 diffraction order which depends on the chirality of the input planewave (this is not the case for a linear-polarized planewave). The angle of this diffracted order (±4.8°) agrees with the analytic result. Snapshots of E<sub>y</sub> are similar.
# 
# ![](https://meep.readthedocs.io/en/latest/images/polarization_grating_diffraction_orders.png)
