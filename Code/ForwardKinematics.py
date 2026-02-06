import numpy as np

class kin():
    def __init__(self, inputs):

        self.inputs = inputs

        self.num_links = inputs.shape[0]
        print("links:" , self.num_links, "\n")

        self.frames = []
        self.combined_frames = []
        self.each_frame = [0]
        self.cords = []

    def coordinates(self):
        trans = kin.Transformation(self)
        self.cords.append(np.zeros(3))
        for i in range(self.num_links):
            self.cords.append(trans[i][0:3, 3])
            print(self.cords)
        return self.cords
    def Transformation(self):
        #creates list of nested arrays for each frame
        u = 0
        p = 1
        #dont question greatness
        for i in range(self.num_links):
            #Append all Rotations; Matrix multiply immediately rather than creating unnessesary additional frame



            print("\n\n\n\n\n" , i, "\n\n\n")
            self.frames.append(self.shell_matrix())

            yaw = kin.yaw(self.inputs[i,0])
            pitch = kin.pitch(self.inputs[i,3])

            self.frames[u][0:3 , 0:3] =  np.matmul(yaw, pitch)

            #Append all translations
            self.frames.append(self.shell_matrix())
            self.frames[p][0,3] = self.inputs[i][2]
            self.frames[p][1,3] = self.inputs[i][2]

            self.combined_frames.append(np.matmul(self.frames[u], self.frames[p]))
            u+=2
            p+=2

        self.each_frame[0] = self.combined_frames[0]

        for i in range(1, self.num_links):
            self.each_frame.append(np.matmul(self.each_frame[i-1], self.combined_frames[i]))
        return self.each_frame

    #theta = yaw ;  d = z translation
    #alpha = pitch; a = x translation
    def shell_matrix(self):
        shell = np.eye(4)
        return shell
    
    #euler angles as inputs for all rotation matricies
    def yaw(alpha):
        alpha = np.deg2rad(alpha)
        return np.array([
            [np.cos(alpha) , -np.sin(alpha) , 0],
            [np.sin(alpha) , np.cos(alpha) , 0] , 
            [0 , 0 , 1]
        ])
    def pitch(beta):
        beta = np.deg2rad(beta)
        return np.array([
            [np.cos(beta) , 0 , np.sin(beta)],
            [0 , 1 , 0] , 
            [-np.sin(beta) , 0 , np.cos(beta)]
        ])
    def roll(gamma):
        gamma = np.deg2rad(gamma)
        return np.array([
            [1 , 0 , 0],
            [0 , np.cos(gamma) , -np.sin(gamma)] , 
            [0 , np.sin(gamma) , np.cos(gamma)]
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


main  = kin(inputs3D)

result  = main.coordinates()

print(result)