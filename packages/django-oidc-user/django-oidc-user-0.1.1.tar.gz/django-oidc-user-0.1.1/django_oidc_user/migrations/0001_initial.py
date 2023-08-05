# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-18 16:06
from __future__ import unicode_literals

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 20 characters or fewer. Letters, numbers and underscore characters', max_length=20, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[\\w]+$', 32), 'Enter a valid username.', 'invalid username')], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=254, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, null=True, unique=True, verbose_name='email address')),
                ('email_verified', models.BooleanField(default=False, verbose_name='email verified')),
                ('phone', models.CharField(blank=True, max_length=16, validators=[django.core.validators.RegexValidator(message="The number must be entered in the format: '+999999999' with up to 15 digits.", regex='^\\+?1?\\d{9,15}$')], verbose_name='phone number')),
                ('phone_verified', models.BooleanField(default=False, verbose_name='phone verified')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into the admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='updated at')),
                ('website', models.CharField(max_length=254, validators=[django.core.validators.URLValidator()], verbose_name='website')),
                ('zoneinfo', models.CharField(choices=[('Africa/Abidjan', 'Abidjan'), ('Africa/Accra', 'Accra'), ('Africa/Addis_Ababa', 'Addis Ababa'), ('Africa/Algiers', 'Algiers'), ('Africa/Asmara', 'Asmara'), ('Africa/Asmera', 'Asmera'), ('Africa/Bamako', 'Bamako'), ('Africa/Bangui', 'Bangui'), ('Africa/Banjul', 'Banjul'), ('Africa/Bissau', 'Bissau'), ('Africa/Blantyre', 'Blantyre'), ('Africa/Brazzaville', 'Brazzaville'), ('Africa/Bujumbura', 'Bujumbura'), ('Africa/Cairo', 'Cairo'), ('Africa/Casablanca', 'Casablanca'), ('Africa/Ceuta', 'Ceuta'), ('Africa/Conakry', 'Conakry'), ('Africa/Dakar', 'Dakar'), ('Africa/Dar_es_Salaam', 'Dar es Salaam'), ('Africa/Djibouti', 'Djibouti'), ('Africa/Douala', 'Douala'), ('Africa/El_Aaiun', 'El Aaiun'), ('Africa/Freetown', 'Freetown'), ('Africa/Gaborone', 'Gaborone'), ('Africa/Harare', 'Harare'), ('Africa/Johannesburg', 'Johannesburg'), ('Africa/Juba', 'Juba'), ('Africa/Kampala', 'Kampala'), ('Africa/Khartoum', 'Khartoum'), ('Africa/Kigali', 'Kigali'), ('Africa/Kinshasa', 'Kinshasa'), ('Africa/Lagos', 'Lagos'), ('Africa/Libreville', 'Libreville'), ('Africa/Lome', 'Lome'), ('Africa/Luanda', 'Luanda'), ('Africa/Lubumbashi', 'Lubumbashi'), ('Africa/Lusaka', 'Lusaka'), ('Africa/Malabo', 'Malabo'), ('Africa/Maputo', 'Maputo'), ('Africa/Maseru', 'Maseru'), ('Africa/Mbabane', 'Mbabane'), ('Africa/Mogadishu', 'Mogadishu'), ('Africa/Monrovia', 'Monrovia'), ('Africa/Nairobi', 'Nairobi'), ('Africa/Ndjamena', 'Ndjamena'), ('Africa/Niamey', 'Niamey'), ('Africa/Nouakchott', 'Nouakchott'), ('Africa/Ouagadougou', 'Ouagadougou'), ('Africa/Porto-Novo', 'Porto Novo'), ('Africa/Sao_Tome', 'Sao Tome'), ('Africa/Timbuktu', 'Timbuktu'), ('Africa/Tripoli', 'Tripoli'), ('Africa/Tunis', 'Tunis'), ('Africa/Windhoek', 'Windhoek'), ('America/Adak', 'Adak'), ('America/Anchorage', 'Anchorage'), ('America/Anguilla', 'Anguilla'), ('America/Antigua', 'Antigua'), ('America/Araguaina', 'Araguaina'), ('America/Argentina/Buenos_Aires', 'Argentina'), ('America/Argentina/Catamarca', 'Argentina'), ('America/Argentina/ComodRivadavia', 'Argentina'), ('America/Argentina/Cordoba', 'Argentina'), ('America/Argentina/Jujuy', 'Argentina'), ('America/Argentina/La_Rioja', 'Argentina'), ('America/Argentina/Mendoza', 'Argentina'), ('America/Argentina/Rio_Gallegos', 'Argentina'), ('America/Argentina/Salta', 'Argentina'), ('America/Argentina/San_Juan', 'Argentina'), ('America/Argentina/San_Luis', 'Argentina'), ('America/Argentina/Tucuman', 'Argentina'), ('America/Argentina/Ushuaia', 'Argentina'), ('America/Aruba', 'Aruba'), ('America/Asuncion', 'Asuncion'), ('America/Atikokan', 'Atikokan'), ('America/Atka', 'Atka'), ('America/Bahia', 'Bahia'), ('America/Bahia_Banderas', 'Bahia Banderas'), ('America/Barbados', 'Barbados'), ('America/Belem', 'Belem'), ('America/Belize', 'Belize'), ('America/Blanc-Sablon', 'Blanc Sablon'), ('America/Boa_Vista', 'Boa Vista'), ('America/Bogota', 'Bogota'), ('America/Boise', 'Boise'), ('America/Buenos_Aires', 'Buenos Aires'), ('America/Cambridge_Bay', 'Cambridge Bay'), ('America/Campo_Grande', 'Campo Grande'), ('America/Cancun', 'Cancun'), ('America/Caracas', 'Caracas'), ('America/Catamarca', 'Catamarca'), ('America/Cayenne', 'Cayenne'), ('America/Cayman', 'Cayman'), ('America/Chicago', 'Chicago'), ('America/Chihuahua', 'Chihuahua'), ('America/Coral_Harbour', 'Coral Harbour'), ('America/Cordoba', 'Cordoba'), ('America/Costa_Rica', 'Costa Rica'), ('America/Creston', 'Creston'), ('America/Cuiaba', 'Cuiaba'), ('America/Curacao', 'Curacao'), ('America/Danmarkshavn', 'Danmarkshavn'), ('America/Dawson', 'Dawson'), ('America/Dawson_Creek', 'Dawson Creek'), ('America/Denver', 'Denver'), ('America/Detroit', 'Detroit'), ('America/Dominica', 'Dominica'), ('America/Edmonton', 'Edmonton'), ('America/Eirunepe', 'Eirunepe'), ('America/El_Salvador', 'El Salvador'), ('America/Ensenada', 'Ensenada'), ('America/Fort_Nelson', 'Fort Nelson'), ('America/Fort_Wayne', 'Fort Wayne'), ('America/Fortaleza', 'Fortaleza'), ('America/Glace_Bay', 'Glace Bay'), ('America/Godthab', 'Godthab'), ('America/Goose_Bay', 'Goose Bay'), ('America/Grand_Turk', 'Grand Turk'), ('America/Grenada', 'Grenada'), ('America/Guadeloupe', 'Guadeloupe'), ('America/Guatemala', 'Guatemala'), ('America/Guayaquil', 'Guayaquil'), ('America/Guyana', 'Guyana'), ('America/Halifax', 'Halifax'), ('America/Havana', 'Havana'), ('America/Hermosillo', 'Hermosillo'), ('America/Indiana/Indianapolis', 'Indiana'), ('America/Indiana/Knox', 'Indiana'), ('America/Indiana/Marengo', 'Indiana'), ('America/Indiana/Petersburg', 'Indiana'), ('America/Indiana/Tell_City', 'Indiana'), ('America/Indiana/Vevay', 'Indiana'), ('America/Indiana/Vincennes', 'Indiana'), ('America/Indiana/Winamac', 'Indiana'), ('America/Indianapolis', 'Indianapolis'), ('America/Inuvik', 'Inuvik'), ('America/Iqaluit', 'Iqaluit'), ('America/Jamaica', 'Jamaica'), ('America/Jujuy', 'Jujuy'), ('America/Juneau', 'Juneau'), ('America/Kentucky/Louisville', 'Kentucky'), ('America/Kentucky/Monticello', 'Kentucky'), ('America/Knox_IN', 'Knox IN'), ('America/Kralendijk', 'Kralendijk'), ('America/La_Paz', 'La Paz'), ('America/Lima', 'Lima'), ('America/Los_Angeles', 'Los Angeles'), ('America/Louisville', 'Louisville'), ('America/Lower_Princes', 'Lower Princes'), ('America/Maceio', 'Maceio'), ('America/Managua', 'Managua'), ('America/Manaus', 'Manaus'), ('America/Marigot', 'Marigot'), ('America/Martinique', 'Martinique'), ('America/Matamoros', 'Matamoros'), ('America/Mazatlan', 'Mazatlan'), ('America/Mendoza', 'Mendoza'), ('America/Menominee', 'Menominee'), ('America/Merida', 'Merida'), ('America/Metlakatla', 'Metlakatla'), ('America/Mexico_City', 'Mexico City'), ('America/Miquelon', 'Miquelon'), ('America/Moncton', 'Moncton'), ('America/Monterrey', 'Monterrey'), ('America/Montevideo', 'Montevideo'), ('America/Montreal', 'Montreal'), ('America/Montserrat', 'Montserrat'), ('America/Nassau', 'Nassau'), ('America/New_York', 'New York'), ('America/Nipigon', 'Nipigon'), ('America/Nome', 'Nome'), ('America/Noronha', 'Noronha'), ('America/North_Dakota/Beulah', 'North Dakota'), ('America/North_Dakota/Center', 'North Dakota'), ('America/North_Dakota/New_Salem', 'North Dakota'), ('America/Ojinaga', 'Ojinaga'), ('America/Panama', 'Panama'), ('America/Pangnirtung', 'Pangnirtung'), ('America/Paramaribo', 'Paramaribo'), ('America/Phoenix', 'Phoenix'), ('America/Port-au-Prince', 'Port au Prince'), ('America/Port_of_Spain', 'Port of Spain'), ('America/Porto_Acre', 'Porto Acre'), ('America/Porto_Velho', 'Porto Velho'), ('America/Puerto_Rico', 'Puerto Rico'), ('America/Punta_Arenas', 'Punta Arenas'), ('America/Rainy_River', 'Rainy River'), ('America/Rankin_Inlet', 'Rankin Inlet'), ('America/Recife', 'Recife'), ('America/Regina', 'Regina'), ('America/Resolute', 'Resolute'), ('America/Rio_Branco', 'Rio Branco'), ('America/Rosario', 'Rosario'), ('America/Santa_Isabel', 'Santa Isabel'), ('America/Santarem', 'Santarem'), ('America/Santiago', 'Santiago'), ('America/Santo_Domingo', 'Santo Domingo'), ('America/Sao_Paulo', 'Sao Paulo'), ('America/Scoresbysund', 'Scoresbysund'), ('America/Shiprock', 'Shiprock'), ('America/Sitka', 'Sitka'), ('America/St_Barthelemy', 'St Barthelemy'), ('America/St_Johns', 'St Johns'), ('America/St_Kitts', 'St Kitts'), ('America/St_Lucia', 'St Lucia'), ('America/St_Thomas', 'St Thomas'), ('America/St_Vincent', 'St Vincent'), ('America/Swift_Current', 'Swift Current'), ('America/Tegucigalpa', 'Tegucigalpa'), ('America/Thule', 'Thule'), ('America/Thunder_Bay', 'Thunder Bay'), ('America/Tijuana', 'Tijuana'), ('America/Toronto', 'Toronto'), ('America/Tortola', 'Tortola'), ('America/Vancouver', 'Vancouver'), ('America/Virgin', 'Virgin'), ('America/Whitehorse', 'Whitehorse'), ('America/Winnipeg', 'Winnipeg'), ('America/Yakutat', 'Yakutat'), ('America/Yellowknife', 'Yellowknife'), ('Antarctica/Casey', 'Casey'), ('Antarctica/Davis', 'Davis'), ('Antarctica/DumontDUrville', 'DumontDUrville'), ('Antarctica/Macquarie', 'Macquarie'), ('Antarctica/Mawson', 'Mawson'), ('Antarctica/McMurdo', 'McMurdo'), ('Antarctica/Palmer', 'Palmer'), ('Antarctica/Rothera', 'Rothera'), ('Antarctica/South_Pole', 'South Pole'), ('Antarctica/Syowa', 'Syowa'), ('Antarctica/Troll', 'Troll'), ('Antarctica/Vostok', 'Vostok'), ('Arctic/Longyearbyen', 'Longyearbyen'), ('Asia/Aden', 'Aden'), ('Asia/Almaty', 'Almaty'), ('Asia/Amman', 'Amman'), ('Asia/Anadyr', 'Anadyr'), ('Asia/Aqtau', 'Aqtau'), ('Asia/Aqtobe', 'Aqtobe'), ('Asia/Ashgabat', 'Ashgabat'), ('Asia/Ashkhabad', 'Ashkhabad'), ('Asia/Atyrau', 'Atyrau'), ('Asia/Baghdad', 'Baghdad'), ('Asia/Bahrain', 'Bahrain'), ('Asia/Baku', 'Baku'), ('Asia/Bangkok', 'Bangkok'), ('Asia/Barnaul', 'Barnaul'), ('Asia/Beirut', 'Beirut'), ('Asia/Bishkek', 'Bishkek'), ('Asia/Brunei', 'Brunei'), ('Asia/Calcutta', 'Calcutta'), ('Asia/Chita', 'Chita'), ('Asia/Choibalsan', 'Choibalsan'), ('Asia/Chongqing', 'Chongqing'), ('Asia/Chungking', 'Chungking'), ('Asia/Colombo', 'Colombo'), ('Asia/Dacca', 'Dacca'), ('Asia/Damascus', 'Damascus'), ('Asia/Dhaka', 'Dhaka'), ('Asia/Dili', 'Dili'), ('Asia/Dubai', 'Dubai'), ('Asia/Dushanbe', 'Dushanbe'), ('Asia/Famagusta', 'Famagusta'), ('Asia/Gaza', 'Gaza'), ('Asia/Harbin', 'Harbin'), ('Asia/Hebron', 'Hebron'), ('Asia/Ho_Chi_Minh', 'Ho Chi Minh'), ('Asia/Hong_Kong', 'Hong Kong'), ('Asia/Hovd', 'Hovd'), ('Asia/Irkutsk', 'Irkutsk'), ('Asia/Istanbul', 'Istanbul'), ('Asia/Jakarta', 'Jakarta'), ('Asia/Jayapura', 'Jayapura'), ('Asia/Jerusalem', 'Jerusalem'), ('Asia/Kabul', 'Kabul'), ('Asia/Kamchatka', 'Kamchatka'), ('Asia/Karachi', 'Karachi'), ('Asia/Kashgar', 'Kashgar'), ('Asia/Kathmandu', 'Kathmandu'), ('Asia/Katmandu', 'Katmandu'), ('Asia/Khandyga', 'Khandyga'), ('Asia/Kolkata', 'Kolkata'), ('Asia/Krasnoyarsk', 'Krasnoyarsk'), ('Asia/Kuala_Lumpur', 'Kuala Lumpur'), ('Asia/Kuching', 'Kuching'), ('Asia/Kuwait', 'Kuwait'), ('Asia/Macao', 'Macao'), ('Asia/Macau', 'Macau'), ('Asia/Magadan', 'Magadan'), ('Asia/Makassar', 'Makassar'), ('Asia/Manila', 'Manila'), ('Asia/Muscat', 'Muscat'), ('Asia/Nicosia', 'Nicosia'), ('Asia/Novokuznetsk', 'Novokuznetsk'), ('Asia/Novosibirsk', 'Novosibirsk'), ('Asia/Omsk', 'Omsk'), ('Asia/Oral', 'Oral'), ('Asia/Phnom_Penh', 'Phnom Penh'), ('Asia/Pontianak', 'Pontianak'), ('Asia/Pyongyang', 'Pyongyang'), ('Asia/Qatar', 'Qatar'), ('Asia/Qyzylorda', 'Qyzylorda'), ('Asia/Rangoon', 'Rangoon'), ('Asia/Riyadh', 'Riyadh'), ('Asia/Saigon', 'Saigon'), ('Asia/Sakhalin', 'Sakhalin'), ('Asia/Samarkand', 'Samarkand'), ('Asia/Seoul', 'Seoul'), ('Asia/Shanghai', 'Shanghai'), ('Asia/Singapore', 'Singapore'), ('Asia/Srednekolymsk', 'Srednekolymsk'), ('Asia/Taipei', 'Taipei'), ('Asia/Tashkent', 'Tashkent'), ('Asia/Tbilisi', 'Tbilisi'), ('Asia/Tehran', 'Tehran'), ('Asia/Tel_Aviv', 'Tel Aviv'), ('Asia/Thimbu', 'Thimbu'), ('Asia/Thimphu', 'Thimphu'), ('Asia/Tokyo', 'Tokyo'), ('Asia/Tomsk', 'Tomsk'), ('Asia/Ujung_Pandang', 'Ujung Pandang'), ('Asia/Ulaanbaatar', 'Ulaanbaatar'), ('Asia/Ulan_Bator', 'Ulan Bator'), ('Asia/Urumqi', 'Urumqi'), ('Asia/Ust-Nera', 'Ust Nera'), ('Asia/Vientiane', 'Vientiane'), ('Asia/Vladivostok', 'Vladivostok'), ('Asia/Yakutsk', 'Yakutsk'), ('Asia/Yangon', 'Yangon'), ('Asia/Yekaterinburg', 'Yekaterinburg'), ('Asia/Yerevan', 'Yerevan'), ('Atlantic/Azores', 'Azores'), ('Atlantic/Bermuda', 'Bermuda'), ('Atlantic/Canary', 'Canary'), ('Atlantic/Cape_Verde', 'Cape Verde'), ('Atlantic/Faeroe', 'Faeroe'), ('Atlantic/Faroe', 'Faroe'), ('Atlantic/Jan_Mayen', 'Jan Mayen'), ('Atlantic/Madeira', 'Madeira'), ('Atlantic/Reykjavik', 'Reykjavik'), ('Atlantic/South_Georgia', 'South Georgia'), ('Atlantic/St_Helena', 'St Helena'), ('Atlantic/Stanley', 'Stanley'), ('Australia/ACT', 'ACT'), ('Australia/Adelaide', 'Adelaide'), ('Australia/Brisbane', 'Brisbane'), ('Australia/Broken_Hill', 'Broken Hill'), ('Australia/Canberra', 'Canberra'), ('Australia/Currie', 'Currie'), ('Australia/Darwin', 'Darwin'), ('Australia/Eucla', 'Eucla'), ('Australia/Hobart', 'Hobart'), ('Australia/LHI', 'LHI'), ('Australia/Lindeman', 'Lindeman'), ('Australia/Lord_Howe', 'Lord Howe'), ('Australia/Melbourne', 'Melbourne'), ('Australia/NSW', 'NSW'), ('Australia/North', 'North'), ('Australia/Perth', 'Perth'), ('Australia/Queensland', 'Queensland'), ('Australia/South', 'South'), ('Australia/Sydney', 'Sydney'), ('Australia/Tasmania', 'Tasmania'), ('Australia/Victoria', 'Victoria'), ('Australia/West', 'West'), ('Australia/Yancowinna', 'Yancowinna'), ('Brazil/Acre', 'Acre'), ('Brazil/DeNoronha', 'DeNoronha'), ('Brazil/East', 'East'), ('Brazil/West', 'West'), ('CET', 'CET'), ('CST6CDT', 'CST6CDT'), ('Canada/Atlantic', 'Atlantic'), ('Canada/Central', 'Central'), ('Canada/East-Saskatchewan', 'East Saskatchewan'), ('Canada/Eastern', 'Eastern'), ('Canada/Mountain', 'Mountain'), ('Canada/Newfoundland', 'Newfoundland'), ('Canada/Pacific', 'Pacific'), ('Canada/Saskatchewan', 'Saskatchewan'), ('Canada/Yukon', 'Yukon'), ('Chile/Continental', 'Continental'), ('Chile/EasterIsland', 'EasterIsland'), ('Cuba', 'Cuba'), ('EET', 'EET'), ('EST', 'EST'), ('EST5EDT', 'EST5EDT'), ('Egypt', 'Egypt'), ('Eire', 'Eire'), ('Etc/GMT', 'GMT'), ('Etc/GMT+0', 'GMT+0'), ('Etc/GMT+1', 'GMT+1'), ('Etc/GMT+10', 'GMT+10'), ('Etc/GMT+11', 'GMT+11'), ('Etc/GMT+12', 'GMT+12'), ('Etc/GMT+2', 'GMT+2'), ('Etc/GMT+3', 'GMT+3'), ('Etc/GMT+4', 'GMT+4'), ('Etc/GMT+5', 'GMT+5'), ('Etc/GMT+6', 'GMT+6'), ('Etc/GMT+7', 'GMT+7'), ('Etc/GMT+8', 'GMT+8'), ('Etc/GMT+9', 'GMT+9'), ('Etc/GMT-0', 'GMT-0'), ('Etc/GMT-1', 'GMT-1'), ('Etc/GMT-10', 'GMT-10'), ('Etc/GMT-11', 'GMT-11'), ('Etc/GMT-12', 'GMT-12'), ('Etc/GMT-13', 'GMT-13'), ('Etc/GMT-14', 'GMT-14'), ('Etc/GMT-2', 'GMT-2'), ('Etc/GMT-3', 'GMT-3'), ('Etc/GMT-4', 'GMT-4'), ('Etc/GMT-5', 'GMT-5'), ('Etc/GMT-6', 'GMT-6'), ('Etc/GMT-7', 'GMT-7'), ('Etc/GMT-8', 'GMT-8'), ('Etc/GMT-9', 'GMT-9'), ('Etc/GMT0', 'GMT0'), ('Etc/Greenwich', 'Greenwich'), ('Etc/UCT', 'UCT'), ('Etc/UTC', 'UTC'), ('Etc/Universal', 'Universal'), ('Etc/Zulu', 'Zulu'), ('Europe/Amsterdam', 'Amsterdam'), ('Europe/Andorra', 'Andorra'), ('Europe/Astrakhan', 'Astrakhan'), ('Europe/Athens', 'Athens'), ('Europe/Belfast', 'Belfast'), ('Europe/Belgrade', 'Belgrade'), ('Europe/Berlin', 'Berlin'), ('Europe/Bratislava', 'Bratislava'), ('Europe/Brussels', 'Brussels'), ('Europe/Bucharest', 'Bucharest'), ('Europe/Budapest', 'Budapest'), ('Europe/Busingen', 'Busingen'), ('Europe/Chisinau', 'Chisinau'), ('Europe/Copenhagen', 'Copenhagen'), ('Europe/Dublin', 'Dublin'), ('Europe/Gibraltar', 'Gibraltar'), ('Europe/Guernsey', 'Guernsey'), ('Europe/Helsinki', 'Helsinki'), ('Europe/Isle_of_Man', 'Isle of Man'), ('Europe/Istanbul', 'Istanbul'), ('Europe/Jersey', 'Jersey'), ('Europe/Kaliningrad', 'Kaliningrad'), ('Europe/Kiev', 'Kiev'), ('Europe/Kirov', 'Kirov'), ('Europe/Lisbon', 'Lisbon'), ('Europe/Ljubljana', 'Ljubljana'), ('Europe/London', 'London'), ('Europe/Luxembourg', 'Luxembourg'), ('Europe/Madrid', 'Madrid'), ('Europe/Malta', 'Malta'), ('Europe/Mariehamn', 'Mariehamn'), ('Europe/Minsk', 'Minsk'), ('Europe/Monaco', 'Monaco'), ('Europe/Moscow', 'Moscow'), ('Europe/Nicosia', 'Nicosia'), ('Europe/Oslo', 'Oslo'), ('Europe/Paris', 'Paris'), ('Europe/Podgorica', 'Podgorica'), ('Europe/Prague', 'Prague'), ('Europe/Riga', 'Riga'), ('Europe/Rome', 'Rome'), ('Europe/Samara', 'Samara'), ('Europe/San_Marino', 'San Marino'), ('Europe/Sarajevo', 'Sarajevo'), ('Europe/Saratov', 'Saratov'), ('Europe/Simferopol', 'Simferopol'), ('Europe/Skopje', 'Skopje'), ('Europe/Sofia', 'Sofia'), ('Europe/Stockholm', 'Stockholm'), ('Europe/Tallinn', 'Tallinn'), ('Europe/Tirane', 'Tirane'), ('Europe/Tiraspol', 'Tiraspol'), ('Europe/Ulyanovsk', 'Ulyanovsk'), ('Europe/Uzhgorod', 'Uzhgorod'), ('Europe/Vaduz', 'Vaduz'), ('Europe/Vatican', 'Vatican'), ('Europe/Vienna', 'Vienna'), ('Europe/Vilnius', 'Vilnius'), ('Europe/Volgograd', 'Volgograd'), ('Europe/Warsaw', 'Warsaw'), ('Europe/Zagreb', 'Zagreb'), ('Europe/Zaporozhye', 'Zaporozhye'), ('Europe/Zurich', 'Zurich'), ('GB', 'GB'), ('GB-Eire', 'GB Eire'), ('GMT', 'GMT'), ('GMT+0', 'GMT+0'), ('GMT-0', 'GMT 0'), ('GMT0', 'GMT0'), ('Greenwich', 'Greenwich'), ('HST', 'HST'), ('Hongkong', 'Hongkong'), ('Iceland', 'Iceland'), ('Indian/Antananarivo', 'Antananarivo'), ('Indian/Chagos', 'Chagos'), ('Indian/Christmas', 'Christmas'), ('Indian/Cocos', 'Cocos'), ('Indian/Comoro', 'Comoro'), ('Indian/Kerguelen', 'Kerguelen'), ('Indian/Mahe', 'Mahe'), ('Indian/Maldives', 'Maldives'), ('Indian/Mauritius', 'Mauritius'), ('Indian/Mayotte', 'Mayotte'), ('Indian/Reunion', 'Reunion'), ('Iran', 'Iran'), ('Israel', 'Israel'), ('Jamaica', 'Jamaica'), ('Japan', 'Japan'), ('Kwajalein', 'Kwajalein'), ('Libya', 'Libya'), ('MET', 'MET'), ('MST', 'MST'), ('MST7MDT', 'MST7MDT'), ('Mexico/BajaNorte', 'BajaNorte'), ('Mexico/BajaSur', 'BajaSur'), ('Mexico/General', 'General'), ('NZ', 'NZ'), ('NZ-CHAT', 'NZ CHAT'), ('Navajo', 'Navajo'), ('PRC', 'PRC'), ('PST8PDT', 'PST8PDT'), ('Pacific/Apia', 'Apia'), ('Pacific/Auckland', 'Auckland'), ('Pacific/Bougainville', 'Bougainville'), ('Pacific/Chatham', 'Chatham'), ('Pacific/Chuuk', 'Chuuk'), ('Pacific/Easter', 'Easter'), ('Pacific/Efate', 'Efate'), ('Pacific/Enderbury', 'Enderbury'), ('Pacific/Fakaofo', 'Fakaofo'), ('Pacific/Fiji', 'Fiji'), ('Pacific/Funafuti', 'Funafuti'), ('Pacific/Galapagos', 'Galapagos'), ('Pacific/Gambier', 'Gambier'), ('Pacific/Guadalcanal', 'Guadalcanal'), ('Pacific/Guam', 'Guam'), ('Pacific/Honolulu', 'Honolulu'), ('Pacific/Johnston', 'Johnston'), ('Pacific/Kiritimati', 'Kiritimati'), ('Pacific/Kosrae', 'Kosrae'), ('Pacific/Kwajalein', 'Kwajalein'), ('Pacific/Majuro', 'Majuro'), ('Pacific/Marquesas', 'Marquesas'), ('Pacific/Midway', 'Midway'), ('Pacific/Nauru', 'Nauru'), ('Pacific/Niue', 'Niue'), ('Pacific/Norfolk', 'Norfolk'), ('Pacific/Noumea', 'Noumea'), ('Pacific/Pago_Pago', 'Pago Pago'), ('Pacific/Palau', 'Palau'), ('Pacific/Pitcairn', 'Pitcairn'), ('Pacific/Pohnpei', 'Pohnpei'), ('Pacific/Ponape', 'Ponape'), ('Pacific/Port_Moresby', 'Port Moresby'), ('Pacific/Rarotonga', 'Rarotonga'), ('Pacific/Saipan', 'Saipan'), ('Pacific/Samoa', 'Samoa'), ('Pacific/Tahiti', 'Tahiti'), ('Pacific/Tarawa', 'Tarawa'), ('Pacific/Tongatapu', 'Tongatapu'), ('Pacific/Truk', 'Truk'), ('Pacific/Wake', 'Wake'), ('Pacific/Wallis', 'Wallis'), ('Pacific/Yap', 'Yap'), ('Poland', 'Poland'), ('Portugal', 'Portugal'), ('ROC', 'ROC'), ('ROK', 'ROK'), ('Singapore', 'Singapore'), ('Turkey', 'Turkey'), ('UCT', 'UCT'), ('US/Alaska', 'Alaska'), ('US/Aleutian', 'Aleutian'), ('US/Arizona', 'Arizona'), ('US/Central', 'Central'), ('US/East-Indiana', 'East Indiana'), ('US/Eastern', 'Eastern'), ('US/Hawaii', 'Hawaii'), ('US/Indiana-Starke', 'Indiana Starke'), ('US/Michigan', 'Michigan'), ('US/Mountain', 'Mountain'), ('US/Pacific', 'Pacific'), ('US/Pacific-New', 'Pacific New'), ('US/Samoa', 'Samoa'), ('UTC', 'UTC'), ('Universal', 'Universal'), ('W-SU', 'W SU'), ('WET', 'WET'), ('Zulu', 'Zulu')], default='Europe/London', max_length=254, verbose_name='time zone')),
                ('locale', models.CharField(choices=[('no-NO', 'Norwegian'), ('hu-HU', 'Hungarian'), ('fr-FR', 'French'), ('it-IT', 'Italian'), ('lt-LT', 'Lithuanian'), ('nl-NL', 'Dutch'), ('sk-SK', 'Slovak'), ('zh-CN', 'Chinese'), ('tr-TR', 'Turkish'), ('de-DE', 'German'), ('ru-RU', 'Russian'), ('sv-SE', 'Swedish'), ('cs-CZ', 'Czech'), ('en-US', 'English'), ('sl-SI', 'Slovenian'), ('da-DK', 'Danish'), ('ro-RO', 'Romanian'), ('lv-LV', 'Latvian'), ('et-EE', 'Estonian'), ('bg-BG', 'Bulgarian'), ('hr-HR', 'Croatian'), ('el-GR', 'Greek'), ('fi-FI', 'Finnish'), ('es-ES', 'Spanish'), ('pt-PT', 'Portuguese'), ('pl-PL', 'Polish')], default='en-US', max_length=254, verbose_name='locale')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
