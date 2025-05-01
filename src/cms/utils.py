# src/cms/utils.py

from magiccube.cube_base import Face


def cube_to_faces(cube):
    """
    Extracts and flattens the 6 cube faces (U, L, F, R, B, D) from a Cube object.
    Returns a list of 6 lists, each with 9 single-character color codes.
    """
    face_order = ["U", "L", "F", "R", "B", "D"]

    face_enum_map = {
        "U": Face.U,
        "L": Face.L,
        "F": Face.F,
        "R": Face.R,
        "B": Face.B,
        "D": Face.D,
    }

    faces = []

    for face_letter in face_order:
        face_enum = face_enum_map[face_letter]
        colors_flat = cube.get_face_flat(face_enum)
        faces.append(
            [color.name[0] for color in colors_flat]
        )  # Take first letter: W, O, G, R, B, Y

    return faces


def build_edge_map(cube, args):
    faces_list = cube_to_faces(cube)

    faces = {
        "U": faces_list[0],
        "L": faces_list[1],
        "F": faces_list[2],
        "R": faces_list[3],
        "B": faces_list[4],
        "D": faces_list[5],
    }

    EDGE_SPECS = {
        "UF": ("U", 7, "F", 1),
        "UR": ("U", 5, "R", 1),
        "UB": ("U", 1, "B", 1),
        "UL": ("U", 3, "L", 1),
        "DF": ("D", 1, "F", 7),
        "DR": ("D", 5, "R", 7),
        "DB": ("D", 7, "B", 7),
        "DL": ("D", 3, "L", 7),
        "FR": ("F", 5, "R", 3),
        "FL": ("F", 3, "L", 5),
        "BR": ("B", 3, "R", 5),
        "BL": ("B", 5, "L", 3),
    }

    edge_map = {}

    for edge, (face1, idx1, face2, idx2) in EDGE_SPECS.items():
        color1 = faces[face1][idx1]
        color2 = faces[face2][idx2]
        edge_map[edge] = (color1, color2)

    return edge_map


def display_edge_map(edge_map):
    """
    Print the 12 edges in three rows of four,
    e.g.
      UF W-G   UR W-R   UB W-B   UL W-O
      FR G-R   FL G-O   BR B-R   BL B-O
      DF Y-G   DR Y-R   DB Y-B   DL Y-O
    """
    order = ["UF", "UR", "UB", "UL", "FR", "FL", "BR", "BL", "DF", "DR", "DB", "DL"]
    # group 4 per row
    for i in range(0, 12, 4):
        row = order[i : i + 4]
        print("  " + "   ".join(f"{e} {edge_map[e][0]}-{edge_map[e][1]}" for e in row))


def build_corner_map(cube, args):
    """
    Like build_edge_map, but for 8 corners,
    returns { "UFR": ("W","G","R"), … }
    """
    faces = cube_to_faces(cube)
    F = dict(zip(["U", "L", "F", "R", "B", "D"], faces))

    # spec: (face1,idx1,face2,idx2,face3,idx3)
    specs = {
        "UFR": ("U", 8, "F", 2, "R", 0),
        "UFL": ("U", 6, "L", 2, "F", 0),
        "UBL": ("U", 0, "B", 2, "L", 0),
        "UBR": ("U", 2, "R", 2, "B", 0),
        "DFR": ("D", 2, "F", 8, "R", 6),
        "DFL": ("D", 0, "L", 8, "F", 6),
        "DBL": ("D", 6, "B", 8, "L", 6),
        "DBR": ("D", 8, "R", 8, "B", 6),
    }

    return {
        name: (F[f1][i1], F[f2][i2], F[f3][i3])
        for name, (f1, i1, f2, i2, f3, i3) in specs.items()
    }


def display_corner_map(corner_map):
    """
    Print the 8 corners in two rows of four,
    e.g.
      UFR W-G-R   UFL W-O-G   UBL W-O-B   UBR W-B-R
      DFR Y-G-R   DFL Y-O-G   DBL Y-B-O   DBR Y-R-B
    """
    order = ["UFR", "UFL", "UBL", "UBR", "DFR", "DFL", "DBL", "DBR"]
    for i in range(0, 8, 4):
        row = order[i : i + 4]
        print("  " + "   ".join(f"{c} {'-'.join(corner_map[c])}" for c in row))
