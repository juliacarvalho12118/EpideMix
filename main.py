import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap

# -----------------------------
# Parâmetros configuráveis
# -----------------------------
GRID_SIZE = 200
INITIAL_INFECTED = 5
INFECTION_RATE = 0.1
RECOVERY_RATE = 0.05
MORTALITY_RATE = 0.02
STEPS = 50

# Estados possíveis
SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2
DEAD = 3

# -----------------------------
# Inicialização da população
# -----------------------------
def initialize_population():
    population = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    for _ in range(INITIAL_INFECTED):
        x, y = np.random.randint(0, GRID_SIZE, size=2)
        population[x, y] = INFECTED
    return population

# -----------------------------
# Atualização da simulação
# -----------------------------
def update_population(population):
    new_population = population.copy()
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if population[x, y] == INFECTED:
                r = np.random.rand()
                if r < MORTALITY_RATE:
                    new_population[x, y] = DEAD
                elif r < MORTALITY_RATE + RECOVERY_RATE:
                    new_population[x, y] = RECOVERED
                else:
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                                if population[nx, ny] == SUSCEPTIBLE and np.random.rand() < INFECTION_RATE:
                                    new_population[nx, ny] = INFECTED
    return new_population

# -----------------------------
# Visualização em tempo real
# -----------------------------
def animate(i, img, population, counts, lines):
    new_population = update_population(population[0])
    population[0] = new_population
    img.set_data(population[0])

    # Contagem de estados
    unique, counts_states = np.unique(population[0], return_counts=True)
    state_counts = dict(zip(unique, counts_states))
    S = state_counts.get(SUSCEPTIBLE, 0)
    I = state_counts.get(INFECTED, 0)
    R = state_counts.get(RECOVERED, 0)
    D = state_counts.get(DEAD, 0)

    counts["S"].append(S)
    counts["I"].append(I)
    counts["R"].append(R)
    counts["D"].append(D)

    # Atualiza linhas do gráfico
    lines[0].set_data(range(len(counts["S"])), counts["S"])
    lines[1].set_data(range(len(counts["I"])), counts["I"])
    lines[2].set_data(range(len(counts["R"])), counts["R"])
    lines[3].set_data(range(len(counts["D"])), counts["D"])

    return img, *lines

def run_simulation():
    population = [initialize_population()]
    counts = {"S": [], "I": [], "R": [], "D": []}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Mapa de calor
    cmap = ListedColormap(["blue", "red", "green", "black"])
    img = ax1.imshow(population[0], cmap=cmap, interpolation="nearest", vmin=0, vmax=3)
    ax1.set_title("Mapa da epidemia")
    cbar = plt.colorbar(img, ax=ax1, ticks=[0, 1, 2, 3])
    cbar.ax.set_yticklabels(["Suscetível", "Infectado", "Recuperado", "Morto"])

    # Gráfico de evolução
    ax2.set_title("Evolução da epidemia")
    ax2.set_xlim(0, STEPS)
    ax2.set_ylim(0, GRID_SIZE * GRID_SIZE)
    lineS, = ax2.plot([], [], color="blue", label="Suscetível")
    lineI, = ax2.plot([], [], color="red", label="Infectado")
    lineR, = ax2.plot([], [], color="green", label="Recuperado")
    lineD, = ax2.plot([], [], color="black", label="Morto")
    ax2.legend()

    ani = animation.FuncAnimation(
        fig, animate, fargs=(img, population, counts, [lineS, lineI, lineR, lineD]),
        frames=STEPS, interval=200, blit=True
    )
    plt.show()

# -----------------------------
# Executa a simulação
# -----------------------------
if __name__ == "__main__":
    run_simulation()