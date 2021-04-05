import random
import math
import matplotlib.pyplot as plt

MAPWIDTH = 100 # 地图的宽度
MAPLEN = 200 # 地图的长度

class Path:
    '''represent hamiltonian cycle

    attributes:
    num(int):num of existing edges
    path(list):sequence of city ID listed in city_map
    '''
    def __init__(self, city_map, path_list=[]):
        self.num = city_map.num
        self.city_map = city_map
        if len(path_list) == 0:
            self.path = random.shuffle(list(range(self.num)))
        else:
            self.path = path_list.copy()

    def add_vertex(self, ID):
        '''添加新的城市到列表中，表示一条路径。

        args:
        ID参数表示添加城市的编号，位于(1~num)的范围中。
        如果ID重复或者num = 总数，就不继续添加'''
        if ID in self.path:
            return 0
        else:
            self.path.append(ID)
            self.num += 1

    def get_distance(self, city_map):
        '''统计当前的路径的总距离。

        city_map参数是当前的路径所在的地图上。'''
        distance = 0
        for i in range(self.num):
            distance += city_map.map[self.path[i]][self.path[(i+1)%self.num]]
        return distance

    def combine_path(self, partner):
        '''两条路径进行交叉。

        partner表示进行交叉的另一条路径。'''
        min = random.randint(0, self.num-1)
        max = random.randint(min, self.num-1)
        #print("min:", min, "max:", max)
        #print("before:")
        #print(self.path)
        #print(partner.path)
        self.path[min: max+1], partner.path[min: max+1] = \
        partner.path[min: max+1], self.path[min: max+1]
        # 交换去重
        check_area = list(range(self.num))[0: min] +\
                     list(range(self.num))[max+1: self.num]
        ptn_s = 0
        for i in check_area:
            if self.path[i] in self.path[min:max+1]:
                for j in check_area[ptn_s:]:
                    if partner.path[j] in partner.path[min:max+1]:
                        self.path[i], partner.path[j] =\
                        partner.path[j], self.path[i]
                        ptn_s += 1
                        break
                    ptn_s += 1
        #print("after:")
        #print(self.path)
        #print(partner.path)
class CityMap:
    def __init__(self, num):
        self.num = num
        # 产生一个初始的城市地图，采用邻接矩阵来存储
        self.city = []
        for i in range(self.num):
            self.city.append((random.randrange(MAPWIDTH), 
                              random.randrange(MAPLEN)))
        # 先假设每个城市之间都有路
        self.map = [[0]*self.num for i in range(self.num)]
        for i in range(self.num):
            for j in range(self.num):
                self.map[i][j] = distance(self.city[i], 
                                          self.city[j])

class Group:
    def __init__(self, city_map, init_size):
        '''种群类。
        
        传入参数city_map，根据这个地图，生成初始的种群。
        通过num参数可以设置处置种群的大小。'''
        self.city_map = city_map # 委托模式，仅仅是一个引用而不是新的对象
        self.path = [Path(city_map) for i in range(init_size)]

    def score(self, save_rate=1):
        '''为每个path打分。

        通过save_rate可以调节最高的留存概率。'''
        result = []
        for i in range(len(self.path)):
            result.append(float(1)/self.path[i].get_distance(self.city_map))
        max_possibility = max(result)
        result = [i / max_possibility * save_rate for i in result]
        return result

    def revolve(self, variation_rate):
        score = self.score()
        max_index = score.index(max(score))
        result = []
        for i in range(len(self.path)):
            if random.random() > score[i]: # 把这一项变异掉
                list = self.path[max_index].path.copy()
                for i in range(variation_rate):
                    a = random.randrange(0, self.city_map.num)
                    b = random.randrange(0, self.city_map.num)
                    list[a], list[b] = list[b], list[a]
                self.path[i] = Path(list)
                result.append(0)
            else:
                result.append(1)
        good_index = [i[0] for i in enumerate(result) if i[1] == 1]
        random.shuffle(good_index)
        for i in range(int(len(good_index)/2)):
            self.path[good_index[2*i]].combine_path(self.path[good_index[2*i+1]])
        #print("after revolution:")
        #for i in self.path:
            #print(i.path)
            

    def show_map(self, choice=0):
        '''显示出当前的某个图片。
        
        如果choice为0，那么展示最近的。
        否则展示choice指定的路径。'''
        if(choice == 0):
            score = self.score()
            choice = score.index(max(score))
        elif choice>0 and choice<len(self.path)+1:
            choice -= 1
        else:
            raise(Exception, "Wrong choice value.")

        plt.figure(figsize = (10, 10), dpi = 100)
        x = [i[0] for i in self.city_map.city]
        y = [i[1] for i in self.city_map.city]
        plt.scatter(x, y)
        for i in range(self.path[choice].num):
            plt.plot([self.city_map.city[self.path[choice].path[i]][0],\
                      self.city_map.city[self.path[choice].path[(i+1)%self.path[choice].num]][0]],\
                     [self.city_map.city[self.path[choice].path[i]][1],\
                      self.city_map.city[self.path[choice].path[(i+1)%self.path[choice].num]][1]])
        plt.show()

def distance(city1, city2):
    return math.sqrt(math.pow(city1[0]-city2[0], 2)+math.pow(city1[1]-city2[1], 2))

if __name__== '__main__':
    init_size = 1000
    epoch = 200
    city_map = CityMap(100)
    # print("city is", city_map.city)
    # print("map is", city_map.map)
    group = Group(city_map, init_size)
    result = []
    group.show_map()
    # for i in range(len(group.path)):
    #     print("path is", group.path[i].path)
    #     print("length is", group.path[i].get_di stance(city_map))
    for i in range(epoch):
        group.revolve(10)
        score = group.score(0.8)
        # for i in range(len(group.path)):
        #     print("length is", group.path[i].get_distance(city_map))
        min_length = group.path[score.index(max(score))].get_distance(city_map)
        print("min length:", min_length)
        result.append(min_length)
    group.show_map()
    plt.plot(result)
    plt.show()
