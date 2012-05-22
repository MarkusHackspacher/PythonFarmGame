import os
from xml.etree import ElementTree as ET

from farmlib.seed import Seed, seeds

class FarmField:

    def __init__(self):
        """ Init FarmField"""

        self.farmtiles={}

    def get_farmtile(self, posx, posy):
        """Get farmtile from given position"""

        arg=str(posx)+'x'+str(posy)
        if self.farmtiles.has_key(arg):
            return self.farmtiles[arg]

        else:
            self.farmtiles[arg]={'water':0,'seed':None}
            return self.farmtiles[arg]

    def set_farmtile(self, posx, posy, farmtile):
        """Set farmtile at given position"""

        arg=str(posx)+'x'+str(posy)
        self.farmtiles[arg]=farmtile

    def plant(self, posx, posy, seed):
        """Plant a seed on the given farmtile position"""

        farmtile=self.get_farmtile(posx, posy)
        if not farmtile['seed'] and seed:
            #plant a new seed on empty place
            farmtile['seed']=seed
            seed.start_grow()
        else:
            return 1 #  error there something on that position

    def harvest(self,posx, posy, inventory, itemscounter):
        """Harvest growed seed from farmtile"""

        farmtile=self.get_farmtile(posx, posy)
        if farmtile['seed']:
            if not farmtile['seed'].growing and farmtile['seed'].to_harvest:
                #harvest seeds
                for i in range(farmtile['seed'].growquantity):
                    itemid=farmtile['seed'].id
                    if itemid not in inventory:
                        inventory.append(itemid)
                        itemscounter[str(itemid)]+=1
                    else:
                        itemscounter[str(itemid)]+=1
                #TODO: add feature to many years seeds
                farmtile['seed']=None
                farmtile['water']=0

    def water(self, posx, posy):
        """Watering a farm tile"""

        farmtile=self.get_farmtile(posx, posy)
        #only one per seed
        if farmtile['water']<100:
            farmtile['water']=100 #  min(farmtile['water']+10,100)
            farmtile['seed'].growendtime-=20*60

    def status(self, posx, posy):
        """Status"""

        farmtile=self.get_farmtile(posx,posy)
        if farmtile['seed']:
            print farmtile['seed'].name, "-", farmtile['seed'].description, "[ End in.",farmtile['seed'].remainstring,"]"

    #UPDATE
    def update(self):
        """update a farmtiles"""

        #update each farmtile
        for farmtile in self.farmtiles.values():
            if farmtile['seed']:
                farmtile['seed'].update(farmtile)

    def save_farmfield(self, filename):
        """Save farmfield to xml file"""

        farmfield=ET.Element('FarmField',{'inventory':str(self.inventory), 'itemscounter':str(self.itemscounter)})

        for ft in self.farmtiles.keys():
            posx=ft.split('x')[0]
            posy=ft.split('x')[1]

            farmtile=self.farmtiles[ft]
            if not farmtile['seed']:continue

            farmtileelem=ET.Element('farmtile', {'posx':posx,'posy':posy,'water':str(farmtile['water'])})

            #store seed if exist
            if farmtile['seed']:

                seed=farmtile['seed']

                seedelem=ET.Element('seed',
                    {
                    'growstarttime':str(seed.growstarttime),
                    'growendtime':str(seed.growendtime),
                    'growing':str(int(seed.growing)),
                    'to_harvest':str(int(seed.to_harvest)),
                    'id':str(seed.id),
                    })
                farmtileelem.append(seedelem)

            farmfield.append(farmtileelem)
        #save created node to file
        ET.ElementTree(farmfield).write(filename)
        return 1

    def load_farmfield(self, filename):
        """Load farmfield from XML file"""

        if not os.path.isfile(filename):
            return 0

        rootelement=ET.parse(open(filename)).getroot()
        if rootelement.tag!="FarmField":return 1

        #load game information
        self.inventory=eval(str(rootelement.attrib['inventory']))
        self.itemscounter=eval(str(rootelement.attrib['itemscounter']))

        for elem in rootelement:
            if elem.tag=="farmtile":
                #if there is a children node (should be /seed/)
                if elem is not None:
                    #got seed
                    if elem[0].tag=="seed":
                        newseed=Seed()
                        newseed.growstarttime=int(elem[0].attrib['growstarttime'])
                        newseed.growendtime=int(elem[0].attrib['growendtime'])
                        newseed.growing=int(elem[0].attrib['growing'])
                        newseed.to_harvest=int(elem[0].attrib['to_harvest'])
                        newseed.id=int(elem[0].attrib['id'])
                        newseed.apply_dict(seeds[newseed.id])

                    #there no seed on the farmtile (wrong tag name)
                    else:newseed=None
                #there no seed on the farmtile
                else:newseed=None

            #restore a farmtile
            px=int(elem.attrib['posx'])
            py=int(elem.attrib['posy'])
            wa=int(elem.attrib['water'])
            newfarmtile={'water':wa, 'seed':newseed}

            self.set_farmtile(px,py,newfarmtile)

        #return 1 as done
        return 1