from vpython import *
e_graph = gcurve(color=color.blue)

scene = canvas(title='<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">',
     x=0, y=0, width=16*40, height=9*25,
     center=vector(0,0,0), background=vector(0,0,0))

#scientific constants/variables
K = 89875517873681764 #N*m2*C^−2
k = 1.38064852*(10**-23) #m2*kg*s-2*K-1
G = 6.67408*(10**-11) #m^3 kg^-1 s^-2, gravitational constant
c = 2.998*(10**8)
sun_mass = 1.989*(10**30) #kg
sun_radius = 695510000 #m
sun_lightforce = 3.86*(10**26) #J/s
hydrogen_atom_mass = 1.6735575*(10**-27) #kg
helium_atom_mass = 6.6464764*(10**-27) #kg
co_atom_mass = 1.9944235*(10**-26) #kg
#heat capcities, J/kg*K
specific_heat_co = 1262
specific_heat_helium = 5192
specific_heat_hydrogen = 14300
#programming constants/variables
r = 60
current_time = 0 #years
addition_years = 100000 #years added 
time_run = True #if time ismoving on
status = 'Burning Helium, core expanding.'
status_eq = 'No values yet.'
burning = True
white_dwarf = False

#changable/new scientific variables
composition_dict = {
    "hydrogen": 1,
    "helium": 0,
    "co" : 0,
}
new_sun_mass = 1.989*(10**30) #kg
core_mass = new_sun_mass*0.1
new_sun_radius = 695510000 #m
new_sun_lightforce = sun_lightforce*((new_sun_mass/sun_mass)**3.5)
sun_mass_loss_per_year = (new_sun_lightforce/(c**2))*60*60*24*365

sun_volume = (4/3)*pi*(sun_radius**3)
new_sun_density = new_sun_mass/sun_volume
sun_core_pressure = (2*G*(sun_mass**2))/(pi*(sun_radius**4))

average_atom_mass_core = (((composition_dict["helium"]*100)*helium_atom_mass)+((composition_dict["hydrogen"]*100)*hydrogen_atom_mass)+((composition_dict["co"]*100)*co_atom_mass))/100
average_heat_capacity_core = ((core_mass*composition_dict["helium"])/new_sun_mass*10)*specific_heat_helium+((core_mass*composition_dict["hydrogen"])/new_sun_mass*10)*specific_heat_hydrogen+((core_mass*composition_dict["co"])/new_sun_mass*10)*specific_heat_co
print(average_heat_capacity_core)

#Core temp
sun_core_temp = (G*new_sun_mass*average_atom_mass_core)/(new_sun_radius*(3/2)*k)

#unchanging density, always average
#MASS on point in radius r
def M(r):
    return new_sun_density*(4/3)*pi*(r**3)

#PRESSURE in r part of radius
def P(r):
    return (3/(8*pi))*((G*(new_sun_mass**2))/(new_sun_radius**4))*(1-((r**2)/(new_sun_radius**2)))

#Temp change on free fall
temp_change = ((((3/10))*(G*((new_sun_mass**2)/new_sun_radius)))/((new_sun_mass)*average_heat_capacity_core))

star = sphere( pos=vector(0,0,0), radius = sun_radius, color=color.yellow, mass = sun_mass, momentum=vector(0,0,0), make_trail=False, lightforce = sun_lightforce, name="sun", opacity=0.5 )
star_helium_burning = sphere( pos=vector(0,0,0), radius = sun_radius*0.2, color=color.orange, name="sun_help_obj", visible=False )

status_text = wtext(text='<b>Status: '+status+'</b>\n', pos=scene.title_anchor)
status_eq_text = wtext(text='<b>Hydrostatic Equilibrium Status: '+status_eq+'</b>\n', pos=scene.title_anchor)

def time_run_slider_function(s):
    global addition_years
    addition_years = s.value
time_run_slider = slider( bind=time_run_slider_function, min=0 , max=addition_years*r*5, value=addition_years*r, pos=scene.title_anchor, length=200)

current_time_text = wtext(text='Lived: '+str(current_time)+' years (' + str(current_time*60) + ' years/sec)\n', pos=scene.title_anchor)
sun_lifetime_text = wtext(text='Total Lifetime (Main Sequence): '+str(0)+' years', pos=scene.title_anchor)
sun_lifetime_text_extended = wtext(text=' ≈ 10^'+str(len(str(0)))+' years', pos=scene.title_anchor)
sun_lifetime_progress_bar = wtext(text='<div class="w3-light-grey w3-tiny" style="width:640px; border: 1px solid grey"><div class="w3-container w3-green" style="width:0%">0%</div></div>', pos=scene.title_anchor)
html_text = wtext(text='<script>function hide() {var x = document.getElementById("hide_sources");if (x.style.display === "none") {x.style.display = "block";} else {x.style.display = "none"}}</script>', pos=scene.title_anchor)

#def time_run_slower(b):
#    global addition_years
#    addition_years -= 600000
#button( bind=time_run_slower, text='+ 10-³ y/s', pos=scene.title_anchor )

#def time_run_button(b):
#    global time_run
#    if time_run == True:
#        time_run = False
#        b.text = "<b>Play</b>"
#        return
#    else:
#        time_run = True
#        b.text = "<b>Pause</b>"
#button( bind=time_run_button, text='<b>Pause</b>', pos=scene.title_anchor )

#def time_run_faster(b):
#    global addition_years
#    addition_years += 600000
#button( bind=time_run_faster, text='+ 10³ y/s', pos=scene.title_anchor )

spliter = wtext(text='<br>', pos=scene.title_anchor)
information_text = wtext(text='<b>Information Star:</b>', pos=scene.title_anchor)
information_text_mass = wtext(text='\nMass: '+ str(new_sun_mass) +' kg (' + str(round(new_sun_mass/sun_mass, 3)) + ' *sun_mass)<br>', pos=scene.title_anchor)

def remove_mass(b):
    global new_sun_mass
    addition_value = 2*(10**30)
    old_sun_mass = new_sun_mass
    new_sun_mass -= addition_value
    percentage_mass_add = new_sun_mass/addition_value
    #only when mass is addet to inner layers
    old_amount = composition_dict["helium"]*old_sun_mass
    composition_dict["helium"] = old_amount/new_sun_mass
    old_amount_h = composition_dict["hydrogen"]*(old_sun_mass*0.1)
    composition_dict["hydrogen"] = (old_amount_h-(0.1*addition_value))/(new_sun_mass*0.1)
button( bind=remove_mass, text='- 1*sun_mass (Hydrogen, equaly distributed)', pos=scene.title_anchor )

def add_mass(b):
    global new_sun_mass
    addition_value = sun_mass
    old_sun_mass = new_sun_mass
    new_sun_mass += addition_value
    percentage_mass_add = new_sun_mass/addition_value
    #only when mass is addet to inner layers
    old_amount = composition_dict["helium"]*old_sun_mass
    composition_dict["helium"] = old_amount/new_sun_mass
    #composition_dict["helium"] = composition_dict["helium"]*((old_sun_mass)/(new_sun_mass))
    #composition_dict["hydrogen"] = 1-composition_dict["helium"]
    old_amount_h = composition_dict["hydrogen"]*(old_sun_mass*0.1)
    composition_dict["hydrogen"] = ((old_amount_h+(addition_value*0.1)))/(new_sun_mass*0.1)
button( bind=add_mass, text='+ 1*sun_mass (Hydrogen, equaly distributed)', pos=scene.title_anchor )

information_text_radius = wtext(text='\nRadius: '+ str(new_sun_radius) +' m<br>', pos=scene.title_anchor)

def remove_radius(b):
    global new_sun_radius
    addition_value_radius = 10**3
    new_sun_radius-= addition_value_radius
button( bind=remove_radius, text='- 10^3 m', pos=scene.title_anchor )

def add_radius(b):
    global new_sun_radius
    global new_sun_density
    global new_sun_mass
    addition_value_radius = 10**3
    new_sun_radius += addition_value_radius
    new_sun_density=(new_sun_mass)/((4/3)*pi*(new_sun_radius**3))
    new_sun_mass=new_sun_density*((4/3)*pi*(new_sun_radius**3))
    print(new_sun_mass)
button( bind=add_radius, text='+ 10^3 m', pos=scene.title_anchor )

spliter_core = wtext(text='<br><br>', pos=scene.title_anchor)
information_text_core = wtext(text='<b>Information Star Core:</b>\n', pos=scene.title_anchor)
information_text_sun_core_mass = wtext(text='\nCore Mass: '+ str(new_sun_mass/10) +' kg<br>', pos=scene.title_anchor)
information_text_sun_core_temp = wtext(text='\nCore Temperature: '+ str(sun_core_temp) +' K', pos=scene.title_anchor)
information_text_sun_core_pressure = wtext(text='\nCore Pressure: '+ str(P(0)) +' Pa', pos=scene.title_anchor)
information_text_composition_dict = wtext(text='Elements: H('+ str(composition_dict["hydrogen"]) + '), He('+ str(composition_dict["helium"]) + '), C('+ str(composition_dict["co"]) + ')', pos=scene.title_anchor)

information_text_links = wtext(text='<button onclick="hide()"><b>Sources/Links</b></button><div id="hide_sources" style="display: none;">\nhttp://earthguide.ucsd.edu/virtualmuseum/images/raw/protonprotonchain.jpg\nhttp://astronomy.swin.edu.au/cosmos/M/Main+Sequence+Lifetime\nhttp://www.pa.uky.edu/~wilhelm/ast192_f09/Calculating%20the%20Lifetime%20of%20the%20Sun.pdf\n\nhttps://www.atnf.csiro.au/outreach/education/senior/astrophysics/stellarevolution_postmain.html\nhttp://abyss.uoregon.edu/~js/ast122/lectures/lec16.html\nHyperphysics: http://230nsc1.phy-astr.gsu.edu/hbase/hframe.html</div>', pos=scene.caption_anchor)

e_plot = graph(scroll=True, fast=False, xmin=0, xmax=new_sun_mass, title="Fusion temperatures compared with simulated star fusion potentials", xtitle="Years", ytitle="Temperature Potetntial", width=16*40, height=9*25)
plot_e = gcurve(label="Energy", color=color.red)
plot_h = gcurve(label="H to He fusion")
plot_k = gcurve(label="He to Co/O fusion")
plot_c = gcurve(label="Co to Mg/Na/Ne fusion")
plot_o = gcurve(label="O to S/P/Si fusion")
plot_s = gcurve(label="Si to Fe fusion")
#hydrogen_plot = gcurve(label="Hydrogen")
#helium_plot = gcurve(color=color.red, label="Helium")
#carbon_plot = gcurve(color=color.blue, label="Carbon")

#while loop
while current_time > -1:
    rate(r)

    #lifetime calculations
    per_reaction_energy = 4.32*(10**-12)
    reaction_per_sec = new_sun_lightforce/per_reaction_energy

    sun_core_mass = core_mass
    information_text_sun_core_mass.text='Core Mass: '+ str(new_sun_mass/10) +' kg'
    kg_per_reaction = 6.692*(10**-27)
    possible_reactions = sun_core_mass/kg_per_reaction

    lifetime = possible_reactions/reaction_per_sec
    sun_lifetime = lifetime/(pi*(10**7))
    
    plot_e.plot( pos = [current_time, (sun_core_temp + temp_change)] )
    plot_k.plot( pos = [current_time , 10**8] )
    plot_h.plot( pos = [current_time , 15*(10**6)] )
    plot_c.plot( pos = [current_time , 5*(10**8)] )
    plot_o.plot( pos = [current_time , 1.4*(10**9)] )
    plot_s.plot( pos = [current_time , 2*(10**9)] )
    e_plot.xmax = current_time

    #hydrogen_plot.plot( pos = [current_time, composition_dict["hydrogen"]] )
    #helium_plot.plot( pos = [current_time, composition_dict["helium"]] )
    #carbon_plot.plot( pos = [current_time, composition_dict["co"]] )
    #not as precise:
    #sun_lifetime = (10**10)*(((sun_mass/new_sun_mass)**2.5)) #/(new_sun_lightforce/sun_lightforce))

    #time management
    if time_run == True:
        current_time += addition_years
        current_time_text.text = 'Lived: '+str(current_time)+' years (' + str(addition_years*60) + ' years/sec)\n'
        sun_lifetime_progress_bar.text = '<div class="w3-light-grey w3-tiny" style="width:880px; border: 1px solid grey"><div class="w3-container w3-green" style="width:' + str((current_time/sun_lifetime)*100) + '%">' + str(round((current_time/sun_lifetime)*100, 2)) + '%</div></div>'
        star_helium_burning.visible=True
        if round((current_time/sun_lifetime)*100, 2) > 100:
            sun_lifetime_text.text=''
            sun_lifetime_text_extended.text=''
            status = 'Main sequence end, Hertzsprung gap'
            status_text.text='<b>Status: '+status+'</b>\n'
            #helium white dwarf
            free_fall_time_counter = 0
            if (sun_core_temp + temp_change) < 10**8:
                status = 'Burning Hydrogen end. Helium white dwarf.'
                status_text.text='<b>Status: '+status+'</b>\n'
                sun_lifetime_progress_bar.text = False
                star_helium_burning.visible=False
                #falltime
                free_fall_time = (((3*pi)/(32*G*new_sun_density))**(1/2))/60/60/24/365
                free_fall_time_counter += free_fall_time
                if free_fall_time_counter > addition_years:
                    free_fall_time_counter -= addition_years
                else:
                    #collapse white dwarf
                    white_dwarf = True
                    radius_wd = (4*pi*K)/(G*(((4/3)*pi)**(5/3))*(new_sun_mass**(1/3)))
                    print(radius_wd)
                    star.radius = radius_wd
            elif 10**8 < (sun_core_temp + temp_change) < 5*(10**8): #
                sun_lifetime_progress_bar.text = False
                star_helium_burning.visible=False
                if composition_dict["helium"] <0.01:
                    status = 'Burning to Carbon complete.'
                    status_text.text='<b>Status: '+status+'</b>\n'
                else:
                    status = 'Burning till C-O star (Triple Alpha Process)'
                    status_text.text='<b>Status: '+status+'</b>\n'
                    #core composition
                    helium_loss = addition_years*60*60*24*365*(8.8*10**37)*(24*(helium_atom_mass)/(core_mass))
                    co_gain = addition_years*60*60*24*365*(8.8*10**37)*(1*(co_atom_mass)/(core_mass))
                    composition_dict["helium"] = composition_dict["helium"] - helium_loss
                    composition_dict["co"] = composition_dict["co"] + co_gain
                    information_text_composition_dict.text='\nElements: H('+ str(round(composition_dict["hydrogen"], 3)) + '), He('+ str(round(composition_dict["helium"], 3)) + '), C('+ str(composition_dict["co"]) + ')'
                    #lifetime while co bruning
                    per_reaction_energy_co = 1.3273*(10**-23) + 2.15891*(10**-26) + (1.602*(10**-19)*200000)#Energy of 2 fusions, 2He to Be, He and Be to C + 2 gamma rays
                    reaction_per_sec_co = new_sun_lightforce/per_reaction_energy_co

                    sun_core_mass = core_mass
                    information_text_sun_core_mass.text='Core Mass: '+ str(new_sun_mass/10) +' kg'
                    kg_per_reaction_co = 6.692*(10**-27)
                    possible_reactions_co = sun_core_mass/kg_per_reaction_co

                    lifetime_co = possible_reactions_co/reaction_per_sec_co
                    sun_lifetime_co = lifetime_co/(pi*(10**7))
                    sun_lifetime_text.text='Total Lifetime (C-O white dwarf): '+str(round(sun_lifetime_co, 2))+' years'
                    sun_lifetime_text_extended.text=' ≈ 10^'+str(len(str(round(sun_lifetime_co))))+' years'
            elif 5*(10**8) < (sun_core_temp + temp_change) < 1.4*(10**9):
                status = 'Burning Carbon.'
                status_text.text='<b>Status: '+status+'</b>\n'
            elif 1.4*(10**9) < (sun_core_temp + temp_change) < 2*(10**9):
                status = 'Burning Oxygen.'
                status_text.text='<b>Status: '+status+'</b>\n'
            elif 2*(10**9) < (sun_core_temp + temp_change) < 5*(10**8):
                status = 'Burning Silicon.'
                status_text.text='<b>Status: '+status+'</b>\n'
            else:
                status = "Burning till Fe core star, then black hole or neutron star."
                status_text.text='<b>Status: '+status+'</b>\n'
        else:
            hydrogen_loss = addition_years*60*60*24*365*(8.8*10**37)*(4*(hydrogen_atom_mass)/(core_mass))
            helium_gain = addition_years*60*60*24*365*(8.8*10**37)*(1*(helium_atom_mass)/(core_mass))
            composition_dict["hydrogen"] = composition_dict["hydrogen"] - hydrogen_loss
            composition_dict["helium"] = composition_dict["helium"] + hydrogen_loss
            information_text_composition_dict.text='\nElements: H('+ str(round(composition_dict["hydrogen"], 3)) + '), He('+ str(round(composition_dict["helium"], 3)) + '), C('+ str(composition_dict["co"]) + ')'
            sun_lifetime_text.text='Total Lifetime (Main Sequence): '+str(round(sun_lifetime, 2))+' years'
            sun_lifetime_text_extended.text=' ≈ 10^'+str(len(str(round(sun_lifetime))))+' years'
        #mass loss thorugh energy loss
        new_sun_mass-=sun_mass_loss_per_year*addition_years
        new_sun_density = new_sun_mass/sun_volume
        #other variables
        sun_core_temp = (G*new_sun_mass*average_atom_mass_core)/(new_sun_radius*(3/2)*k)
        average_atom_mass_core = (((composition_dict["helium"]*100)*helium_atom_mass)+((composition_dict["hydrogen"]*100)*hydrogen_atom_mass)+((composition_dict["co"]*100)*co_atom_mass))/100
        temp_change = ((((3/10))*(G*((new_sun_mass**2)/new_sun_radius)))/((new_sun_mass)*average_heat_capacity_core))
        core_mass = new_sun_mass*0.1

    #hydrostatisches gleichgweicht
    pressure_eq = (P(new_sun_radius+((new_sun_radius/2)/2))-P(new_sun_radius-((new_sun_radius/2)/2)))/(new_sun_radius/2)
    gravity_eq = 2*-((G*M(new_sun_radius/2)*new_sun_density)/(((new_sun_radius/2)**2)))
    if round(pressure_eq)==round(gravity_eq):
        status_eq='Pressure and gravity are in check.'
        status_eq_text.text='<b style="color: green;">Hydrostatic Equilibrium Status: '+status_eq+'</b>('+ str(round(pressure_eq))+ '=' +str(round(gravity_eq)) +')\n'
    else:
        status_eq='Pressure and gravity are NOT in check.' 
        status_eq_text.text='<b style="color: red;">Hydrostatic Equilibrium Status: '+status_eq+'</b>('+ str(round(pressure_eq))+ '=' +str(round(gravity_eq)) +')\n'
    #obj uppdate
    if white_dwarf == False:
        star.radius = new_sun_radius
    star.mass = new_sun_mass
    #console.log(sun_central_pressure) 
    information_text_sun_core_temp.text='\nCore Temperature: '+ str(sun_core_temp) +' K'
    information_text_sun_core_pressure.text='\nCore Pressure: '+ str(P(0)) +' Pa<br>'
    information_text_mass.text='\nMass: '+ str(new_sun_mass) +' kg (' + str(round(new_sun_mass/sun_mass, 3)) + ' *sun_mass)<br>'
    information_text_radius.text='\nRadius: '+ str(new_sun_radius) +' m<br>'
    t = (-(G*sun_mass*2*(10**30))/(sun_radius**2))
    