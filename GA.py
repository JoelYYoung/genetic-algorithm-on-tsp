import random
import math
import matplotlib.pyplot as plt

MAPWIDTH = 100 # 地图的宽度
MAPLEN = 200 # 地图的长度

class Path:
    '''represent hamiltonian cycle.

    attributes:
    num(int):num of existing edges
    path(list):sequence of city ID listed in city_map
    city_map(CityMap):related map of cities
    '''
    def __init__(self, city_map, path_list=[]):
        self.num = city_map.num
        self.city_map = city_map
        if len(path_list) == 0:
            self.path = list(range(self.num))
            random.shuffle(self.path)
        else:
            self.path = path_list.copy()

    def get_distance(self):
        '''return total distance of the cycle.'''
        distance = 0
        for i in range(self.num):
            distance += self.city_map.map[self.path[i]][self.path[(i+1)%self.num]]
        return distance

    def crossover_path(self, partner):
        '''crossover with partner and return nothing.

        args:
        partner(Path):path to crossover with
        '''
        min = random.randint(0, self.num-1)
        max = random.randint(min, self.num-1)
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

class CityMap:
    '''representation of graph of cities.'''
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
    '''representation of Group in revolution.'''

    def __init__(self, city_map, init_size):
        '''constructor of Group class.
        
        args:
        city_map(CityMap):city_map that the group is based on
        init_size(int):initial size of group
        '''
        self.city_map = city_map # 委托模式，仅仅是一个引用而不是新的对象
        self.init_size = init_size
        self.path = [Path(city_map) for i in range(init_size)]

    def score(self, save_rate=1.0):
        '''evaluate every path in the group and return a list of score.

        args:
        save_rate(float):highest surviving possibility
        '''
        result = []
        for i in range(self.init_size):
            result.append(float(1)/self.path[i].get_distance())
        max_possibility = max(result)
        result = [i / max_possibility * save_rate for i in result]
        return result

    def revolve(self, variation_rate):
        '''implement revolution.
        
        args:
        variation_rate(float):ratio of variate genes
        '''
        variation_rate = int(variation_rate * self.city_map.num)
        score = self.score()
        max_index = score.index(max(score))
        result = []
        for i in range(self.init_size):
            if random.random() > score[i]: # 把这一项变异掉
                list = self.path[max_index].path.copy()
                for i in range(variation_rate):
                    a = random.randrange(0, self.city_map.num)
                    b = random.randrange(0, self.city_map.num)
                    list[a], list[b] = list[b], list[a]
                self.path[i] = Path(self.city_map, list)
                result.append(0)
            else:
                result.append(1)
        good_index = [i[0] for i in enumerate(result) if i[1] == 1]
        random.shuffle(good_index)
        for i in range(int(len(good_index)/2)):
            self.path[good_index[2*i]].crossover_path(self.path[good_index[2*i+1]])

    def show(self, choice=0):
        '''display path as a matplotlib pic.
        
        args:
        choice(int):choose the path to display

        note:
        if choice missing then display the shortest path in the group.
        parameter choice should be within the range of 0~num or will arise Exception.
        '''
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
    '''caculate and return distance between two cities.'''
    return math.sqrt(math.pow(city1[0]-city2[0], 2)+math.pow(city1[1]-city2[1], 2))

if __name__== '__main__':
    init_size = 1000
    epoch = 20

    city_map = CityMap(100)
    group = Group(city_map, init_size)
    result = []
    group.show()
    for i in range(epoch):
        group.revolve(10)
        score = group.score(0.8)
        min_length = group.path[score.index(max(score))].get_distance()
        print("min length:", min_length)
        result.append(min_length)
    group.show()
    plt.plot(result)
    plt.show()
