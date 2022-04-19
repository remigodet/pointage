### Pointage MAIN

# Remi Godet - Hoche 2020/2021 - TIPE AMA/TLCD
# @author : remgodet@laposte.net
# version : 2.0

##python imports
import os
import imageio
import matplotlib.pyplot as plt
import numpy as np
import xlwt
import time
import random as rd
import cv2


## local imports

## fonctions

def menu():
    choice = input('crop or run \n')
    if choice=='crop':
        choice_crop()
        choice_run()
        return
    elif choice == 'run':
        choice_run()
        return
    else:
        print('none choosen')
        pass

def create_filter(TAILLE,e):
    matrix = np.zeros((TAILLE,TAILLE))
    matrix.fill(100)
    matrix[TAILLE//2-e:TAILLE//2+e,:] = -300
    matrix[:,TAILLE//2-e:TAILLE//2+e] = -100
    return matrix


def stamp(i,j,M,F,TAILLE):
    matrix = M[i:i+TAILLE,j:j+TAILLE]
    matrix = matrix*F
    return np.sum(matrix)




def find_pos(image_grey,STEP,TAILLE,LINE,old_i=False,old_j=False,return_type='pos'):

    filter = create_filter(TAILLE,LINE)
    max_value = stamp(0,0,image_grey,filter,TAILLE)
    maxi=0
    maxj=0


    if old_i:
        old_i -= TAILLE//2
        old_j -= TAILLE//2
        # avec la memoire et STEP ++ rapide
        for j in range(max(old_j-STEP,0),min(old_j+STEP,len(image_grey[0])-TAILLE)+1):
            for i in range(max(old_i-STEP,0),min(old_i+STEP,len(image_grey)-TAILLE)+1):

                t = stamp(i,j,image_grey,filter,TAILLE)
                if t >= max_value:
                    max_value = t
                    maxi = i-min(old_i-STEP,0)
                    maxj = j-min(old_j-STEP,0)
    else:
        # sans memoire
        for i in range(len(image_grey)-TAILLE):
            for j in range(len(image_grey[0])-TAILLE):
                t = stamp(i,j,image_grey,filter,TAILLE)
                if t >= max_value:
                    max_value = t
                    maxi=i
                    maxj=j

    #return types
    #debug
    if return_type == 'debug':
        M = image_grey.copy()
        if old_i:
            for j in range(max(old_j-STEP,0),min(old_j+STEP,len(image_grey[0])-TAILLE)+1):
                for i in range(max(old_i-STEP,0),min(old_i+STEP,len(image_grey)-TAILLE)+1):
                    M[i][j]=0
        M[maxi+TAILLE//2-25:maxi+TAILLE//2+25,maxj+TAILLE//2-25:maxj+TAILLE//2+25]=255
        print('debug')
        print(max(old_j-STEP,0),min(old_j+STEP,len(image_grey[0])-TAILLE)+1)
        print(max(old_i-STEP,0),min(old_i+STEP,len(image_grey)-TAILLE)+1)
        print(maxi,maxj)
        return M,maxi+TAILLE//2,maxj+TAILLE//2
    #crop
    elif return_type != 'pos':
        M = image_grey.copy()

        M[maxi+TAILLE//2-5:maxi+TAILLE//2+5,maxj+TAILLE//2-5:maxj+TAILLE//2+5]=0
        return M,maxi+TAILLE//2,maxj+TAILLE//2
    #run
    else:
        return maxi+TAILLE//2,maxj+TAILLE//2




def choice_crop():
    print('Opening crop parameters')
    token = True
    while token:
        print("x--> Vertical")
        print("y--> Horizontal")
        print(PARAM)
        #
        #
        for filename in os.listdir():
            print(filename)
            vid = imageio.get_reader(filename,  'ffmpeg')
            break
        #
        #dims
        image = vid.get_data(0)
        print(f'Image caractéristiques : {len(image)} * {len(image[0])}.')
        #
        # input user
        x1=int(input('x1\n'))
        x2=int(input('x2\n'))
        y1=int(input('y1\n'))
        y2=int(input('y2\n'))
        TAILLE =  int(input('TAILLE\n'))
        LINE = int(input('LINE\n'))
        STEP =  int(input('STEP\n'))


        PARAM['x1'] = x1
        PARAM['x2'] = x2
        PARAM['y1'] = y1
        PARAM['y2'] = y2
        PARAM['TAILLE'] = TAILLE
        PARAM['LINE'] = LINE
        PARAM['STEP'] = STEP

        #
        fig,axs = plt.subplots(nb,2)
        fig.suptitle('comparing crops')
        alea = rd.randint(0,vid.count_frames()-1-nb)
        for num in range(nb):
            image = vid.get_data(num+alea)
            image = image[x1:x2, y1:y2]
            image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            if num==0:
                image2,i,j = find_pos(image,STEP,TAILLE,LINE,return_type='crop')
            else:
                image2,i,j = find_pos(image,STEP,TAILLE,LINE,return_type='crop',old_i=i,old_j=j)
            axs[num,0].imshow(image)
            axs[num,1].imshow(image2)
        plt.show()
        plt.waitforbuttonpress()
        plt.close()

        if input('Save target ?- yes\n')=='yes':
            NAME = input('Target name ?\n')
            str_to_show = input('list to show - X or Y\n')
            target = Target(NAME,x1,x2,y1,y2,TAILLE,STEP,LINE,str_to_show)
            TARGETS.append(target)



        token = input('Crop again ? - yes\n')

        if token =='' or token == 'yes':
            token = True

        else:
            token = False


class Target():
    # str to show is 'X' or 'Y'
    def __init__(self,NAME,x1,x2,y1,y2,TAILLE,STEP,LINE,str_to_show):
        self.NAME = NAME
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.TAILLE = TAILLE
        self.STEP = STEP
        self.LINE = LINE
        self.str_to_show = str_to_show
        self.num = True
        self.X = []
        self.Y = []
        self.i = 0
        self.j = 0

    def __str__(self):
        return 'my name is '+NAME

    def process_img(self,image):
            image = image[self.x1:self.x2, self.y1:self.y2]
            image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

            if self.num==True:
                self.i,self.j = find_pos(image,self.STEP,self.TAILLE,self.LINE,return_type='pos')
                self.num = False
            else:
                self.i,self.j = find_pos(image,self.STEP,self.TAILLE, self.LINE,return_type='pos',old_i=self.i,old_j=self.j)
            self.X.append(self.i)
            self.Y.append(self.j)
            return self.i, self.j

    def get_XY(self):
        return self.X, self.Y

    def reset(self):
        self.num = True
        self.X = []
        self.Y = []



def choice_run():
    book = xlwt.Workbook()
    print('Running...')
    filenames = os.listdir()
    print('videos count : {}'.format(len(filenames)))
    print('target count: {}'.format(len(TARGETS)))

    for filename in filenames:
        vid = imageio.get_reader(filename,  'ffmpeg')
        data = []
        #time init
        t0 = time.time()

        for i in range(vid.count_frames()-1):

            if i%100 == 0:
                print('processing video '+filename+', frame numero {}'.format(i+1)+' out of {}'.format(vid.count_frames()))

            image = vid.get_data(i)

            for target in TARGETS:
                target.process_img(image)
        #time end
        temps = time.time() - t0
        pixels = len(image) * len(image[0]) * vid.count_frames()
        print('temps mis: {}s '.format(temps))
        print('temps par pixel = {} s'.format(temps/pixels,format_spec='e'))

        #end of vid
        for target in TARGETS:
            data.append([target.NAME, target.X, target.Y, target.str_to_show])
            #show
            if data[-1][3]=='X':
                plt.plot(data[-1][1])
                plt.suptitle(data[-1][0])
                plt.show()
                plt.waitforbuttonpress()
                plt.close()
                plt.clf()
            else:
                plt.plot(data[-1][2])
                plt.suptitle(data[-1][0])
                plt.show()
                plt.waitforbuttonpress()
                plt.close()
                plt.clf()
            target.reset()
        sheet = book.add_sheet(filename)
        for idx,serie in enumerate(data):

            sheet.write(1,idx*2+1,data[idx][0])
            sheet.write(2,idx*2+1,data[idx][3])

            for index,x in enumerate(data[idx][1]):
                sheet.write(index+3,idx*2+1,x)

            for index,y in enumerate(data[idx][2]):
                sheet.write(index+3,idx*2+1+1,y)

    book.save('excel.xls')







    # batch-> video-> image -> targets -> excel


# main

def init(your_path='C:\\Users\\Utilisateur\\Desktop\\Pointage_auto\\BATCH'):
    os.chdir(your_path)
    menu()



## params

#crop
nb = 3
# algo
PARAM = {'x1' : 500,
    'x2' : 600,
    'y1': 700,
    'y2': 1000,
    'TAILLE': 26,
    'STEP': 50,
    'LINE':4
    }
TARGETS=[]

##run
plt.clf()
init(your_path="'C:\\Users\\Utilisateur\\your\\path\\BATCH")








