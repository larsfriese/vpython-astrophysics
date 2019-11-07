from vpython import *
e_graph = gcurve(color=color.blue)

#global constans
G = (6.67*(10**-11)) # metres, kilograms and seconds, gravitational contstant
au = 149597870700 # metres, astronomical unit with scale
ms = 1.989*(10**30) # kilogramms, sun mass
me = 5.9722*(10**24) # kilogramms, earth mass
sl = 1 # light force of sun

click_objects_visible = False
# if help click objects are visible or not
real_values_visuals = False
#Use real-world values of radius and visuals,
#good for simulations, bad for view
asteroid_mass = 0.4
#asteroid created by click mass
asteroid_momentum = 0
#asteroid created by click momentum,
#1 dimensional

#for the engine needed vaviables are 'stars_spec', 'planet_spec' and 'systems_list'
sr = 695510 # sun radius in kilometres
er = 6371 # earth radius in kilometres

#sonnenmassen,radius(km),speed,pos in au,name for planetsystem, name sun, scale for scale_obj(distance),light force sun
sun = [[0.89,sr,0,0,"solar_system","sun",0,1]]
trappist1_star = [[0.089,0.121*sr,0,0.5,"trappist1","trappist-1",2,5.22*(10**-4)]]
kepler11_star = [[0.95,1.10*sr,0,14,"kepler11","kepler-11",14,1.045]]

# erdmassen,radius(km),speed,pos in au,name for tag,planet system
trappist1 = [[0.97,6371,82854,0.0115,"a","trappist1"],[1.16,6371,71029,0.0158,"b","trappist1"],[0.3,6371,59902,0.0223,"c","trappist1"],[0.7,6371,45478,0.0293,"d","trappist1"],[0.93,6371,(2*3.14159265359*(0.0385*au))/(86400*9.21),0.0385,"e","trappist1"],[1.51,6371,(2*3.14*(0.0469*au))/(86400*12.35),0.0469,"f","trappist1"],[0.33,6371,(2*3.141592653594*(0.0619*au))/(86400*18.77),0.0619,"g","trappist1"]]
solar_system_planets = [[0.055,2439.7,47360,0.387099273,"merkur","solar_system"],[0.815,6051.8,35020,0.723,"venus","solar_system"],[1.0,6371,29722,1.0,"erde","solar_system"],[0.107,3389.5,24130,1.524,"mars","solar_system"]]
solar_system_sattelites = [[0.01230,6371/4,29722,1.00257,"erde_mond1","solar_system"]]
kepler11 = [[4.3,1.97*er,(2*3.141592653594*(0.091*au))/(86400*10.30),0.091,"b","kepler11"],[13.5,3.15*er,(2*3.141592653594*(0.106*au))/(86400*13.02),0.106,"c","kepler11"],[6.1,3.43*er,(2*3.141592653594*(0.159*au))/(86400*22.68),0.159,"d","kepler11"],[8.4,4.52*er,(2*3.141592653594*(0.1949*au))/(86400*31.99598),0.1949,"e","kepler11"],[2.34,2.612*er,(2*3.141592653594*(0.259*au))/(86400*46.688768),0.259,"f","kepler11"]]

#all suns in one list
stars_spec = sun + kepler11_star + trappist1_star
#all planets in one big list
planet_spec = solar_system_planets + kepler11 + trappist1
# all systems
systems_list=[solar_system_planets, kepler11, trappist1]#[trappist1, solar_system]


scene = canvas(title='<b>Planetary System Simulation</b>\n',
     x=0, y=0, width=16*55, height=9*55,
     center=vector(0,0,0), background=vector(0,0,0))

if real_values_visuals == False:
    scene.append_to_title('(Scaled visual values are used)\n\n')
else:
    scene.append_to_title('(Real visual values are used)\n\n')
scene.append_to_title('<div id="seperator"></div><br>')
#basic functions(gforce, collision etc.)

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
    r_vec = p1.pos-p2.pos
    new_radius = p1.radius + p2.radius
    new_mass = p1.mass + p2.mass
    new_momentum = p1.momentum + p2.momentum

    if p2 in planets:
        li = planets.index(p2)
        labels[li].visible = False
        del labels[li]
        planets.remove(planets[li])
        for i in click_obj_planets: 
            if i.belonging == p2.belonging:
                click_obj_planets.remove(i)
                i.visible = False
                del i
                return
            if i.belonging == p2.name:
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
        p1.color = color.green
    elif r_mag < (sun.radius + (au*0.7*sqrt((sun.lightforce)/sl))):
        p1.color = color.orange
    else:
        p1.color = color.red

    return
#color of p1 changes because of distance to sun

#planet systems
#radius doesnt have to be scaled a it is not YET important to the calculations

#star = sphere( pos=vector(0,0,0), radius=84179700*radius_zoom, color=color.yellow, mass = int(0.089*ms), momentum=vector(0,0,0), make_trail=True, shininess = 1, texture = "http://i.imgur.com/yoEzbtg.jpg"  )
#label_star = label(pos=star.pos, text="trappist-1", xoffset=20, yoffset=12, space=star.radius, height=10, border=6, font="sans")
#trappist1_scale = sphere( pos=vector(0,0,0), radius=0.2*au, color=color.white, make_trail=True, opacity = 0.2, visible=False )
#star = sphere( pos=vector(0,0,0), radius=84179700*radius_zoom, color=color.yellow, mass = int(ms), momentum=vector(0,0,0), make_trail=True )
#label_star = label(pos=star.pos, text="sonne", xoffset=20, yoffset=12, space=star.radius, height=10, border=6, font="sans")

systems_strings=[]
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
selected="none"

for ps in planet_spec:
    for star in stars_spec:
        if star[4] == ps[5]:
            scale = star[6]
            radius_star = star[1]
    if real_values_visuals == True:
        p_r = ps[1]
    else:
        p_r = (ps[1]/20)*radius_star

    planet = sphere( pos=vector((scale + ps[3])*au,0,0), radius=p_r, color=color.white, mass = ps[0]*me, momentum=vector(0,ps[2]*ps[0]*me,0), make_trail=False, belonging=ps[5], name=ps[4], pickable=True, original_radius=ps[1] )
    trail = attach_trail(planet, radius=planet.radius, color=color.white, retain=1000 )
    label_ps = label(pos=planet.pos, text=ps[4], xoffset=20, yoffset=12, space=planet.radius, height=10, border=6, font="sans", belonging=ps[5], original_name = ps[4])
    planet_click = sphere(  pos=planet.pos, radius=6*planet.radius, color=color.white, opacity=0.05, belonging=ps[4], belonging_system=ps[5] )
    click_obj_planets.append(planet_click)
    trails.append(trail)
    labels.append(label_ps)
    planets.append(planet)


for s in stars_spec:
    dist2 = 0
    for planet in planet_spec:
        if planet[5] == s[4]:
            if dist2 > planet[3]:
                pass
            else:
                dist2 = planet[3]
    dist = dist2*au
    
    s_r = s[1] if real_values_visuals else dist/20
    #if real_values_visuals == True:
       # s_r = s[1]
    #else:
        #s_r = (dist/20)
        
    star = sphere( pos=vector(s[3]*au,0,0), radius=s_r, color=color.yellow, mass = s[0]*ms, momentum=vector(0,s[2]*s[0]*ms,0), make_trail=False, belonging = s[4], lightforce = s[7], name=s[5], pickable=True, original_radius=s[1] )
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
    r = x[3]*2
    for star in stars_spec:
        if x[-1] == star[4]:
            pos_sys = star[2]
            belonging_s = star[4]
    scale_obj = sphere( pos=vector(0,pos_sys,0), radius=r*au, color=color.white, make_trail=False, opacity = 0.2, visible=False, belonging=belonging_s )
    systems_scale.append(scale_obj)

for l in labels:
    l.line = False
for l in labels_s:
    l.line = False

scene.append_to_title('Select Planets/Stars in Simulation:\n\n')

lip = []
lip.append("none")
for z in systems_list:
    for i in z:
        lip.append(i[4])
def M(m):
    global selected
    objex = '<span style="color: black;">(Destroyed)</span>'
    for i in planets:
        if i.name == m.selected:
            objex = '<span style="color: green;">(Present)</span>'
    for i in planet_spec:
        if i[4] == m.selected:
            for u in labels_s:
                u.linewidth = 1
            for ii in labels:
                ii.linewidth = 1
                if ii.text == i[4]:
                    ii.line = False
                    ii.linewidth = 4
                    scene.center = ii.pos
                    selected=i[4]
                    obj_t.text =  '\n<div id="data">' + '<b>' + i[4] +'</b> ' + objex + ' | Initial Values:\n' + str(i[0]) + '*earths mass\n' + str(round(i[2], 2)) + ' m/s velocity\n' + str(i[3]) + '*astronomical unit, \noriginal distance to star</div>\n'
                    choose_s.selected= "none"
                else:
                    obj_t.text =  '\n<div id="data">' + '<b>' + i[4] +'</b> ' + objex + ' | Initial Values:\n' + str(i[0]) + '*earths mass\n' + str(round(i[2], 2)) + ' m/s velocity\n' + str(i[3]) + '*astronomical unit, \noriginal distance to star</div>\n'
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
    objex = '<span style="color: black;">(Destroyed)</span>'
    for s in stars:
        if s.name == m.selected:
            objex = '<span style="color: green;">(Present)</span>'
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
                    obj_t.text =  '\n<div id="data">' + '<b>' + i[5] +'</b> ' + objex + ' | Initial Values:\n' + str(i[0]) + '*suns mass\n' + str(round(i[2], 2)) + ' m/s velocity\n' + str(i[3]) + '*astronomical unit, \ndistance to 0-point \nof coordinate system.</div>\n'
                    choose_p.selected = "none"
                else:
                    obj_t.text =  '\n<div id="data">' + '<b>' + i[5] +'</b> ' + objex + ' | Initial Values:\n' + str(i[0]) + '*suns mass\n' + str(round(i[2], 2)) + ' m/s velocity\n' + str(i[3]) + '*astronomical unit, \ndistance to 0-point \nof coordinate system.</div>\n'
                    choose_p.selected = "none"
    if m.selected == "none":
        for x in labels:
            x.linewidth = 1
        obj_t.text = "\n\n"
choose_s = menu( choices=lip_s, bind=M_S, value="stars" , pos=scene.title_anchor )

scene.append_to_title('\n\n')

dt = 60*10*2 #60 = 1 Minute
t = 0
t_real = 0
r = 30
bu = True

#widgets
def S(s):
    global dt
    dt = s.value
    wt.text = str(round((dt/60)*2, 2)) + " minutes/second scaling.\n"
slider( bind=S, min=60*2, max=60*200*2, value=60*10*2, pos=scene.title_anchor, length=200)
wt = wtext(text=str(round((dt/60)*2, 2)) + " minutes/second scaling.\n", pos=scene.title_anchor)

def B_faster(b):
    global dt
    dt += 60*20*2
    wt.text = str(round((dt/60)*2, 2)) + " minutes/second scaling.\n"
button( bind=B_faster, text='>>', pos=scene.title_anchor )

def B(b):
    global bu
    if bu == True:
        bu = False
        b.text = "&#9654;"
        return
    else:
        bu = True
        b.text = "||"
button( bind=B, text='||', pos=scene.title_anchor )

wt2 = wtext(text="Realtime/Time: " + str(round((t/60)/60, 1)) + "h/" + str(round(t_real, 1)) + "s", pos=scene.title_anchor)

scene.append_to_title('<div id="seperator"></div>')

clickaction = False
def B_clickaction(b):
    global clickaction
    global click_objects_visible
    if clickaction == True:
        clickaction = False
        click_objects_visible = False
        b.text = '<div class="tooltip"><img src="https://www.materialui.co/materialIcons/av/library_add_black_24x24.png"><span class="tooltiptext">OnClick Action: Asteroid creation</span></div>'
        return
    else:
        clickaction = True
        b.text = '<div class="tooltip"><img src="https://www.materialui.co/materialIcons/action/touch_app_black_24x24.png"><span class="tooltiptext">OnClick Action: Object selection</span></div>'
        click_objects_visible = True

obj = scene.mouse.pick

#click functions
#def asteroid(evt):
#    if clickaction == False:
#        loc = evt.pos
#        planet = sphere(pos=loc, radius=5417900*radius_zoom, color=color.white, mass=asteroid_mass, momentum=vector(0,asteroid_momentum,0), belonging="asteroid")
#        label_ps = label(pos=planet.pos, text="asteroid", xoffset=20, yoffset=12, space=planet.radius, height=10, border=6, font="sans" )
#        planets.append(planet)
#        labels.append(label_ps)
int = 0
def activateLabelOrAsteroid(evt):
    global selected
    if clickaction == True:
        for label1 in labels:
            planet_i = labels.index(label1)
            planet_obj = planets[planet_i]
            planet_click_obj = click_obj_planets[planet_i]
            try:
                yy = planet_spec[planet_i]
            except:
                yy = "Unknown"
            obj = scene.mouse.pick
            if (obj == planet_click_obj): #mag(planet_obj.pos - evt.pos) < planet_obj.radius**1.15:
                for ii in labels_s:
                    ii.linewidth = 1
                for iii in labels:
                    iii.linewidth = 1
                label1.line = False
                label1.linewidth = 4
                objex = '<span style="color: black;">(Destroyed)</span>'
                if yy == undefined:
                    if "asteroid" in planet_obj.belonging:
                        for p in planets:
                            if p.belonging == label1.text:
                                objex = '<span style="color: green;">(Present)</span>'
                        choose_s.selected = "none"
                        choose_p.selected = "none"
                        selected=planet_obj.belonging
                        obj_t.text = '\n<div id="data">' + '<b>Asteroid</b> ' + objex + ' | Values:\n' + str((planet_obj.mass/me)) + '*me kg\n' + str(round(mag(planet_obj.momentum/planet_obj.mass)),1) + ' m/s\nBelongs to: ' + planet_obj.belonging_system + '</div> \n'
                else:
                    for p in planets:
                        if p.name == label1.text:
                            objex = '<span style="color: green;">(Present)</span>'
                    choose_s.selected = "none"
                    choose_p.selected = label1.text
                    selected=planet_obj.name
                    obj_t.text =  '\n<div id="data">' + '<b>' + planet_obj.name +'</b> ' + objex + ' | Values:\n' + str((planet_obj.mass/me)) + '*me kg\n' + str(round(mag(planet_obj.momentum/planet_obj.mass)),1) + ' m/s velocity\n' + str(yy[3]) + '*au, original distance to star\n' + str((planet_obj.mass*1000)/(3.14159265359*((planet_obj.original_radius*100000)**3)*(4/3))) + ' g/cm&#179</div>\n'
    else:
        # give asteroid a belonging system by finding the nearest star
        distances=[]
        names=[]
        for i in stars:
            distance = i.pos-evt.pos
            distances.append(mag(distance))
            names.append(i.belonging)
        index_worth = distances.index(min(distances))
        system = names[index_worth]
        if min(distances)>10*au: system="none"
        
        # create asteroid
        global int
        loc = evt.pos
        global asteroid_momentum
        global asteroid_mass
        as_planet = sphere(pos=loc, radius=54179000, color=color.white, mass=asteroid_mass*me, momentum=vector(0,asteroid_momentum,0), belonging="asteroid"+str(int), belonging_system=system)
        label_ps = label(pos=as_planet.pos, text="asteroid"+str(int), xoffset=20, yoffset=12, space=as_planet.radius, height=10, border=6, font="sans", belonging=system )
        planet_click = sphere(  pos=as_planet.pos, radius=16*as_planet.radius, color=color.white, opacity=0.1, belonging=as_planet.belonging, belonging_system=system )
        label_ps.line = False
        click_obj_planets.append(planet_click)
        planets.append(as_planet)
        labels.append(label_ps)
        int += 1

scene.append_to_title('\n\nAsteroid Settings:\n\n')

def S_asteroid_momentum(s):
    global asteroid_momentum
    global asteroid_mass
    asteroid_momentum = s.value*(asteroid_mass*me)
    wt_am.text = str(s.value) + " m/s speed (y-axis)"
slider_m = slider( bind=S_asteroid_momentum, min=0, max=100000, value=0, pos=scene.title_anchor, length=200)
wt_am = wtext(text="0 m/s speed (y-axis)", pos=scene.title_anchor)

scene.append_to_title('\n')

def S_asteroid_mass(s):
    global asteroid_mass
    asteroid_mass = (s.value/10)
    wt_ama.text = str(round((s.value/10), 2)) + " *me kg" 
slider_ma = slider( bind=S_asteroid_mass, min=0, max=100, value=4, pos=scene.title_anchor, length=200)
wt_ama = wtext(text="0.4 *me kg", pos=scene.title_anchor)

scene.append_to_title('\n\nSettings:\n')

#a_trial(c):
#    
#
#r2 = radio(bind=a_trial, text='Trial')

scene.bind('click', activateLabelOrAsteroid)

following = True
scene.append_to_title('\n')
button( bind=B_clickaction, text='<div class="tooltip"><img src="https://www.materialui.co/materialIcons/av/library_add_black_24x24.png"><span class="tooltiptext">OnClick Action: Object selection</span></div>', pos=scene.title_anchor )
def B_following(b):
    global following
    if following == True:
        following = False
        b.text = '<div class="tooltip"><img src="https://www.materialui.co/materialIcons/image/switch_camera_grey_24x24.png"><span class="tooltiptext">Camera not following targets</span></div>'
        return
    else:
        following = True
        b.text = '<div class="tooltip"><img src="https://www.materialui.co/materialIcons/image/switch_camera_black_24x24.png"><span class="tooltiptext">Camera following targets</span></div>'
button( bind=B_following, text='<div class="tooltip"><img src="https://www.materialui.co/materialIcons/image/switch_camera_black_24x24.png"><span class="tooltiptext">Camera following targets</span></div>', pos=scene.title_anchor )

better_view = False
def B_better_view(b):
    global better_view
    if better_view == False:
        b.text = '<div class="tooltip"><img src="https://www.materialui.co/materialIcons/image/camera_black_24x24.png"><span class="tooltiptext">Better view (of solar systems)</span></div>'
        better_view = True
        return
    else:
        b.text = '<div class="tooltip"><img src="https://www.materialui.co/materialIcons/image/camera_grey_24x24.png"><span class="tooltiptext">Normal view</span></div>'
        better_view = False
button( bind=B_better_view, text='<div class="tooltip"><img src="https://www.materialui.co/materialIcons/image/camera_grey_24x24.png"><span class="tooltiptext">Normal view</span></div>', pos=scene.title_anchor )

def B_clear_trails(b):
    for x in trails:
        x.clear()
button( bind=B_clear_trails, text='<div class="tooltip"><img src="https://www.materialui.co/materialIcons/action/highlight_off_black_24x24.png"><span class="tooltiptext">Clear all trails</span></div>', pos=scene.title_anchor )

trails_tf = True
def B_stop_trails(b):
    global trails_tf
    if trails_tf == True:
        trails_tf = False
        b.text = '<div class="tooltip"><img src="https://www.materialui.co/materialIcons/av/not_interested_grey_24x24.png"><span class="tooltiptext">Trails: False</span></div>'
        for x in trails:
            x.stop()
        return
    else:
        trails_tf = True
        b.text = '<div class="tooltip"><img src="https://www.materialui.co/materialIcons/av/not_interested_black_24x24.png"><span class="tooltiptext">Trails: True</span></div>'
        for x in trails:
            x.start()
button( bind=B_stop_trails, text='<div class="tooltip"><img src="https://www.materialui.co/materialIcons/av/not_interested_black_24x24.png"><span class="tooltiptext">Trails: True</span></div>', pos=scene.title_anchor )
    
obj_t = wtext(text="\n\n", pos=scene.title_anchor)

graph_plot = graph(scroll=True, fast=False, xmin=0, xmax=1, title=selected, xtitle="Time [s]", ytitle="Velocity [m/s]", width=16*40, height=9*25)
plot_s = gcurve(label="Velocity", color=color.red)

#while loop

for star in stars: star.force = vector(0,0,0)
for planet in planets: planet.force = vector(0,0,0)

while (t >-1):#
    rate(r) #time
    
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
    
    if bu == True: # if program_runs_continuous
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

        #planet1.force = gforce(planet1,star)+gforce(planet1,planet2)+gforce(planet1,planet3)+gforce(planet1,planet4)
        #planet2.force = gforce(planet2,star)+gforce(planet2,planet1)+gforce(planet2,planet3)+gforce(planet2,planet4)
        #planet3.force = gforce(planet3,star)+gforce(planet3,planet1)+gforce(planet3,planet2)+gforce(planet3,planet4)
        #planet4.force = gforce(planet4,star)+gforce(planet4,planet1)+gforce(planet4,planet2)+gforce(planet4,planet3)
    
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
                        plot_s.plot( pos = [t , mag(planet.momentum)] )
                        graph_plot.xmax = t
                    elif planet.belonging == selected:
                        scene.center = planet.pos
                        plot_s.plot( pos = [t , mag(planet.momentum)] )
                        graph_plot.xmax = t
                    else:
                        pass

        if following == True:
            if choose_s.selected is not "none" and choose_p.selected is "none":
                for star in stars:
                    if star.name == choose_s.selected:
                        scene.center = star.pos
                        plot_s.plot( pos = [t , mag(star.momentum)] )
                        graph_plot.xmax = t
                        
        if following == True:
            if choose_s.selected is "none" and choose_p.selected is "none":
                for planet in planets:
                    if planet.belonging == selected:
                        scene.center = planet.pos
                        plot_s.plot( pos = [t , mag(planet.momentum)] )
                        graph_plot.xmax = t
        
        if t == 60*5: scene.autoscale = False
        t += dt
        t_real += 1/r
        wt2.text = "Realtime/Time: " + str(round((t/60)/60, 1)) + "h/" + str(round(t_real, 1)) + "s"

