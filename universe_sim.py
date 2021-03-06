from vpython import *
e_graph = gcurve(color=color.blue)

#scientific constants/variables
G = (6.67*(10**-11)) # metres, kilograms and seconds, gravitational contstant
au = 149597870700 # metres, astronomical unit with scale
ms = 1.989*(10**30) # kilogramms, sun mass
me = 5.9722*(10**24) # kilogramms, earth mass
sl = 1 # light force of sun
sr = 695510 # sun radius in kilometres
er = 6371 # earth radius in kilometres
specific_heat_oxygen = 919 #J/(kg K)
specific_heat_iron = 449 #J/(kg K)
specific_heat_silicon = 710 #J/(kg K)
specific_heat_natrium = 1260 #J/(kg K)
specific_heat_graphite = 717 #J/(kg K)
specific_heat_helium = 5192 #J/(kg K)
specific_heat_hydrogen = 14300 #J/(kg K)

#programming constants/variables
dt = 60*10*2 #60 = 1 Minute
t = 0
t_real = 0
r = 30
# if programm is running continous true/false
programm_running = True
# if help click objects are visible or not
click_objects_visible = False
#Use real-world values of radius and visuals,
#good for simulations, bad for view
real_values_visuals = True
#asteroid created by click mass (*earths mass)
asteroid_mass = 0.4
#asteroid created by click momentum,
#1 dimensional (y-axis)
asteroid_momentum = vector(0,0,0)
#habital zone coloring of planets
habitable_zone = False

# [[mass(kg), radius(km), speed(m/s), pos(au), name(system), name(sun), scale(how much au the systems are apart),lightforce(relative to sun), texture file, hours per rotation]]
sun = [[0.89,sr,0,0,"solar_system","sun",0,1,specific_heat_hydrogen,15000000,"textures/sun.jpg",1587.28]]
trappist1_star = [[0.089,0.121*sr,0,32,"trappist1","trappist-1",32,5.22*(10**-4)]]
kepler11_star = [[0.95,1.10*sr,0,35,"kepler11","kepler-11",35,1.045]]

# [[mass(kg), radius(km), speed(m/s), pos(au), name(planet), name(planet system to which it belongs), specific heat capicity(average), main elements(list), average temperature(Kelvin), texture file, roation speed(hours per rotation)]]
trappist1 = [[0.97,6371,82854,0.0115,"a","trappist1"],[1.16,6371,71029,0.0158,"b","trappist1"],[0.3,6371,59902,0.0223,"c","trappist1"],[0.7,6371,45478,0.0293,"d","trappist1"],[0.93,6371,(2*3.14159265359*(0.0385*au))/(86400*9.21),0.0385,"e","trappist1"],[1.51,6371,(2*3.14*(0.0469*au))/(86400*12.35),0.0469,"f","trappist1"],[0.33,6371,(2*3.141592653594*(0.0619*au))/(86400*18.77),0.0619,"g","trappist1"]]

solar_system_planets = [
[0.055,2439.7,47360,0.387099273,"mercury","solar_system",(specific_heat_iron+specific_heat_oxygen+specific_heat_natrium)/3,["iron", "oxygen", "natrium"],440,"textures/mercury.jpg", 1407.5],
[0.815,6051.8,35020,0.723,"venus","solar_system",(specific_heat_oxygen+specific_heat_graphite)/2,["oxygen","carbon"],737,"textures/venus.jpg", 5832],
[1.0,6371,29722,1.0,"earth","solar_system",(specific_heat_oxygen+specific_heat_silicon)/2,["oxygen","silicon"],288,"textures/earth_8k.jpg", 24],
[0.01,1737.1,29722+1021.9334,1.0+0.00257356604,"earth - moon","solar_system",(specific_heat_oxygen+specific_heat_iron)/2,["oxygen","iron"],100,"textures/earth_moon.jpg", 655.2],
[0.107,3389.5,24130,1.524,"mars","solar_system",(specific_heat_iron+specific_heat_oxygen+specific_heat_natrium)/3,["iron", "oxygen", "natrium"],210,"textures/mars.jpg", 24.5],
[318,69911,13070,5.203,"jupiter","solar_system",(specific_heat_helium+specific_heat_hydrogen)/2,["hydrogen","helium"],165,"textures/jupiter.jpg", 9.9],
[95.16,58232,9690,9.5,"saturn","solar_system",(specific_heat_helium+specific_heat_hydrogen)/2,["hydrogen","helium"],134,"textures/saturn.jpg", 10.65],
[14.54,25362,6810,19.2,"uranus","solar_system",(specific_heat_helium+specific_heat_hydrogen)/2,["hydrogen","helium"],76,"textures/uranus.jpg", 17.2],
[17.15,24622,5430,30.1,"neptun","solar_system",(specific_heat_helium+specific_heat_hydrogen)/2,["hydrogen","helium"],72,"textures/neptune.jpg", 16.11]]

solar_system_sattelites = [[0.01230,6371/4,29722,1.00257,"erde_mond1","solar_system"]]
kepler11 = [[4.3,1.97*er,(2*3.141592653594*(0.091*au))/(86400*10.30),0.091,"b","kepler11"],[13.5,3.15*er,(2*3.141592653594*(0.106*au))/(86400*13.02),0.106,"c","kepler11"],[6.1,3.43*er,(2*3.141592653594*(0.159*au))/(86400*22.68),0.159,"d","kepler11"],[8.4,4.52*er,(2*3.141592653594*(0.1949*au))/(86400*31.99598),0.1949,"e","kepler11"],[2.34,2.612*er,(2*3.141592653594*(0.259*au))/(86400*46.688768),0.259,"f","kepler11"]]

#all suns in one list
stars_spec = []
stars_spec.extend(sun)
#stars_spec.extend(kepler11_star)
#stars_spec.extend(trappist1_star)
#all planets in one big list
planet_spec = []
planet_spec.extend(solar_system_planets)
#planet_spec.extend(kepler11)
#planet_spec.extend(trappist1)
# all systems with planets in one big list
systems_list=[]#[trappist1, solar_system]
systems_list.append(solar_system_planets)
#systems_list.append(kepler11)
#systems_list.append(trappist1)

#scene setup
scene = canvas(title='<b>Planetary System Simulation</b>\n',
     x=0, y=0, width=16*55, height=9*55,
     center=vector(0,0,0), background=vector(0,0,0))#, fov=pi/1.5)

#background_img = sphere( pos=vector(0,0,0), texture="textures/background.jpg", radius=40*au)

if real_values_visuals == False:
    scene.append_to_title('(Scaled visual values are used)\n\n')
else:
    scene.append_to_title('(Real visual values are used)\n\n')
scene.append_to_title('<div id="seperator"></div><br>')

# Basic functions(gforce, collision etc.)

def gforce(p1,p2):
    # Calculate the gravitational force exerted on p1 by p2.
    # Calculate distance vector between p1 and p2.
    r_vec = p1.pos-p2.pos
    # Calculate magnitude of distane vector.
    r_mag = mag(r_vec)
    # Calcualte unit vector of distance vector.
    r_hat = r_vec/r_mag
    # Calculate force magnitude.
    force_mag = G*p1.mass*p2.mass/r_mag**2
    # Calculate force vector.
    force_vec1 = -force_mag*r_hat
    force_vec = force_vec1

    return force_vec
#returns force vector between two objects

def collision_tf(p1,p2):
    r_vec = p1.pos-p2.pos
    r_mag = mag(r_vec)
    if r_mag >= (p1.radius + p2.radius):
        bol_var = False
    else:
        bol_var = True

    return bol_var
#returns true/false if objects collide or not

def collision(p1,p2):
    new_radius = p1.radius + p2.radius
    new_mass = p1.mass + p2.mass
    new_momentum = p1.momentum + p2.momentum
    
    energy_scale = ((1/2)*p1.mass*(mag(p1.momentum)**2))/((1/2)*p2.mass*(mag(p2.momentum)**2))
    mass_scale = p1.mass/p2.mass
    velocity_scale = mag(p1.momentum/p1.mass)/mag(p2.momentum/p2.mass)
    print("Relation of Energy, Mass and Velocity of colliding Objects: " + str(energy_scale) + "   " + str(mass_scale) + "   " + str(velocity_scale))
    
    ekin1 = (1/2)*p1.mass*(mag(p1.momentum/p1.mass)**2)
    ekin2 = (1/2)*p2.mass*(mag(p2.momentum/p2.mass)**2)

    #If energy is 100 times bigger than on other object
    #if mass_scale < (1/100):
    if p1.mass > p2.mass:
        if p2 in planets:
            li = planets.index(p2)
            labels[li].visible = False
            del labels[li]
            planets.remove(planets[li])
            for i in click_obj_planets: 
                if i.belonging == p2.belonging or i.belonging == p2.name:
                    click_obj_planets.remove(i)
                    i.visible = False
                    del i
        if p2 in stars:
            li_s = stars.index(p2)
            labels_s[li_s].visible = False
            del labels_s[li_s]
            stars.remove(stars[li_s])
        p2.visible = False
        del p2
        p1.mass = new_mass
        p1.radius = new_radius
        p1.momentum = new_momentum

        ekin_total = (1/2)*p1.mass*(mag(p1.momentum/p1.mass)**2)
        ekin_leftover = (ekin1+ekin2) - ekin_total
        temp_change = ekin_leftover/(p1.mass*p1.heat_capacity)
        p1.temp += temp_change

        return
    else:
        if p1 in planets:
            li = planets.index(p1)
            labels[li].visible = False
            del labels[li]
            planets.remove(planets[li])
            for i in click_obj_planets: 
                if i.belonging == p1.belonging or i.belonging == p1.name:
                    click_obj_planets.remove(i)
                    i.visible = False
                    del i
        if p1 in stars:
            li_s = stars.index(p1)
            labels_s[li_s].visible = False
            del labels_s[li_s]
            stars.remove(stars[li_s])
        p1.visible = False
        del p1
        p2.mass = new_mass
        p2.radius = new_radius
        p2.momentum = new_momentum

        ekin_total = (1/2)*p2.mass*(mag(p2.momentum/p2.mass)**2)
        ekin_leftover = (ekin1+ekin2) - ekin_total
        temp_change = ekin_leftover/(p2.mass*p2.heat_capacity)
        p2.temp += temp_change

        return
#forms to sphere together into one object

def chz(p1,sun):
    r_vec = p1.pos-sun.pos
    r_mag = mag(r_vec)
    if r_mag > (sun.radius + (au*2.1*sqrt(((sun.lightforce)/sl)))):
        p1.color = color.blue
    elif (sun.radius + (au*1*sqrt((sun.lightforce)/sl))) < r_mag < (sun.radius + (au*2.1*sqrt((sun.lightforce)/sl))):
        p1.color = color.cyan
    elif (sun.radius + (au*0.7*sqrt((sun.lightforce)/sl))) < r_mag <= (sun.radius + (au*1*sqrt((sun.lightforce)/sl))):
        pass#p1.color = color.green
    elif r_mag < (sun.radius + (au*0.7*sqrt((sun.lightforce)/sl))):
        p1.color = color.orange
    else:
        p1.color = color.red

    return
#color of p1 changes because of distance to sun

systems_strings=[]
#List of all star and planet objects. Everything can be found in here
stars=[]
planets=[]

#help objects
labels=[]
lights=[]
labels_s=[]
systems_scale=[]
click_obj_planets=[]
trails=[]
#currently selected object
selected="none selected"
def create_scene():
    #Planet creation
    for ps in planet_spec:
        for star in stars_spec:
            if star[4] == ps[5]:
                scale = star[6]
                radius_star = star[1]
        if real_values_visuals == True:
            p_r = ps[1]*1000
        else:
            p_r = (ps[1]/20)*radius_star
        
        #help functions because lists are not fully defined
        if len(ps)<9:
            ps.append(specific_heat_oxygen)
            ps.append("oxygen")
            ps.append(200)
        
        if len(ps)<10:
            planet = sphere( shininess=0, emissive=0, pos=vector((scale + ps[3])*au,0,0), radius=p_r, color=color.white, mass = ps[0]*me, momentum=vector(0,0,-ps[2]*ps[0]*me), make_trail=False, belonging=ps[5], name=ps[4], pickable=True, original_radius=ps[1], heat_capacity=ps[6], composition=ps[7], temp=ps[8], radians=ps[10] )
        else:     
            planet = sphere( shininess=0, emissive=0, pos=vector((scale + ps[3])*au,0,0), radius=p_r, color=color.white, mass = ps[0]*me, momentum=vector(0,0,-ps[2]*ps[0]*me), make_trail=False, belonging=ps[5], name=ps[4], pickable=True, original_radius=ps[1], heat_capacity=ps[6], composition=ps[7], temp=ps[8], radians=ps[10], texture=ps[9] )

        trail = attach_trail(planet, radius=planet.radius*30, color=color.white, retain=1000 )
        label_ps = label(pos=planet.pos, text=ps[4], xoffset=20, yoffset=12, space=planet.radius, height=10, border=6, font="sans", belonging=ps[5], original_name = ps[4])
        planet_click = sphere(  pos=planet.pos, radius=6*planet.radius, color=color.white, opacity=0.05, belonging=ps[4], belonging_system=ps[5] )
        click_obj_planets.append(planet_click)
        trails.append(trail)
        labels.append(label_ps)
        planets.append(planet)

    #Star creation
    for s in stars_spec:
        dist2 = 0
        for planet in planet_spec:
            if planet[5] == s[4]:
                if dist2 > planet[3]:
                    pass
                else:
                    dist2 = planet[3]
        dist = dist2*au
    
        s_r = s[1]*1000 if real_values_visuals else dist/80
        #if real_values_visuals == True:
            # s_r = s[1]
        #else:
            #s_r = (dist/20)

        star = sphere( shininess=1, emissive=1, pos=vector(s[3]*au,0,0), radius=s_r, color=color.yellow, mass = s[0]*ms, momentum=vector(0,0,-s[2]*s[0]*ms), make_trail=False, belonging = s[4], lightforce = s[7], name=s[5], pickable=True, original_radius=s[1], heat_capacity=s[8], temp=s[9], texture=s[10], radians=s[11] )
        trail = attach_trail(star, radius=(s_r/2), color=color.white )
        #lamp = local_light(pos=star.pos, color=color.yellow, belonging = s[4])
        label_star = label(pos=star.pos, text=s[5], xoffset=20, yoffset=12, space=star.radius, height=10, border=6, font="sans", belonging = s[4], original_name = s[5])
        if s[4] in systems_strings:
            pass
        else:
            systems_strings.append(s[4])
        labels_s.append(label_star)
        trails.append(trail)
        stars.append(star)
        #lights.append(lamp)
    for i in systems_list:
        x = i[-1]
        ra = x[3]*2
        for star in stars_spec:
            if x[5] == star[4]:
                pos_sys = star[2]
                belonging_s = star[4]
        scale_obj = sphere( pos=vector(0,pos_sys,0), radius=ra*au, color=color.white, make_trail=False, opacity = 0.2, visible=False, belonging=belonging_s )
        systems_scale.append(scale_obj)

    for l in labels:
        l.line = False
    for l in labels_s:
        l.line = False

create_scene()

scene.append_to_title('Select Planets/Stars in Simulation:\n\n')

lip = []
lip.append("none")
for z in systems_list:
    for i in z:
        lip.append(i[4])
def M(m):
    global selected
    for i in planet_spec:
        if i[4] == m.selected:
            #reset all label edits at stars
            for u in labels_s:
                u.linewidth = 1
            #reset all label edits at planets
            for ii in labels:
                ii.linewidth = 1
                #select label and get planet informations
                if ii.text == i[4]:
                    ii.line = False
                    ii.linewidth = 4
                    scene.center = ii.pos
                    selected=i[4]
                    choose_s.selected= "none"
                else:
                    choose_s.selected= "none"
    if m.selected == "none":
        for x in labels:
            x.linewidth = 1
        obj_t.text = "\n\n"
choose_p = menu( choices=lip, bind=M, value="planets" , pos=scene.title_anchor )

lip_s = []
lip_s.append("none")
for z in stars_spec:
    lip_s.append(z[5])
def M_S(m):
    global selected
    for i in stars_spec:
        if i[5] == m.selected:
            for u in labels:
                u.linewidth = 1
            for ii in labels_s:
                ii.linewidth = 1
                if ii.text == i[5]:
                    ii.line = False
                    ii.linewidth = 4
                    scene.center = ii.pos
                    selected=i[5]
                    choose_p.selected = "none"
                else:
                    choose_p.selected = "none"
    if m.selected == "none":
        for x in labels:
            x.linewidth = 1
        obj_t.text = "\n\n"
choose_s = menu( choices=lip_s, bind=M_S, value="stars" , pos=scene.title_anchor )

scene.append_to_title('\n\n')

#widgets
def S(s):
    global dt
    global n
    dt = s.value
    wt.text = str((dt*r)/60/60/24) + " days/second scaling.\n"
    n = 1
slider( bind=S, min=60*2, max=60*200*2, value=60*10*2, pos=scene.title_anchor, length=200)
wt = wtext(text=str((dt*r)/60/60/24) + " days/second scaling.\n", pos=scene.title_anchor)

n = 1
def B_faster(b):
    global dt
    global n
    dt += 60*20*5**n
    n += 1
    wt.text = str(round((dt/60)*2, 2)) + " minutes/second scaling.\n"
button( bind=B_faster, text='>>', pos=scene.title_anchor )

def B(b):
    global programm_running
    if programm_running == True:
        programm_running = False
        b.text = "&#9654;"
        return
    else:
        programm_running = True
        b.text = "||"
button( bind=B, text='||', pos=scene.title_anchor )

wt2 = wtext(text="Realtime/Time: " + str(round((t/60)/60, 1)) + "h/" + str(round(t_real, 1)) + "s", pos=scene.title_anchor)

obj_settings = wtext(text="\n\nAsteroid Settings:\n\n", pos=scene.title_anchor)

clickaction = False
def B_clickaction(b):
    global clickaction
    global click_objects_visible
    if clickaction == True:
        clickaction = False
        click_objects_visible = False
        b.text = '<img src="https://www.materialui.co/materialIcons/av/library_add_black_24x24.png"> OnClick Action: Asteroid creation'
        asteroid_momentum_winput.disabled=False
        asteroid_mass_winput.disabled=False
        return
    else:
        clickaction = True
        b.text = '<img src="https://www.materialui.co/materialIcons/action/touch_app_black_24x24.png"> OnClick Action: Object selection'
        asteroid_momentum_winput.disabled=True
        asteroid_mass_winput.disabled=True
        click_objects_visible = True

obj = scene.mouse.pick

button( bind=B_clickaction, text='<img src="https://www.materialui.co/materialIcons/av/library_add_black_24x24.png"> OnClick Action: Asteroid creation', pos=scene.title_anchor )
asteroid_density_text =  wtext(text='\n\nRadius: Earths Radius (6371 km)\nDensity: ' + str(round(((asteroid_mass*me)/((4/3)*pi*((er*1000)**3)))/1000, 2)) + ' g/cm3\n', pos=scene.title_anchor)

def asteroid_momentum_func(s):
    global asteroid_momentum
    global asteroid_mass
    asteroid_momentum = vector(0,s.number*(asteroid_mass*me),0)
asteroid_momentum_winput = winput( bind=asteroid_momentum_func, text="0", pos=scene.title_anchor )
wt_am = wtext(text=" m/s speed (y-axis)", pos=scene.title_anchor)

scene.append_to_title('\n')

def asteroid_mass_func(s):
    global asteroid_mass
    asteroid_mass = s.number
asteroid_mass_winput = winput( bind=asteroid_mass_func, text="0.4", pos=scene.title_anchor)
wt_ama = wtext(text="*me kg", pos=scene.title_anchor)

scene.append_to_title('\n\nSettings:\n\n')

def B_clear_trails(b):
    for x in trails:
        x.clear()
button( bind=B_clear_trails, text='<img src="https://www.materialui.co/materialIcons/action/highlight_off_black_24x24.png"> Clear all trails', pos=scene.title_anchor )
scene.append_to_title('\n')

#too much for interface, always true
better_view = True
#def B_better_view(b):
#    global better_view
#    if better_view == False:
#        b.text = '<img src="https://www.materialui.co/materialIcons/image/camera_black_24x24.png"> Better view (of solar systems)'
#        better_view = True
#        return
#    else:
#        b.text = '<img src="https://www.materialui.co/materialIcons/image/camera_grey_24x24.png"> Normal view'
#        better_view = False
#button( bind=B_better_view, text='<img src="https://www.materialui.co/materialIcons/image/camera_grey_24x24.png"> Normal view', pos=scene.title_anchor )

following = True
scene.append_to_title('\n')
def B_following(b):
    global following
    if following == True:
        following = False
        b.text = 'Camera not following targets'
        return
    else:
        following = True
        b.text = 'Camera following targets'
checkbox( bind=B_following, text='Camera following targets', pos=scene.title_anchor )
scene.append_to_title('\n')

trails_tf = True
def B_stop_trails(b):
    global trails_tf
    if trails_tf == True:
        trails_tf = False
        b.text = 'Trails: False'
        for x in trails:
            x.stop()
        return
    else:
        trails_tf = True
        b.text = 'Trails: True'
        for x in trails:
            x.start()
checkbox( bind=B_stop_trails, text='Trails: True', pos=scene.title_anchor )

obj_sm = wtext(text="\n\nSandboxmode Settings:\n\n", pos=scene.title_anchor)

sandbox_mode = False
sandbox_mode_timer = 0
testarrows=[]
def sandbox_modef(b):
    global sandbox_mode
    global testarrows
    if sandbox_mode == True:
        sandbox_mode = False
        #setting the camera to look downwards a bit
        scene.camera.pos += vector(0,17*au,0)
        scene.camera.axis += vector(0,17*-au,0)
        b.text = 'Sandboxmode: Off'
        create_scene()
        for i in testarrows:
            i.visible = False
            del i
        testarrows.clear()
        return
    else:
        sandbox_mode = True
        scene.center = vector(0,0,0)
        b.text = 'Sandboxmode: On'
        for i in planets:
            i.visible = False
            del i
        planets.clear()
        for i in stars:
            i.visible = False
            del i
        stars.clear()
        for i in labels:
            i.visible = False
            del i
        labels.clear()
        for i in labels_s:
            i.visible = False
            del i
        labels_s.clear()
        for i in trails:
            i.clear()
            del i
        trails.clear()
        for i in click_obj_planets:
            i.visible = False
            del i
        click_obj_planets.clear()
        pointerx = arrow(pos=vector(0,0,0), axis=vector(4*au,0,0), color=vector(1,1,1))
        pointery = arrow(pos=vector(0,0,0), axis=vector(0,4*au,0), color=vector(1,0,1))
        pointerz = arrow(pos=vector(0,0,0), axis=vector(0,0,4*au), color=vector(0,1,1))
        testarrows.append(pointerx)
        testarrows.append(pointery)
        testarrows.append(pointerz)
checkbox( bind=sandbox_modef, text='Sandboxmode: Off', pos=scene.title_anchor )

graph_plot = graph(scroll=True, fast=False, xmin=0, xmax=1, title=str(selected), xtitle="Time [s]", ytitle="Velocity [m/s]", width=16*40, height=9*25)
plot_s = gcurve(label="Velocity", color=color.red)

drag = False
s_obj = None # declare s to be used below
int_var = 0
def down():
    global s_obj, drag, selected
    if clickaction == True:
        for label1 in labels:
            planet_i = labels.index(label1)
            planet_obj = planets[planet_i]
            planet_click_obj = click_obj_planets[planet_i]
            obj = scene.mouse.pick
            if (obj == planet_click_obj): #mag(planet_obj.pos - evt.pos) < planet_obj.radius**1.15:
                for ii in labels_s:
                    ii.linewidth = 1
                for iii in labels:
                    iii.linewidth = 1
                label1.line = False
                label1.linewidth = 4
                if "asteroid" in planet_obj.name:
                    choose_s.selected = "none"
                    choose_p.selected = "none"
                    selected=planet_obj.name
                else:
                    choose_s.selected = "none"
                    choose_p.selected = label1.text
                    selected=planet_obj.name
    else:
        # give asteroid a belonging system by finding the nearest star
        distances=[]
        names=[]
        for i in stars:
            distance = i.pos-scene.mouse.pos
            distances.append(mag(distance))
            names.append(i.belonging)
        try:
            index_worth = distances.index(min(distances))
            system = names[index_worth]
            if min(distances)>10*au: system="none"
        except:
            system="none"
        # create asteroid
        global int_var
        loc = scene.mouse.pos
        global asteroid_momentum
        global asteroid_mass

        as_planet = sphere(pos=loc, radius=er*1000, color=color.white, mass=asteroid_mass*me, momentum=asteroid_momentum, belonging="asteroid"+str(int_var), belonging_system=system, name="asteroid"+str(int_var), heat_capacity=specific_heat_graphite, temp=200, radians="none")
        label_ps = label(pos=as_planet.pos, text="asteroid"+str(int_var), xoffset=20, yoffset=12, space=as_planet.radius, height=10, border=6, font="sans", belonging=system )
        planet_click = sphere(  pos=as_planet.pos, radius=16*as_planet.radius, color=color.white, opacity=0.1, belonging=as_planet.belonging, belonging_system=system )
        label_ps.line = False
        click_obj_planets.append(planet_click)
        planets.append(as_planet)
        labels.append(label_ps)
        int_var += 1
        s_obj = as_planet
    drag = True

def move():
    global drag, s_obj
    if drag: # mouse button is down
        s_obj.pos = scene.mouse.pos

def up():
    global drag, s_obj
    s_obj.color = color.cyan
    drag = False

scene.bind("mousedown", down)
scene.bind("mousemove", move)
scene.bind("mouseup", up)

obj_t = wtext(text="", pos=scene.title_anchor)

obj_g = wtext(text="\n<div id='test'>Environmental Settings:\n\n", pos=scene.caption_anchor)
def ev_g(s):
    global G
    G = G*s.value
    wt_g.text = "G: " + str(G) + " m^3/kg*s^2"
sliderg = slider( bind=ev_g, min=0, max=2, value=1, pos=scene.caption_anchor, length=200)
wt_g = wtext(text="G: 6.67e-11 m^3/kg*s^2", pos=scene.caption_anchor)

#setting the camera to look downwards a bit
scene.camera.pos += vector(0,17*au,0)
scene.camera.axis += vector(0,17*-au,0)

#while loop
for star in stars: star.force = vector(0,0,0)
for planet in planets: planet.force = vector(0,0,0)

while (t >-1):#
    rate(r) #time
    
    #sandbox_mode start initialisation
    if sandbox_mode == True:
        if sandbox_mode_timer > 15:
            for i in testarrows:
                i.visible = False
        if sandbox_mode_timer > 30:
            for i in testarrows:
                i.visible = True
        if sandbox_mode_timer > 45:
            for i in testarrows:
                i.visible = False
        if sandbox_mode_timer > 60:
            for i in testarrows:
                i.visible = True
        sandbox_mode_timer += 1
        if sandbox_mode_timer > 75:
            for i in testarrows:
                i.visible = True
                i.opacity = 0.2
                
    #obj = scene.mouse.pick
    #for i in click_obj_planets:
    #    if obj==i:
    #        i.opacity=0.5
    #    else:
    #        i.opacity=0.05
    
    for i in click_obj_planets: i.radius=scene.range/25
    if click_objects_visible==True:
        for x in click_obj_planets:
            x.visible = True
    if click_objects_visible==False:
        for y in click_obj_planets:
            y.visible = False
    
    
    # Position check on scale
    if better_view == True:
        for i in systems_scale:
            for star in stars:
                if i.belonging == star.belonging:
                    star_pos = star.pos
                    star_searched = star
                    i.pos = star_pos
                    i.opacity = 0.2
                    pos_star_label = stars.index(star)
                    f = labels_s[pos_star_label]
                    for label_p in labels:
                        if label_p.belonging == star_searched.belonging:
                            label_p.visible = False
                            f.text == star_searched.belonging
                
                            if scene.range/2 > i.radius > scene.range/4:
                                i.visible = True
                                i.opacity = 0.2
                                label_p.visible = False
                                f.text = i.belonging
                                click_objects_visible = False
                
                            elif scene.range/4 > i.radius:
                                i.visible = True
                                i.opacity = 0.2 #0.9 for better visualization over long distance
                                label_p.visible = False
                                f.text = i.belonging
                                click_objects_visible = False
                            else:
                                label_p.visible = True
                                i.visible = False
                                f.text = f.original_name
                                if click_objects_visible==False:
                                    pass
                                else:
                                    click_objects_visible = True

            
    else:
        for l in labels:
            l.visible = True
        for x in labels_s:
            x.visible = True
            x.text = x.original_name
        for i in systems_scale:
            i.visible = False
    
    if programm_running == True: # if program_runs_continuous
        # Calculate forces
        for star in stars: 
            star.force = vector(0,0,0)
            for planet in planets:
                star.force += gforce(star,planet)
            for star_other in stars:
                if not star is star_other: star.force += gforce(star,star_other)

        #star.force=star.force + gforce(star,planets[0]) +gforce(star,planet2)+gforce(star,planet3)+gforce(star,planet4)
        for planet in planets:
            planet.force = vector(0,0,0)
            for star in stars:
                planet.force += gforce(planet,star)
            for planet_other in planets:
                if not planet is planet_other: planet.force += gforce(planet,planet_other)

        # Update momenta.
        for star in stars: star.momentum += star.force*dt
        for planet in planets: planet.momentum += planet.force*dt

        # Update positions.
        for x,star in enumerate(stars):
            star.pos += star.momentum/star.mass*dt
            labels_s[x].pos = star.pos

        #for planet in planets:
        for y,planet in enumerate(planets):
            planet.pos += planet.momentum/planet.mass*dt
            labels[y].pos = planet.pos
        
        # Update light of star.
        #for i in lights:
        #    for s in stars:
        #        if i.belonging == s.belonging:
        #            i.pos = s.pos
        
        # Check collisons.
        for star in stars:
            for planet in planets:
                if collision_tf(star,planet) == True:
                    collision(star,planet)
                else:
                    pass

        for planet in planets:
            for planet_other in planets:
                if not planet is planet_other:
                    if collision_tf(planet,planet_other) == True:
                        collision(planet,planet_other)
                    else:
                        pass

        for star in stars:
            for star_other in stars:
                if not star is star_other:
                    if collision_tf(star,star_other) == True:
                        collision(star,star_other)
                    else:
                        pass

        if habitable_zone == True:
            for star in stars:
                for planet in planets:
                    if star.belonging == planet.belonging:
                        chz(planet,star)

        #clickobjects position update
        for i in click_obj_planets:
            for p in planets:
                if p.name == i.belonging:
                    i.pos = p.pos
                elif p.belonging == i.belonging:
                    i.pos = p.pos
                    
        # Update positions if camera follows a planet/star
        if following == True:
            if choose_p.selected is not "none" and choose_s.selected is "none":
                for planet in planets:
                    if planet.name == choose_p.selected:
                        scene.center = planet.pos
                        plot_s.plot( pos = [t , mag(planet.momentum)/planet.mass] )
                        graph_plot.xmax = t
                        graph_plot.title=str(selected)
                    elif planet.belonging == selected:
                        scene.center = planet.pos
                        plot_s.plot( pos = [t , mag(planet.momentum)/planet.mass] )
                        graph_plot.xmax = t
                        graph_plot.title=str(selected)
                    else:
                        pass

        if following == True:
            if choose_s.selected is not "none" and choose_p.selected is "none":
                for star in stars:
                    if star.name == choose_s.selected:
                        scene.center = star.pos
                        plot_s.plot( pos = [t , mag(star.momentum)/star.mass] )
                        graph_plot.xmax = t
                        graph_plot.title=str(selected)
                        
        if following == True:
            if choose_s.selected is "none" and choose_p.selected is "none":
                for planet in planets:
                    if planet.belonging == selected:
                        scene.center = planet.pos
                        plot_s.plot( pos = [t , mag(planet.momentum)/star.mass] )
                        graph_plot.xmax = t
                        graph_plot.title=str(selected)
        
        for i in planets:
            if i.name == selected:
                obj_t.text = i.name
                obj_t.text =  '\n<div id="data">' + '<b>' + i.name +'</b> <span style="color: green;">Present</span> | Values:\n' + str(round(i.mass/me, 2)) + '*earths mass\n' + str(round(mag(i.momentum)/i.mass, 2)) + ' m/s velocity\n' + str(i.temp) + 'K average teperature (' + str(round(i.temp-273.15, 1)) + ' °C)\n' + str(round((i.mass/((4/3)*pi*(i.radius**3)))/1000, 2)) + ' g/cm3 (average density)\n' + str(i.radians) + ' hours per rotation </div>' 
                asteroid_momentum = (i.momentum/i.mass)*(asteroid_mass*me)
                asteroid_momentum_winput.disabled=True
        for i in stars:
            if i.name == selected:
                obj_t.text = i.name
                obj_t.text =  '\n<div id="data">' + '<b>' + i.name +'</b> <span style="color: green;">Present</span> | Values:\n' + str(round(i.mass/ms, 2)) + '*suns mass\n' + str(round(mag(i.momentum)/i.mass, 2)) + ' m/s velocity\n'  + str(i.temp) + 'K average teperature (' + str(round(i.temp-273.15, 1)) + ' °C)\n' + str(round((i.mass/((4/3)*pi*(i.radius**3)))/1000, 2)) + ' g/cm3 (average density)\n' + str(i.radians) + ' hours per rotation </div>'
                asteroid_momentum = (i.momentum/i.mass)*(asteroid_mass*me)
                asteroid_momentum_winput.disabled=True
        if selected == "none":
            obj_t.text =  '\n<div id="data"><span style="color: red;">Object Destroyed</span></div>'
            asteroid_momentum_winput.disabled=False
        
        asteroid_density_text.text = '\n\nRadius: Earths Radius (6371 km)\nDensity: ' + str(round(((asteroid_mass*me)/((4/3)*pi*((er*1000)**3)))/1000, 2)) + ' g/cm3\n'
        
        #rotation of objects
        for p in planets:
            if p.radians == "none":
                pass
            else:
                radians_var = 360*(dt/60/60/p.radians)
                p.rotate(angle = radians(radians_var), axis = vec(0, 1, 0))
        for s in stars:
            if s.radians == "none":
                pass
            else:
                radians_var = 360*(dt/60/60/s.radians)
                s.rotate(angle = radians(radians_var), axis = vec(0, 1, 0))
        
        for p in planets:
            velocity_p = mag(p.momentum)/p.mass
            if velocity_p > 299792458:
                velocity_p = 299792457
        for s in stars:
            velocity = mag(s.momentum)/s.mass
            if velocity > 299792458:
                velocity = 299792457

        if t == 60*5:
            scene.autoscale = False
        t += dt
        t_real += 1/r
        wt2.text = "Realtime/Time: " + str(round((t/60)/60, 1)) + "h/" + str(round(t_real, 1)) + "s"

