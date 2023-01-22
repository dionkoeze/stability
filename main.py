import random as rnd
import matplotlib.pyplot as plt

class loop:
    def __init__(self, stencil):
        self.stencil = stencil
    
    def response(self, history):
        return sum(h*s for h,s in zip(history[::-1], self.stencil[::-1]))

    def copy(self):
        return loop(self.stencil[:])

    # def run(self, signal):
    #     history = []
    #     for val in signal:
    #         history.append(val + self.response(history))
    #     return history

    def mutate(loop):
        p = rnd.uniform(0,1)
        if p < .1:
            return loop.mutate_grow()
        elif p < .2:
            return loop.mutate_shrink()
        else:
            return loop.mutate_stencil()

    def mutate_stencil(self):
        # change all
        # delta = [rnd.uniform(-1,1) for _ in range(len(self.stencil))]

        # change one 
        delta = [0 for _ in self.stencil]
        delta[rnd.randint(0,len(delta)-1)] = rnd.uniform(-1,1)

        return loop([s+d for s,d in zip(self.stencil, delta)])

    def mutate_grow(self):
        return loop([0, *self.stencil, 0])

    def mutate_shrink(self):
        if len(self.stencil) > 2:
            return loop(self.stencil[1:-1])
        else:
            return loop(self.stencil[:])

class ensemble:
    def __init__(self, loops):
        self.loops = loops

    def run(self, signal):
        history = []
        for val in signal:
            history.append(val + sum(l.response(history) for l in self.loops))
        return history

    def offspring(self):
        genes = [l.copy() for l in self.loops]
        p = rnd.uniform(0,1)
        idx = rnd.randint(0, len(genes)-1)
        if p < .1:
            genes.append(genes[idx].mutate())
        elif p < .2:
            if len(genes) > 1:
                genes.pop(idx)
        else:
            genes[idx] = genes[idx].mutate()
        return ensemble(genes)

# def score(history):
#     return sum((history[i] - math.sin(i))**2 for i in range(len(history)))

def score(history):
    return 100 * (history[-1] - 5) ** 2 + sum(abs(a-b) for a,b in zip(history[:-1], history[1:]))

# eve = ensemble([loop([0,0,0,0,0,0,0])])
# population = [eve.offspring() for _ in range(100)]

pop_size = 1000
population = []
for _ in range(pop_size):
    loops = []
    for _ in range(rnd.randint(1,10)):
        loops.append(loop([rnd.uniform(-1,1) for _ in range(rnd.randint(1,40))]))
    population.append(ensemble(loops))

signal = range(100)
# signal = list(map(lambda x: 5*math.sin(2*x)+5*math.sin(x/2), signal))
signal = [1 for _ in signal]

for generation in range(10000):
    print(generation)
    if generation % 100 == 0:
        print(population[0].stencil)
        print(score(population[0].run(signal)))
        for i in population[:pop_size//2]:
            plt.plot(i.run(signal))
        plt.ylim(-10,10)
        plt.show()
    population.sort(key=lambda i: score(i.run(signal)))
    population = population[:pop_size//2]
    population.extend([i.mutate() for i in population])
    # population.extend([population[0].mutate().mutate().mutate() for _ in range(10)])


population.sort(key=lambda i: score(i.run(signal)))
for i in population[:10]:
    plt.plot(i.run(signal))
plt.ylim(-10,10)
plt.show()
