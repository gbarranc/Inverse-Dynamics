import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QGridLayout, QWidget
import pyqtgraph.opengl as gl
import numpy as np
import ForwardKinematics

#Create widgets to display arm in 3D space
#Links and rotations are currently arbitrary and defined at the bottom
class Main_Window(QtWidgets.QMainWindow):
    def __init__(self, cords, Acceleration_3D):
        super().__init__()

        #inputs taken as whole matrix
        self.cords = cords
        self.Acceleration_3D = Acceleration_3D

        #vualah
        self.layout = QGridLayout()
        self.box = QWidget()
        self.box.setLayout(self.layout)
        self.setCentralWidget(self.box)

        self.box.setWindowTitle('3D Vector Space')
        self.setGeometry(100, 100, 1200, 1000)

        self.Setup_3D()
        self.Setup_2D()

        self.Update_2D()

        #time to update
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.Remove_Nodes)
        self.timer.timeout.connect(self.Update_3D)
        self.timer.start(50)

    def Setup_3D(self):
        self.view3D = gl.GLViewWidget()

        axis = gl.GLAxisItem(size=pg.Vector(10, 10, 10))
        self.view3D.addItem(axis)

        self.view3D.opts['distance'] = 15
        self.layout.addWidget(self.view3D, 0, 0)

        # Create coordinate grids
        self.xgrid = gl.GLGridItem()
        self.ygrid = gl.GLGridItem()
        self.zgrid = gl.GLGridItem()

        # Rotationally offset grids to align with axes
        self.xgrid.rotate(90, 0, 1, 0)  # Y-axis
        self.ygrid.rotate(90, 1, 0, 0)  # X-axis

        # Add grids to window
        self.view3D.addItem(self.xgrid)
        self.view3D.addItem(self.ygrid)
        self.view3D.addItem(self.zgrid)

    def Setup_2D(self):
        self.view2D_Q1 = pg.PlotWidget()
        self.view2D_Q2 = pg.PlotWidget()
        self.view2D_Q3 = pg.PlotWidget()

        self.layout.addWidget(self.view2D_Q1, 0, 1)
        self.layout.addWidget(self.view2D_Q2, 1, 0)
        self.layout.addWidget(self.view2D_Q3, 1, 1)

        #range is arbitrary; should update once actual actuated members are added so it does not escape the bounds
        self.view2D_Q1.setTitle("ax", color="b", size="15pt")
        self.view2D_Q1.showGrid(x=True, y=True)
        self.view2D_Q1.setXRange(0, 5)
        self.view2D_Q1.setYRange(0, 20)

        self.view2D_Q2.setTitle("ay", color="y", size="15pt")
        self.view2D_Q2.showGrid(x=True, y=True)
        self.view2D_Q2.setXRange(0, 5)
        self.view2D_Q2.setYRange(0, 20)

        self.view2D_Q3.setTitle("az", color="g", size="15pt")
        self.view2D_Q3.showGrid(x=True, y=True)
        self.view2D_Q3.setXRange(0, 5)
        self.view2D_Q3.setYRange(0, 20)

    def Remove_Nodes(self):
        try:
            self.view3D.removeItem(self.links)
            self.view3D.removeItem(self.joints)
        except:
            pass

    def Update_3D(self):
        #add links and joints; automated wrt cords matrix
        self.links = gl.GLLinePlotItem(pos=self.cords, color=(1, 0, 0, 1), width=3)

        #note: would be cool to make the color as a function of stress tensor at the respective joint; i.e. red joint = bad
        self.joints = gl.GLScatterPlotItem(pos=self.cords, color=(1, 1, 1, 1), size=10)
        # Add to view
        self.view3D.addItem(self.links)
        self.view3D.addItem(self.joints)

    def Update_2D(self):

        #2D plots are currently arbitarty acceleration functions; can make meaningful with polar cords at each joint.
        penx = pg.mkPen(color=(0, 0, 255), width=5, style=QtCore.Qt.DashLine)
        peny = pg.mkPen(color=(255, 255, 0), width=5, style=QtCore.Qt.DashLine)
        penz = pg.mkPen(color=(0, 255, 0), width=5, style=QtCore.Qt.DashLine)

        self.view2D_Q1.plot(
            self.Acceleration_3D[:,0],
            self.Acceleration_3D[:,1],
            name="Ax",
            pen=penx,
            symbol="t1",
            symbolSize=10,
            symbolBrush="b",
        )
        self.view2D_Q2.plot(
            self.Acceleration_3D[:,0],
            self.Acceleration_3D[:,2],
            name="Ay",
            pen=peny,
            symbol="t1",
            symbolSize=10,
            symbolBrush="y",
        )
        self.view2D_Q3.plot(
            self.Acceleration_3D[:,0],
            self.Acceleration_3D[:,3],
            name="Az",
            pen=penz,
            symbol="t1",
            symbolSize=10,
            symbolBrush="g",
        )

#inputs are based on DH parameters; standard robotics workflow

inputs = np.array([
    #theta(i) , d(i) , a(i) , alpha(i)
    [45,  0 , 2  , 0],
    [0 ,  0 , 3 , 0],
    [15 , 0 , 1 , 0],
    [45,  0 , 2  , 0],
    [25 ,  0 , 3 , 0],
    [15 , 0 , 1 , 0]
])
inputs3D = np.array([
    #theta(i) , d(i) , a(i) , alpha(i)
    [45,  0 , 2  , 45],
    [0 ,  0 , 3 , -90],
    [0 , 0 , 1 , 0],
    [45,  0 , 2  , 45],
    [0 ,  0 , 3 , -90],
    [90 , 0 , 1 , 0]
])

Acceleration_3D = np.array([
    [0, 5, 10, 5],
    [1, 0, 17, 9],
    [2, 1, 15, 4],
    [3, 10, 1, 1],
    [4, 5, 10, 5],
    [5, 1, 6, 3 ]
])
main = ForwardKinematics.kin(inputs3D)
result = main.coordinates()

#def main():

app = QtWidgets.QApplication([])
main = Main_Window(result, Acceleration_3D)
main.show()
app.exec()
 
#if __name__ == '__main__':         
#    main()
