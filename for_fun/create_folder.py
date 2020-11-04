#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: create_folder
# @Date: 2020/11/4
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os
import random

ROOT_PATH = '/mnt/d/wyatc/Documents/temp/MyFolder2'

if __name__ == '__main__':
    firm_names = ['Addison_Co', 'Ajo_Co', 'Ajo_Co', 'Albany_Schenectady_Troy,_Co', 'Albany_Schenectady_Troy,_Co',
                  'Albuquerque,_Co', 'Allegan_Co', 'Allegan_Co', 'Allegheny_Co', 'Allegheny,_Co', 'Allentown,_Co',
                  'Allentown_Bethlehem_Easton,_Co', 'Allentown_Bethlehem_Easton,_Co', 'Allentown_Bethlehem_Easton,_Co',
                  'Alton_Co', 'Altoona,_Co', 'Altoona,_Co', 'Amador_Co', 'Anchorage,_Co', 'Anne_Co', 'Anthony,_Co',
                  'Arecibo,_Co', 'Armstrong_Co', 'Aspen,_Co', 'Atlanta,_Co', 'Atlanta,_Co', 'Atlanta,_Co',
                  'Atlanta,_Co', 'Atlantic_Co', 'Atlantic_Co', 'Bakersfield,_Co', 'Baltimore,_Co', 'Baltimore,_Co',
                  'Baltimore,_Co', 'Baltimore,_Co', 'Baltimore,_Co', 'Baton_Co', 'Baton_Co', 'Baton_Co',
                  'Beaumont_Port_Co', 'Beaumont_Port_Co', 'Beauregard_Co', 'Beaver,_Co', 'Belding,_Co',
                  'Bellefontaine,_Co', 'Benton_Co', 'Benton_Co', 'Benzie_Co', 'Billings,_Co', 'Billings,_Co',
                  'Birmingham,_Co', 'Birmingham,_Co', 'Birmingham,_Co', 'Birmingham,_Co', 'Boise_Northern_Co',
                  'Boise_Northern_Co', 'Bonner_Co', 'Boston,_Co', 'Boston_Lawrence_Worcester_Co',
                  'Boston_Lawrence_Worcester_Co', 'Boston_Manchester_Portsmouth_Co', 'Boyd_Co', 'Bristol,_Co',
                  'Buffalo_Niagara_Co', 'Buffalo_Niagara_Co', 'Burlington,_Co', 'Butte,_Co', 'Calaveras_Co',
                  'Campbell_Clermont_Co', 'Canon_Co', 'Canton,_Co', 'Canton_Massillon,_Co', 'Canton_Massillon,_Co',
                  'Canton_Massillon,_Co', 'Cass_Co', 'Center_Co', 'Central_Co', 'Central_Co', 'Charleston,_Co',
                  'Charleston,_Co', 'Charleston,_Co', 'Charleston,_Co', 'Charlotte,_Co', 'Charlotte_Gastonia,_Co',
                  'Charlotte_Gastonia_Rock_Co', 'Charlotte_Rock_Co', 'Chattanooga,_Co', 'Cherokee_Co', 'Cheshire_Co',
                  'Chicago,_Co', 'Chicago_Gary_Lake_Co', 'Chicago_Gary_Lake_Co', 'Chicago_Gary_Lake_Co',
                  'Chicago_Naperville,_Co', 'Chico_Co', 'Chico,_Co', 'Chico,_Co', 'Chico,_Co', 'Chico,_Co',
                  'Cincinnati,_Co', 'Cincinnati_Hamilton,_Co', 'Cincinnati_Hamilton,_Co', 'Cincinnati_Hamilton,_Co',
                  'Clairton_Co', 'Clark_Co', 'Clarksville_Hopkinsville,_Co', 'Clearfield_Co', 'Cleveland,_Co',
                  'Cleveland,_Co', 'Cleveland,_Co', 'Cleveland_Akron_Lorain,_Co', 'Cleveland_Akron_Lorain,_Co',
                  'Cleveland_Akron_Lorain,_Co', 'Cleveland_Akron_Lorain,_Co', 'Cleveland_Akron_Lorain,_Co',
                  'Clinton_Co', 'Coachella_Co', 'Colbert_Co', 'Collin_Co', 'Colorado_Co', 'Columbia_Co',
                  'Columbiana_Co', 'Columbus,_Co', 'Columbus,_Co', 'Columbus,_Co', 'Columbus,_Co', 'Conewango_Co',
                  'Coso_Co', 'Crawford_Co', 'Cuyahoga_Co', 'Cuyahoga_Co', 'Dakota_Co', 'Dallas_Fort_Co',
                  'Dallas_Fort_Co', 'Dallas_Fort_Co', 'Dayton_Springfield,_Co', 'Dayton_Springfield,_Co',
                  'Dayton_Springfield,_Co', 'Delaware_Co', 'Delta,_Co', 'Denver_Co', 'Denver_Boulder,_Co',
                  'Denver_Boulder,_Co', 'Denver_Boulder_Greeley_Ft._Co', 'Denver_Boulder_Greeley_Ft._Co', 'Detroit,_Co',
                  'Detroit,_Co', 'Detroit_Ann_Co', 'Detroit_Ann_Co', 'Detroit_Ann_Co', 'Detroit_Ann_Co', 'Door_Co',
                  'Door_Co', 'Douglas_Co', 'Douglas_Co', 'Dukes_Co', 'Duluth,_Co', 'Eagan,_Co', 'Eagle_Co', 'East_Co',
                  'East_Co', 'East_Co', 'East_Co', 'East_Co', 'East_Co', 'Edmonson_Co', 'El_Co', 'El_Co', 'El_Co',
                  'Erie,_Co', 'Erie,_Co', 'Essex_Co', 'Essex_Co', 'Eugene_Springfield,_Co', 'Eugene_Springfield,_Co',
                  'Evansville,_Co', 'Evansville,_Co', 'Evansville,_Co', 'Fairbanks,_Co', 'Fairbanks,_Co', 'Fayette_Co',
                  'Flathead_Co', 'Flint,_Co', 'Flint,_Co', 'Follansbee,_Co', 'Fort_Co', 'Fort_Co', 'Fort_Co',
                  'Franklin_Co', 'Franklin_Co', 'Franklin_Co', 'Fredericksburg,_Co', 'Freehold,_Co', 'Freestone_Co',
                  'Fresno,_Co', 'Frisco,_Co', 'Grand_Co', 'Grand_Co', 'Granite_Co', 'Granite_Co', 'Grant_Co',
                  'Grant_Co', 'Grants_Co', 'Grants_Co', 'Great_Co', 'Greater_Co', 'Greater_Co', 'Greater_Co',
                  'Greeley,_Co', 'Green_Co', 'Greenbrier,_Co', 'Greene_Co', 'Greene_Co', 'Greene_Co',
                  'Greensboro_Winston_Co', 'Greensboro_Winston_Salem_High_Co', 'Groveland_Co', 'Hancock_Co',
                  'Hancock,_Co', 'Harrisburg_Lebanon_Carlisle,_Co', 'Harrisburg_Lebanon_Carlisle,_Co',
                  'Harrisburg_Lebanon_Carlisle,_Co', 'Harrisburg_Lebanon_Carlisle_York,_Co', 'Hartford_New_Co',
                  'Hayden_Co', 'Hayden,_Co', 'Hayden,_Co', 'Hayden,_Co', 'Haywood_Co', 'Hazelwood,_Co',
                  'Hickory_Morganton_Lenoir,_Co', 'Hillsborough_Co', 'Hollis_Co', 'Houston_Galveston_Brazoria,_Co',
                  'Houston_Galveston_Brazoria,_Co', 'Houston_Galveston_Brazoria,_Co', 'Humphreys_Co',
                  'Huntington_Ashland,_Co', 'Huntington_Ashland,_Co', 'Huntington_Ashland,_Co', 'Huron_Co',
                  'Imperial_Co', 'Imperial_Co', 'Imperial_Co', 'Imperial_Co', 'Imperial_Co', 'Imperial_Co', 'Indian_Co',
                  'Indiana,_Co', 'Indianapolis,_Co', 'Indianapolis,_Co', 'Indianapolis,_Co', 'Indianapolis,_Co',
                  'Indianapolis,_Co', 'Iron_Co', 'Iron_Co', 'Iron,_Co', 'Jackson_Co', 'Jackson_Co', 'Jacksonville,_Co',
                  'Jamestown,_Co', 'Jamestown,_Co', 'Jefferson_Co', 'Jefferson_Co', 'Jefferson_Co', 'Jefferson_Co',
                  'Jefferson_Co', 'Jefferson_Co', 'Jefferson_Co', 'Jefferson_Co', 'Jersey_Co', 'Johnstown,_Co',
                  'Johnstown,_Co', 'Johnstown,_Co', 'Johnstown,_Co', 'Juneau,_Co', 'Juniata_Co', 'Kalamazoo_Battle_Co',
                  'Kalispell,_Co', 'Kansas_Co', 'Kent_Co', 'Kent_Co', 'Kent,_Co', 'Kern_Co', 'Kern_Co', 'Kewaunee_Co',
                  'Kewaunee_Co', 'King_Co', 'Klamath_Co', 'Klamath_Co', 'Klamath_Co', 'Knox_Co', 'Knoxville,_Co',
                  'Knoxville,_Co', 'Knoxville,_Co', 'Knoxville,_Co', 'Knoxville_Sevierville_La_Co', 'La_Co', 'La_Co',
                  'LaGrande,_Co', 'Lafayette,_Co', 'Lafourche_Co', 'Lake_Co', 'Lake_Co', 'Lake_Co', 'Lake_Co',
                  'Lake_Co', 'Lake_Co', 'Lake_Co', 'Lake_Co', 'Lamar,_Co', 'Lame_Co', 'Lancaster,_Co', 'Lancaster,_Co',
                  'Lancaster,_Co', 'Lancaster,_Co', 'Lancaster,_Co', 'Lane_Co', 'Lansing_East_Co', 'Las_Co', 'Las_Co',
                  'Lauderdale_Co', 'Laurel_Co', 'Lawrence_Co', 'Lebanon_Co', 'Lemont,_Co', 'Lewiston_Auburn,_Co',
                  'Lexington_Fayette,_Co', 'Libby,_Co', 'Libby,_Co', 'Liberty_Clairton,_Co', 'Liberty_Clairton,_Co',
                  'Lima,_Co', 'Logan,_Co', 'Longmont,_Co', 'Lorain_Co', 'Los_Co', 'Los_Co', 'Los_Co', 'Los_Co',
                  'Los_Co', 'Los_Co', 'Los_Co', 'Los_Co', 'Los_Co', 'Los_Co', 'Los_Co', 'Los_Co', 'Louisville,_Co',
                  'Louisville,_Co', 'Louisville,_Co', 'Lowell,_Co', 'Lower_Co', 'Lucas_Co', 'Lyons_Co', 'Lyons,_Co',
                  'Macon,_Co', 'Macon,_Co', 'Madison_Co']

    property_name = ['total_assets', 'net_income', 'tobinq', 'ebitda', 'ptbi']

    for f_name in firm_names:
        for suffix in property_name:
            tar_dir_path = os.path.join(ROOT_PATH, '{}_{}'.format(f_name, suffix))
            if os.path.isdir(tar_dir_path):
                pass

            else:
                os.makedirs(tar_dir_path)

            for year in range(2000, 2020):
                with open(os.path.join(tar_dir_path, '{}.txt'.format(year)), 'w') as f:
                    f.write(str(random.randint(1, 1000)))
