
def arm_measurement_dict(name = "Max"):
    unit = "cm"

    limb = {
       f"clv_shld_{name}": 15, 
       f"shld_elbow_{name}": 26, 
       f"elbow_wrist_{name}": 25.4, 
        }

    hand = {  
        f"wrist_indexKnu_{name}": 10.5, 
        f"wrist_middleKnu_{name}": 10, 
        f"wrist_ringKnu_{name}": 9.5,
        f"wrist_pinkyKnu_{name}": 9.8,
        f"wrist_thumbKnu_{name}": 9.5
        }

    handknuWidth = {  
        f"handknuWidth_{name}": 8.5
        }

    fingName = ["Knu", "Proximal", "Distal", "DistalEnd"]
    index = {  
        f"Index{fingName[0]}_Index{fingName[1]}_{name}": 3.5,
        f"Index{fingName[1]}_Index{fingName[2]}_{name}": 2.2,
        f"Index{fingName[2]}_Index{fingName[3]}_{name}": 2.7
        }

    middle = {  
        f"middle{fingName[0]}_middle{fingName[1]}_{name}": 3.8,
        f"middle{fingName[1]}_middle{fingName[2]}_{name}": 2.5,
        f"middle{fingName[2]}_middle{fingName[3]}_{name}": 2.9
        }

    ring = {  
        f"ring{fingName[0]}_ring{fingName[1]}_{name}": 3.7,
        f"ring{fingName[1]}_ring{fingName[2]}_{name}": 2.1,
        f"ring{fingName[2]}_ring{fingName[3]}_{name}": 2.9
        }

    pinky = {  
        f"pinky{fingName[0]}_pinky{fingName[1]}_{name}": 3.5,
        f"pinky{fingName[1]}_pinky{fingName[2]}_{name}": 1.9,
        f"pinky{fingName[2]}_pinky{fingName[3]}_{name}": 2.5
        }

    return limb, hand, handknuWidth, index, middle, ring, pinky 
#---------------------------------------------------------

def head_measurement_dict(name = "Max"):
    unit = "cm"

    neckLength = {
        f"neck1_2{name}": 5.5, 
        f"neck2_3{name}": 3   
    }

    neckWidth = {
        f"neckWidth_{name}": 10.9
    }

    headHeight = {f"chin_bridge_{name}":10.3}

    headWidth = {f"ear_ear_{name}":5.4}

    return neckLength, neckWidth, headHeight, headWidth
    

def head_measurement_dict(name = "Jae"):
    unit = "cm"
    
    neckLength = {
        f"neck1_2{name}": 6.5, 
        f"neck2_3{name}": 5   
    }

    neckWidth = {
        f"neckWidth_{name}": 11.4
    }

    headHeight = {f"chin_bridge_{name}":13.3}

    headWidth = {f"ear_ear_{name}":5.4}

    return neckLength, neckWidth, headHeight, headWidth