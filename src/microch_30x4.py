# CellModeller script for two bacterial colonies dividing in a channel
import random
from CellModeller.Regulation.ModuleRegulator import ModuleRegulator
from CellModeller.Biophysics.BacterialModels.CLBacterium import CLBacterium
import numpy
import math

max_cells = 10**3

cell_cols = {0:[0,1.0,0], 1:[1.0,0,0]} # RGB cell colours ... green and red
cell_lens = {0:2.0, 1:2.0} # target cell lengths ... 2 um
cell_growr = {0:0.035, 1:0.035} # growth rates - equivalent to divinding time of 20 mins

def get_x_coord(cell):
    # Finds x-coordinate of a cell
    return cell.pos[0]

def setup(sim):
    # Set biophysics and regulation models
    biophys = CLBacterium(sim,
        gamma=10, 
        jitter_z=False, 
        max_planes=2)

    # add the planes to set physical boundaries of cell growth
    # 4 micrometer width
    biophys.addPlane((0,2,0), (0,-1,0), 1.0)
    biophys.addPlane((0,-2,0), (0,1,0), 1.0)

    regul = ModuleRegulator(sim, sim.moduleName)

    # Only biophys and regulation
    sim.init(biophys, regul, None, None)

    # Specify the initial cells and their location in the simulation
    sim.addCell(cellType=0, pos=(1,0,0), dir=(1,0,0)) 
    sim.addCell(cellType=1, pos=(-1,0,0), dir=(1,0,0))

    # Simulation timestep is dt == 0.005 min == 0.3 s 
    sim.pickleSteps = 100 # Save every 3 minutes in real time. Same as in the experiment

def init(cell):
    # Specify mean and distribution of initial cell size
    cell.targetVol = cell_lens[cell.cellType]
    # Specify growth rate of cells
    cell.growthRate = random.uniform(0.5 * cell_growr[cell.cellType], 
        1.5 * cell_growr[cell.cellType])
    # Specify colour of cells
    cell.color = cell_cols[cell.cellType]

    # Initialize killFlag
    cell.killFlag = False

def update(cells):
    # Iterate through each cell and flag cells that reach target size for division
    # or remove cells from the simualtion that are out of the channel
    for (id, cell) in cells.items():
        if cell.volume > cell.targetVol:
            cell.divideFlag = True
        elif abs(get_x_coord(cell)) > 15: # Microchannel length: 30 microns
            cell.killFlag = True

def divide(parent, d1, d2):
    # Specify target cell size that triggers cell division
    d1.targetVol = cell_lens[parent.cellType] 
    d2.targetVol = cell_lens[parent.cellType]

    # Specify daugther growth rate
    d1.growthRate = random.uniform(0.5 * 0.035, 
        1.5 * 0.035)
    d2.growthRate = random.uniform(0.5 * 0.035, 
        1.5 * 0.035)

