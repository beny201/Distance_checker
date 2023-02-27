from tkinter import *
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point
from shapely.ops import nearest_points
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


LENGTH = {
    "8.8": {
        "M12": (40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 180, 200),
        "M16": (50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 180, 200),
        "M20": (50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 180, 200),
        "M24": (60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 180, 200),
        "M27": (60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 180, 200),
        "M30": (70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 180, 200,),
        "M36": (90, 100, 110, 120, 130, 140, 150, 160, 180, 200),
    },


    "10.9": {
        "M12": (50, 60, 70, 80, 90),
        "M16": (50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 180),
        "M20": (60, 70, 80, 90, 100, 110, 120, 130, 140, 150),
        "M24": (60, 70, 80, 90, 100, 110, 120, 130, 140, 150),
        "M27": (60, 70, 80, 90, 100, 110, 120, 130, 140, 150),
        "M30": (70, 80, 90, 100, 110, 120, 130, 140, 150, 160),
        "M36": (90, 100, 110, 120, 140, 150, 160),
    }
}

# thickness washer
T_HEAD_BOLT = {
    "M12": 8,
    "M16": 10,
    "M20": 13,
    "M24": 15,
    "M27": 17,
    "M30": 19,
    "M36": 23,
}

# thickness washer
T_WIDTH_BOLT = {
    "8.8": {
        "M12": 20,
        "M16": 24,
        "M20": 30,
        "M24": 36,
        "M27": 44,
        "M30": 46,
        "M36": 50,
    },
    "10.9": {
        "M12": 22,
        "M16": 27,
        "M20": 32,
        "M24": 41,
        "M27": 46,
        "M30": 50,
        "M36": 60,
    }}
# thickness washer
T_WASHER = {
    "M12": 2.8,
    "M16": 3.6,
    "M20": 3.6,
    "M24": 4.6,
    "M27": 5,
    "M30": 5,
    "M36": 6,
}

T_NUTS = {
    "M12": 11,
    "M16": 15,
    "M20": 18,
    "M24": 22,
    "M27": 24,
    "M30": 26,
    "M36": 31,
}

A_DISTANCE = {
    "M12": 4,
    "M16": 4,
    "M20": 4,
    "M24": 4,
    "M27": 6,
    "M30": 7,
    "M36": 7,
}

# First value are taken for bolts form list Length !!
Clamping = {
    "M12": 36,
    "M16": 32,
    "M20": 38,
    "M24": 34,
    "M27": 51,
    "M30": 39,
    "M36": 53,
}
root = Tk()
root.title("Distance checker")
WIDTH = "1000"
HEIGHT = "700"
root.geometry(f"{WIDTH}x{HEIGHT}")

# x and y values
start_points = (0, 0)
slope_girder = 10
height_girder = 1
t_top_flange = 0.01
height_column = 1
t_connection_plate = 0.03
class_bolt = "8.8"
t_flange_column = 0.02
diameter_bolt = "M12"


# Create function to execute

def getting_value():
    global slope_girder
    global height_girder
    global t_top_flange
    global height_column
    global t_connection_plate
    global diameter_bolt
    global class_bolt
    global t_flange_column
    try:
        slope_girder = float(f_slope_girder.get())
        height_girder = int(f_girder_height.get())*0.001
        t_top_flange = int(f_t_flange_ridge.get())*0.001
        t_flange_column = int(f_t_flange_column.get())*0.001
        height_column = int(f_column_width.get())*0.001
        t_connection_plate = int(f_t_connection_plate.get())*0.001
        diameter_bolt = used_bolt.get()
        class_bolt = ussed_class.get()
    except ValueError:
        print("error")


def length_bolt(class_bolt, bolt, t_plate):
    new_list = []
    basic_length = 2*T_WASHER[bolt] + T_NUTS[bolt] + \
        (2*t_plate*1000) + A_DISTANCE[bolt]
    for x in LENGTH[class_bolt][bolt]:
        if x > basic_length:
            new_list.append(x)
    return new_list[0]


def searching_length(class_bolt, bolt, t_plate):

    searched_length_of_bolt = (length_bolt(
        class_bolt, bolt, t_plate))*0.001 + (T_HEAD_BOLT[bolt])*0.001
    return searched_length_of_bolt


def finding_bolt_for_clamp(class_bolt, bolt, thickness_plate):
    # Searching for possible length
    keys = [x for x in LENGTH[class_bolt][bolt]]
    # Making proper clamp length
    searching_bolt = int(Clamping[bolt])
    clamps = list(range(searching_bolt, (searching_bolt+10*len(keys)), 10))
    result = list(zip(keys, clamps))
    result_which_mach = [(lenght, clamp) for lenght,
                         clamp in result if clamp > 2 * thickness_plate*1000]
    return result_which_mach[0][0]


def finding_clamp(class_bolt, bolt, thickness_plate):
    searched_length_of_bolt = finding_bolt_for_clamp(
        class_bolt, bolt, thickness_plate)*0.001 + (T_HEAD_BOLT[bolt])*0.001
    return searched_length_of_bolt


def min_distance(class_bolt, distance, bolt):
    offset = 0.5*T_WIDTH_BOLT[class_bolt][bolt] + (distance*1000)
    return int(offset)


def space_for_bolt_bottom(bolt_length, bolt, t_plate):
    needed_length = (bolt_length-2*t_plate*1000-T_WASHER[bolt])*0.001
    return needed_length


def myRidge():
    getting_value()
    if class_bolt == "10.9":
        bolt_length = finding_bolt_for_clamp(
            class_bolt, diameter_bolt, t_connection_plate)
        distance = finding_clamp(class_bolt, diameter_bolt, t_connection_plate)
    else:
        bolt_length = length_bolt(
            class_bolt, diameter_bolt, t_connection_plate)
        distance = searching_length(
            class_bolt, diameter_bolt, t_connection_plate)

    additional_check = space_for_bolt_bottom(
        bolt_length, diameter_bolt, t_connection_plate)

    print(additional_check)
    print(bolt_length)
    # drawings first line top flange column
    A = Point(start_points[0], start_points[1])
    B = Point(start_points[0], start_points[0]-3)
    line_ab = LineString([A, B])
    flange_ab = line_ab.parallel_offset(t_flange_column, "left")
    # drawings second line bottom flange column

    line_cd = line_ab.parallel_offset(height_column, "left")

    C = Point(line_cd.coords[0])
    D = Point(line_cd.coords[1])

    # drawings third line top flange
    E = Point(3, (math.tan(math.radians(slope_girder)))*2)
    line_ae = LineString([A, E])
    flange_ae = line_ae.parallel_offset(t_top_flange, "right")

    # drawings forth line bottom flange
    line_fg = line_ae.parallel_offset(height_girder, "right")

    F = Point(line_fg.coords[0])
    G = Point(line_fg.coords[1])

    # drawings line for connection
    H = line_cd.intersection(line_fg)
    line_ah = LineString([A, H])

    # bottom_flange_view_ridge
    line_gh = LineString([G, H])

    # bottom_flange_view_column
    line_dh = LineString([D, H])

    # offset to find distance for bolts height
    line_ij = line_ah.parallel_offset(distance + t_connection_plate, "left")

    # offset to find distance for bolts height, assembly from bottom
    line_ij1 = line_ah.parallel_offset(distance + t_connection_plate, "right")

    # offset to find distance for bolts height, assembly from bottom, check top space

    line_ij2 = line_ah.parallel_offset(
        additional_check + t_connection_plate, "left")

    # offset to find distance for bolts height, assembly from top, check bottom space

    line_ij3 = line_ah.parallel_offset(
        additional_check + t_connection_plate, "right")

    # intersection height of bolt and flange

    K = line_ij.intersection(flange_ae)

    L = nearest_points(line_ah, K)

    line_kl = LineString([K, L[0]])

    looking_value_top = A.distance(L)

    # intersection of columns flange and length of bolts
    M = line_ij1.intersection(flange_ab)
    N = nearest_points(line_ah, M)
    line_mn = LineString([M, N[0]])

    looking_value_bottom = A.distance(N)

    # intersection of girder flange and space needed for rest of bolt from bottom mounting

    O = line_ij2.intersection(flange_ae)
    P = nearest_points(line_ah, O)
    line_op = LineString([O, P[0]])

    # intersection of column flange and space needed for rest of bolt from top mounting

    R = line_ij3.intersection(flange_ab)
    S = nearest_points(line_ah, R)

    line_rs = LineString([R, S[0]])
    looking_value_top_space = A.distance(S)
    #print(f" Assembly top {looking_value_top_space[0]}")

    # drawing line of bolt when mounting from bottom
    T = nearest_points(line_ij1, O)

    line_pt = LineString([O, T[0]])

    looking_value_bottom_space = A.distance(P)
    #print(f" Assembly bottom {looking_value_bottom_space[0]}")

    # drawing line of bolt when mounting from top
    U = nearest_points(line_ij2, R)

    line_ur = LineString([R, U[0]])

    looking_value_bottom_space = A.distance(P)
    #print(f" Assembly bottom {looking_value_bottom_space[0]}")

    fig = Figure(figsize=(3, 3), dpi=140)

    # adding the subplot
    plot1 = fig.add_subplot(111)

    if looking_value_bottom_space[0] >= looking_value_bottom[0]:
        value_bottom = looking_value_bottom_space[0]
        plot1.plot(*line_pt.xy)
    else:
        value_bottom = looking_value_bottom[0]
        plot1.plot(*line_mn.xy)

    if looking_value_top_space[0] >= looking_value_top[0]:
        value_top = looking_value_top_space[0]
        plot1.plot(*line_ur.xy)
    else:
        value_top = looking_value_top[0]
        plot1.plot(*line_kl.xy)

    # plotting the graph
    plot1.plot(
        *line_ab.xy,
        # *line_cd.xy
        *line_ae.xy,
        *line_ae.xy,
        # *line_fg.xy
        # *flange_ae.xy
        *line_ah.xy,
        # *line_kl.xy,
        # *line_ij.xy,
        *line_gh.xy,
        *line_dh.xy,
        # *line_ij1.xy,
        # *flange_ab.xy,
        # *line_mn.xy,
        # *line_ij2.xy,
        # *line_op.xy,
        # *line_pt.xy,
        # *line_rs.xy,
        # *line_ij3.xy,
    )
    # Make axis equal
    plot1.axis('equal')

    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=root)

    canvas.draw()
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().grid(row=11, column=0, columnspan=2)

    # printing output
    result = min_distance(class_bolt, value_top, diameter_bolt)
    result_label = Label(root, text=result)
    result_label.grid(row=9, column=1, sticky="W")
    result_label1 = Label(root, text="Distance when mounting from top",
                          font='Helvetica 10 bold')
    result_label1.grid(row=9, column=0, sticky="E")

    result = min_distance(class_bolt, value_bottom, diameter_bolt)
    result_label = Label(root, text=result)
    result_label.grid(row=10, column=1, sticky="W")
    result_label1 = Label(root, text="Distance when mounting from bottom",
                          font='Helvetica 10 bold')
    result_label1.grid(row=10, column=0, sticky="E")


# Create text boxes
f_slope_girder = Entry(root, width=20)
f_slope_girder.grid(row=0, column=1, padx=20),
f_slope_girder.insert(0, "10.5")

f_girder_height = Entry(root, width=20)
f_girder_height.grid(row=1, columnspan=1, column=1, padx=20)
f_girder_height.insert(0, "900")

f_t_flange_ridge = Entry(root, width=20)
f_t_flange_ridge.grid(row=2, column=1, padx=20)
f_t_flange_ridge.insert(0, "20")

f_column_width = Entry(root, width=20)
f_column_width.grid(row=3, column=1, padx=20)
f_column_width.insert(0, "900")

f_t_flange_column = Entry(root, width=20)
f_t_flange_column.grid(row=4, column=1, padx=20)
f_t_flange_column.insert(0, "20")

f_t_connection_plate = Entry(root, width=20)
f_t_connection_plate.grid(row=5, column=1, padx=20)
f_t_connection_plate.insert(0, "30")

#f_used_bolt = Entry(root, width=20)
#f_used_bolt.grid(row=6, column=1, padx=20)
#f_used_bolt.insert(0, "M16")

ussed_class = StringVar(root)
ussed_class.set("Select class")
possible_class = [x for x in LENGTH]
f_ussed_class = OptionMenu(root, ussed_class, *possible_class)
f_ussed_class.grid(row=6, column=1, sticky="N")

# Variable to keep track of the option
# selected in OptionMenu
used_bolt = StringVar(root)
possible_bolts = [x for x in LENGTH[class_bolt]]
# Set the default value of the variable
used_bolt.set("Select an bolt")
f_used_bolt = OptionMenu(root, used_bolt, *possible_bolts)
f_used_bolt.grid(row=6, column=2, sticky="N")

# Create text labels
slope_girder_units = Label(root, text="Degree []",)
slope_girder_units.grid(row=0, column=2, sticky="W")

slope_girder_label = Label(root, text="Insert angle of girder",)
slope_girder_label.grid(row=0, column=0, sticky="E")


girder_height_label = Label(root, text="Girder height",)
girder_height_label.grid(row=1, column=0, sticky="E")

profiles_units = Label(root, text="[mm]",)
profiles_units.grid(row=1, rowspan=5,  column=2, sticky="W")

t_flange_girder_label = Label(root, text="Thickness of flange in girder", )
t_flange_girder_label.grid(row=2, column=0, sticky="E")

column_width_label = Label(root, text="Column width",)
column_width_label.grid(row=3, column=0, sticky="E")

t_flange_column_label = Label(root, text="Thickness of flange in column",)
t_flange_column_label.grid(row=4, column=0, sticky="E")

t_connection_plate_label = Label(
    root, text="Thickness of plate in connection",)
t_connection_plate_label.grid(row=5, column=0, sticky="E")

used_bolt_label = Label(root, text="Used bolt in corner connection",)
used_bolt_label.grid(row=6, column=0, sticky="E")

# --------------------------------------------------------------

# Create text boxes
f_slope_girder_left = Entry(root, width=20)
f_slope_girder_left.grid(row=0, column=8, padx=20),
f_slope_girder_left.insert(0, "10.5")


f_slope_girder_right = Entry(root, width=20)
f_slope_girder_right.grid(row=1, column=8, padx=20),
f_slope_girder_right.insert(0, "10.5")

f_girder_height_ridge = Entry(root, width=20)
f_girder_height_ridge.grid(row=2, column=8, padx=20)
f_girder_height_ridge.insert(0, "900")

f_t_flange_girder_left = Entry(root, width=20)
f_t_flange_girder_left.grid(row=3, column=8, padx=20)
f_t_flange_girder_left.insert(0, "20")

f_t_flange_girder_right = Entry(root, width=20)
f_t_flange_girder_right.grid(row=4, column=8, padx=20)
f_t_flange_girder_right.insert(0, "20")


f_t_connection_plate_ridge = Entry(root, width=20)
f_t_connection_plate_ridge.grid(row=5, column=8, padx=20)
f_t_connection_plate_ridge.insert(0, "30")


# Create text labels
empty = Label(root, text="      ",)
empty.grid(row=0, column=6, sticky="N")

f_slope_girder_left = Label(root, text="Insert angle of left girder",)
f_slope_girder_left.grid(row=0, column=7, sticky="E")

f_slope_girder_right = Label(root, text="Insert angle of right girder",)
f_slope_girder_right.grid(row=1, column=7, sticky="E")


# Create button to execute

myButton = Button(root, text="Check minimum distance", command=myRidge)
myButton.grid(row=8, column=0, columnspan=2)

root.mainloop()
