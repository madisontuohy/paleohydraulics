#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 14:56:56 2024

@author: madisontuohy
"""

import math

def calculate_mean_velocity(d_s, d_w, D_50, sigma_g, g, h_o, w_o, nu):
    """
    Calculate mean flow velocity using the Herget et al. (2013) regression model.
    
    Parameters:
    - d_s: Scour depth (m)
    - d_w: Water depth (m)
    - D_50: Median grain size (m)
    - sigma_g: Sediment sorting coefficient
    - g: Gravitational acceleration (m/s^2)
    - h_o: Obstacle height (m)
    - w_o: Obstacle width (m)
    - nu: Kinematic viscosity (m^2/s) ~ 1.3e-6 at 10°C
    
    Returns:
    - U_m: Mean flow velocity (m/s)
    """
    # Calculate equivalent length of obstacle frontal area
    L_A = (h_o ** (2 / 3)) * (w_o ** (1 / 3))

    # Regression model equation
    log_Um = 0.46 + 0.326 * math.log10((d_s * d_w * D_50 * sigma_g * g) / (L_A * nu))
    
    # Convert back to linear scale
    U_m = 10 ** log_Um
    return U_m

def calculate_velocity_from_dunes(L, H, D_50, Fr=0.6, g=9.81):
    """
    Calculate flow velocity using gravel dune dimensions and Froude number.
    
    Parameters:
    - L: Dune length (m)
    - H: Dune height (m)
    - D_50: Median grain size (m)
    - Fr: Froude number (default 0.6 for subcritical flow)
    - g: Gravitational acceleration (m/s^2)
    
    Returns:
    - U: Mean flow velocity (m/s)
    - h: Water depth estimated from dune length (m)
    - H_L_ratio: Dune steepness (H/L)
    """
    # Step 1: Estimate water depth from dune length
    h = L / 10  # Empirical scaling for gravel dunes
    
    # Step 2: Calculate mean flow velocity using Froude number
    U = Fr * math.sqrt(g * h)
    
    # Step 3: Dune steepness (H/L)
    H_L_ratio = H / L
    
    return U, h, H_L_ratio

if __name__ == "__main__":
    # --- DUNE CODE INPUT PARAMETERS ---
    L = (193 + 166 + 205) / 3      # Dune length in meters
    H = (245.365 - 239.871)        # Dune height in meters
    D_50 = 0.05  # Median grain size in meters
    Fr = 0.6     # Froude number (typical range: 0.4-0.75 for gravel dunes)

    # --- CALCULATE VELOCITY AND STEEPNESS ---
    U_dune, h_dune, H_L_ratio = calculate_velocity_from_dunes(L, H, D_50, Fr)

    # --- OUTPUT DUNE CODE RESULTS ---
    print(f"Estimated water depth (h) from dunes: {h_dune:.2f} m")
    print(f"Mean flow velocity (U) from dunes: {U_dune:.2f} m/s")
    print(f"Dune steepness (H/L): {H_L_ratio:.3f}")

    # --- SCOUR MARK INPUT PARAMETERS (USING DUNE h AS WATER DEPTH) ---
    d_s = (333.9 - 331.5)  # Scour depth in meters (From DEM)
    d_w = h_dune  # Water depth calculated from dune code
    sigma_g = 1.5  # Sediment sorting coefficient (use ~1.5 if unknown)
    g = 9.81  # Gravitational acceleration (m/s^2)
    h_o = (341.7 - 333.5)  # Obstacle height in meters (From DEM)
    w_o = 16.2  # Obstacle width in meters (From DEM)
    nu = 1.0e-3  # Kinematic viscosity of water at 10°C (m^2/s)

    # --- CALCULATE MEAN VELOCITY FROM SCOUR MARK ---
    U_scour = calculate_mean_velocity(d_s, d_w, D_50, sigma_g, g, h_o, w_o, nu)

    # --- OUTPUT SCOUR MARK RESULTS ---
    print(f"The calculated mean flow velocity (U_m) from scour mark: {U_scour:.2f} m/s")
