# PROYECTO BUSCAMINAS - GRUPO COD3

# Integrantes:

* David Santiago Hoyos Mateus

* Diego Garcés Torres

# Logo: 

[![Captura-de-pantalla-2024-09-01-114242.png](https://i.postimg.cc/ZYcmqRNh/Captura-de-pantalla-2024-09-01-114242.png)](https://postimg.cc/yWktQ7nf)

# Alternativa Seleccionada:
La alternativa elegida fue desarrollar un juego de Buscaminas, un juego clasico que consiste en destapar todas las casillas vacías de un tablero sin revelar aquellas que contienen minas. Este proyecto fue seleccionado porque ofrece la oportunidad de implementar varios aspectos técnicos clave, como la generación aleatoria de minas, la revelación de celdas y el cálculo preciso de los números adyacentes. Además, implica la creación de una interfaz gráfica que no solo debe ser intuitiva y fácil de usar, sino también visualmente atractiva para el usuario.

Un aspecto particularmente interesante de este proyecto es su potencial para expansión. Se pueden añadir diferentes niveles de dificultad, temporizadores y tableros personalizados, lo que permite convertir este desarrollo en un proyecto mucho más completo y sofisticado. Estas características adicionales no solo aumentan la complejidad del juego, sino que también permiten explorar diversas técnicas de programación y diseño, enriqueciendo aún más la experiencia de desarrollo.


### Lógica (Como se va a desarrollar el programa)
*Hay ciertas cosas que hay que tener en cuenta en la logica interna del programa...

### Funciones preliminares

*En el programa hay 6 funciones primordiales las cuales son:

### Programa preliminar

```python
#Aqui va el programa preliminar
```

### Explicacion del programa

*Basicamente...

### Algoritmo preliminar

```mermaid
flowchart TD
%% Nodos
    A("Inicio")
    B("Se imprimen las reglas y el tablero en la pantalla")
    C("Se le pide al usuario una posicion")
    D{¿Desea poner una bandera o destapar la casilla?}
    E(Desea poner una bandera)
    F(Desea destapar la casilla)
    G(Se pone una bandera)
    H(Se destapa la casilla)
    I{¿La casilla es una mina?}
    J(Fin)
    K(Si)
    L(No)
    M{¿La casilla contiene un cero?}
    N(Si)
    O(No)
    P(Se destapan las casillas adyacentes que también son ceros y
cada casilla que se destape se suma en casillas destapadas
)
    Q(Se suma uno en casillas destapadas)
    R{¿Casillas destapadas = 90?}
    S(Si)
    T(No)
    U(Se le suma 1 a casillas minas)
    V{¿Casillas minas es igual a 10?}
    W(Si)
    Y(No)

%% Conexiones entre los nodos
    A-->B-->Z-->C-->D-->E-->G-->U-->V-->W-->J
    D-->F-->H-->I-->K-->J
    I-->L-->M-->N-->P
    M-->O-->Q
    P-->C
    Q-->R-->S-->J
    R-->T-->C
    V-->Y-->C
    Z(Casillas minas = 0
    Casillas destapadas = 0)

```
