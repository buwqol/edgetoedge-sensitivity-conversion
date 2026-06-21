## Overview
A quick breakdown of how you do edge to edge sensitivity conversions across different resolutions (mostly tailored to Valorant, but the math general enough to be adapted into whatever game).

## Disclaimer
I don't think any of this is necessarily beneficial at all. I'm in the camp that playing on different sensitivities is not at all harmful, and might even be productive to accelerating raw mouse control. I don't believe in 'muscle memory' when it comes to aim - I don't think forcing yourself to play on the same sensitivity just because it's what you're used to is particularly helpful. Don't be afraid to experiment with whatever feels comfortable from time to time.

With that being said, I do think the math behind it is interesting, so here it is.

## The math
Valorant has a fixed horizontal FOV of 103, and a fixed aspect ratio of 16:9
(Note: I say fixed, it's obviously bypass-able if you use true stretched, but initially these are locked values)

For our screen-edge to screen-edge sensitivity conversions, we need to recalculate our horizontal FOV, as it changes when we use true-stretched. This is what causes your normal sensitivity to **feel** faster, even though the cm/360 hasn't changed.

Lucky for us, the vertical FOV is **actually** fixed, and doesn't change regardless of which resolution you use (native, stretched, true-stretched, etc.)

To get our vertical FOV, all we need to do is the following:


$$
v = 2\cdot\arctan\left(\tan\left(\frac{h\mathrm{_original}}{2}\right)\div a\mathrm{_original}\right)
$$


Where:
- $v$ is our vertical FOV (constant value),
- $h\mathrm{_original}$ is our original horizontal FOV, 
- and $a\mathrm{_original}$ is our original aspect ratio $(\frac{\text{resolution width}}{\text{resolution height}})$. 

(Also note that in this case I'm accepting our FOVs in degrees rather than radians, but in a program you'll (probably) have to first convert your $h\mathrm{_original}$ to radians)

Again, in the case of Valorant, this is a fixed value:


$$
v = 2\cdot\arctan\left(\tan\left(\frac{103}{2}\right)\div\mathrm{\frac{16}{9}}\right)\approx70.5328\degree
$$


Now that we have our vertical FOV, to get our new horizontal FOV:


$$
h\mathrm{_new} = 2\cdot\arctan\left(\tan\left(\frac{v}{2}\right)\cdot a\mathrm{_new}\right)
$$


Where:
- $v$ is our vertical FOV (constant value),
- $h\mathrm{_new}$ is our new horizontal FOV, 
- and $a\mathrm{_new}$ is our new aspect ratio $(\frac{\text{resolution width}}{\text{resolution height}})$. 

With our new horizontal FOV, we can find the ratio between the old and new, which will then act as our sensitivity multiplier ($s$):


$$
\frac{h_\mathrm{new}}{h_\mathrm{old}} = \text{s}
$$


Then, just multiply $s$ with your original sensitivity, and you'll get your new sensitivity!

For example, if:
- my new resolution is $1024\times768$
- my original sensitivity is $0.555$


$$
h\mathrm{_new} = 2\cdot\arctan\left(\tan\left(\frac{v}{2}\right)\cdot\frac{1024}{768}\right) \approx 86.63197\degree,
$$


$$
\frac{h_\mathrm{new}}{103} = \text{s} \approx 0.8410870958626299,
$$


$$
\text{new sensitivity} = s \cdot 0.555 \approx 0.467
$$


That's it!

## Disadvantage & a work-around

Unfortunately, this comes at the disadvantage of scaling down your vertical sensitivity along side it. We can counteract it by using something like [rawaccel's](https://github.com/RawAccelOfficial/rawaccel) scaling feature, which lets you disconnect the X and Y scaling (you don't need to actually use an acceleration curve, you can literally just use it to change your X:Y ratio).

For this, install rawaccel, uncheck "Lock X & Y" and set the "Y/X Ratio" to the inverse of whatever you calculated for s.

For example, using the same results from the prior example, I would set my "Y/X Ratio" parameter to:


$$
\frac{1}{s} \approx 1.188937513034113
$$


I don't think this automatically applies on startup, so you might want to manually set that up (I'm not going to go over how, it's very easy).

That's really it.

## The code

Here's a little python script that'll hopefully help illustrate how you would go about doing it in code:

```python
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
print(f'New sens: {round(ORIG_SENS * mult, 3)}') # idk valo only has sensitivities to 3 decimal places 
```

That's **actually** it, have fun!