import math

# change these
ORIG_SENS = 0.555
NEW_RES_X = 1024
NEW_RES_Y = 768

def edgeToEdgeMult(
        newAspectRatio, 
        origAspectRatio=(16.0/9.0), # valo's aspect ratio is 'locked' at 16:9
        origHorizFOV=103.0          # valo's horizontal FOV is 'locked' at 103
        ):
    vertFOV = 2.0 * math.atan(
        math.tan(math.radians(origHorizFOV) / 2.0) / origAspectRatio
    )

    newHorizFOV = math.degrees(
        2.0 * math.atan(
            math.tan(vertFOV / 2.0) * newAspectRatio
        )
    )

    return newHorizFOV / origHorizFOV

mult = edgeToEdgeMult(float(NEW_RES_X)/float(NEW_RES_Y))

print(f'Sens multiplier: {mult}')
print(f'Rawaccel \'Y/X Ratio\' value: {1.0/mult}')
print(f'New sens: {round(ORIG_SENS * mult, 3)}') # idk valo only has sensitivies to 3 decimal places 