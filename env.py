import os
from os.path import expanduser

hdname = '/media/sxr/TOURO/'

homedir = expanduser('~') + '/'

# 0: routeviews; 1: ripe ris
collectors = [('', 0, '20011101'), ('rrc00', 1, '19991101'), ('rrc01', 1,\
            '20000801'), ('rrc03', 1, '20010201'),\
             ('rrc04', 1, '20010501'), ('rrc05', 1, '20010701'), ('rrc06', 1,\
                     '20010901'), ('rrc07', 1, '20020501'),\
             ]

# number of days in total
daterange = [('20061225', 4, 177, '2006 taiwan cable cut', 0, 11,\
                '2006-12-26 12:25:00', '', 'Earthquake\nhappened'),
            ('20081218', 4, 181, '2008 mediterranean cable cut 2', 1, 11,\
                '2008-12-19 07:28:00', '', 'First\ncable\ncut'),
            ('20030813', 4, 113, '2003 east coast blackout', 2, 11,\
                '2003-08-14 20:10:39', '2003-08-15 03:00:00',\
                'Blackouts\nduration'),
            ('20050911', 4, 135, '2005 LA blackout', 3, 11,\
                '2005-09-12 20:00:00', '', 'Blackouts\nbegan'),
            ('20050828', 4, 166, '2005 Hurricane Katrina', 4, 11,\
                '2005-08-28 18:00:00', '', 'Reached\npeak\nstrength'),
            ('20080129', 4, 156, '2008 mediterranean cable cut 1', 5, 11,\
                '2008-01-30 04:30:00', '', 'Cable\ncut'),
            ('20100226', 4, 177, '2010 Chile earthquake', 6, 11,\
                '2010-02-27 06:34:00', '', 'Earthquake\nhappened'),
            ('20110310', 4, 179, '2011 Japan Tsunami', 7, 10,\
                '2011-03-11 05:46:00', '', 'Tsunami\nhappened'),
            ('20121021', 4, 173, '2012 Hurricane Sandy', 8, 10,\
                '2012-10-24 19:00:00', '', 'Landfall\non\nJamaica'),
            ('20130317', 4, 190, '2013 Spamhaus DDoS', 9, 10,\
                '2013-03-18 00:00:00', '2013-03-19 00:00:00', 'Attack\nbegan'),
            ('20140601', 7, 186, 'for CDF in intro 2014', 10, 01,\
                '', '', ''),
            ('20060601', 7, 152, 'for CDF in intro 2006', 11, 01,\
                '', '', ''),
            ('20130207', 4, 191, '2013 Northeastern U.S. Blackout', 12, 01,\
                '2013-02-08 21:15:00', '2013-02-09 23:59:59',
                'Several\nregions\nblackouts'),
            ('20100413', 4, 180, '2010 Sea-Me undersea cable cut', 13, 01,\
                '', '', ''),
            ('20120221', 4, -1, 'Australia route leakage', 14, 00,\
                '', '', ''),
            ('20120807', 4, -1, 'Canada route leakage', 15, 00,\
                '', '', ''),
            ('20030124', 4, 168, '2003 Slammer worm', 16, 10,\
                '2003-01-25 05:30:00', '', 'Worm\nstarted'),
            ('20130321', 4, 185, '20130322 EASSy/SEACOM Outages', 17, 10,\
                '', '', ''),
            ('20130213', 4, 192, '20130214 SEACOM Outages', 18, 10,\
                '2013-02-14 11:59:00', '', 'Outage\nconfirmed'),
            ('20110327', 4, 179, '20110328 Caucasus cable cut', 19, 10,\
                '2011-03-28 13:00:00', '', 'Cable\ncut'),
            ('20121222', 4, 177, '20121223 Georgia-Russia cable cut', 20, 01,\
                '2012-12-23 00:00:00', '2012-12-23 23:59:59', 'Cable\ncut'),
            ('20120224', 4, -1, '20120225 0913 TEAMS cable cut in east Africa', 21, 00,\
                '', '', ''),
            ('20120425', 4, -1, '20120426 0904 TEAMS cable cut again in east\
                    Africa', 22, 00,\
                '', '', ''),
            ('20110824', 4, -1, '201108 hurricane Irene in east U.S.', 23, 01,\
                '', '', ''),
            ('20070701', 4, -1, '2007 training data', 24, 00,\
                '', '', ''),
            ]
