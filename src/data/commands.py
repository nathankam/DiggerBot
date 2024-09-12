from src.models.message import Command


COMMANDS = [
    Command(
        name='HELP',
        code='!help',
        description='List all available commands'
    ),
    Command(
        name='ME',
        code='!me',
        description='Add yourself to the users',
        instructions='!me <username>'
    ),
    Command(
        name='ADD USER',
        code='!user_create',
        description='Create a new user and add to the group',
        instructions='!create <username> <discord_id>',
        restricted=True
    ),
    Command(
        name='REMOVE USER',
        code='!user_delete',
        description='Delete existing user',
        instructions='!user_delete <username>',
        restricted=True
    ),
    Command(
        name='FREEZE USER',
        code='!user_freeze',
        description='Freeze user streak',
        instructions='!user_freeze <username>',
        restricted=True
    ),
    Command(
        name='UNFREEZE USER',
        code='!user_unfreeze',
        description='Unfreeze user streak',
        instructions='!user_unfreeze <username>',
        restricted=True
    ),
    Command(
        name='LIST USERS',
        code='!user_list',
        description='List all users'
    ),
    Command(
        name='GET INFO',
        code='!info',
        description='Show group info',
        instructions='!info'
    ),
    Command(
        name='GOAGAIN',
        code='!goagain',
        description='Restart the group if it was paused',
        instructions='!info'
    ),
    Command(
        name='LIST SCHEDULES',
        code='!list_schedules',
        description='Show available options for scheduling the sessions',
        instructions='!list_schedules'
    ),
    Command(
        name='SET SCHEDULE',
        code='!set_schedule',
        description='Set the schedule for the group, takes effect next session.',
        instructions='!set_schedule <schedule_id>',
    ),
    Command(
        name='SETTINGS',
        code='!settings_show',
        description='Show current settings'
    ),
    Command(
        name='SETTINGS INC',
        code='!settings_incognito',
        description='Toggle incognito mode',
        instructions='!settings_incognito <0/1>'
    ),
    Command(
        name='SETTINGS GER',
        code='!settings_ger',
        description='Set the genre exploration ratio',
        instructions='!settings_ger <ratio>'
    ),
    Command(
        name='SETTINGS GSR',
        code='!settings_gsr',
        description='Set the genre/subgenre ratio',
        instructions='!settings_gsr <ratio>'
    ),
    Command(
        name='SETTINGS GPR',
        code='!settings_gpr',
        description='Set the genre proportions',
        instructions='!settings_gpr <genre> <weight>'
    ),
    Command(
        name='SETTINGS GPR SHOW',
        code='!settings_sgprop',
        description='Show the genre proportions'
    ),
]
